from typing import Any, AsyncGenerator, Dict, Optional, Callable, Annotated
from fastapi import Request, Depends, WebSocket
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers
from fastapi_users import exceptions, models, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    JWTStrategy,
    CookieTransport,
)
import jwt
from src.repositories import AbstractUOW, UnitOfWorkPgs, AbstractUserRepository
from src.config import SECRET, COOKIE_NAME
from src.models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    user_db: AbstractUserRepository

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        existing_user = await self.user_db.get_by_username_or_email(
            user_create.username, user_create.email
        )
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)
        return created_user

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> User | None:

        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})
        return user

    async def _update(self, user: models.UP, update_dict: Dict[str, Any]) -> models.UP:
        validated_update_dict = {}
        for field, value in update_dict.items():
            if field == "email" and value != user.email:
                try:
                    await self.get_by_email(value)
                    raise exceptions.UserAlreadyExists()
                except exceptions.UserNotExists:
                    validated_update_dict["email"] = value
                    validated_update_dict["is_verified"] = False
            elif field == "password" and value is not None:
                await self.validate_password(value, user)
                validated_update_dict["hashed_password"] = self.password_helper.hash(
                    value
                )
            elif field == "username" and value != user.username:
                try:
                    await self.get_by_username(value)
                    raise exceptions.UserAlreadyExists()
                except exceptions.UserNotExists:
                    validated_update_dict["username"] = value
            else:
                validated_update_dict[field] = value
        return await self.user_db.update(user, validated_update_dict)

    async def get_by_username(self, username: str) -> User:
        user = await self.user_db.get_by_username(username)
        if user is None:
            raise exceptions.UserNotExists()
        return user


class AuthService:
    fastapi_users: FastAPIUsers
    current_user: Callable
    auth_backend: AuthenticationBackend

    def __init__(self):
        self.init_auth_service()

    def init_auth_service(self):
        self.auth_backend = AuthenticationBackend(
            name="jwt",
            transport=CookieTransport(
                cookie_name=COOKIE_NAME, cookie_max_age=3600, cookie_secure=False
            ),
            get_strategy=self.get_jwt_strategy,
        )
        self.fastapi_users = FastAPIUsers[User, int](
            self.get_user_manager, [self.auth_backend]
        )
        self.current_user = self.fastapi_users.current_user()

    @staticmethod
    async def get_user_manager(
        uow: Annotated[AbstractUOW, Depends(UnitOfWorkPgs)]
    ) -> AsyncGenerator[BaseUserManager[User, int], Any]:
        async with uow:
            yield UserManager(uow.users)

    @staticmethod
    def get_jwt_strategy() -> JWTStrategy:
        return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

    @staticmethod
    async def authorize_ws_endpoint(
        websocket: WebSocket, uow: Annotated[AbstractUOW, Depends(UnitOfWorkPgs)]
    ) -> int | None:
        if COOKIE_NAME not in websocket.cookies:
            return None
        try:
            data = jwt.decode(
                websocket.cookies[COOKIE_NAME],
                SECRET,
                algorithms=["HS256"],
                audience=["fastapi-users:auth"],
            )
            user_id = int(data.get("sub"))
        except (jwt.PyJWTError, ValueError, TypeError):
            return None
        async with uow:
            user = await uow.users.get(user_id)
            return user_id if user is not None else None


AuthServiceInstance = AuthService()
