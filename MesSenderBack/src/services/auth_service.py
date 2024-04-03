from typing import Optional, Callable, Annotated
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.config import SECRET
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers
from fastapi_users import exceptions, models, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    JWTStrategy, CookieTransport,
)
from src.models import User
from src.repositories import AbstractUOW, UnitOfWorkPgs, AbstractUserRepository


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

        existing_user = await self.user_db.get_by_username_or_email(user_create.username, user_create.email)
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

    async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:

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
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})
        return user

    async def get_by_username(self, username: str) -> models.UP:
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
            transport=CookieTransport(cookie_name="credits", cookie_max_age=3600),
            get_strategy=self.get_jwt_strategy,
        )
        self.fastapi_users = FastAPIUsers[User, int](self.get_user_manager, [self.auth_backend])
        self.current_user = self.fastapi_users.current_user()

    @staticmethod
    async def get_user_manager(uow: Annotated[AbstractUOW, Depends(UnitOfWorkPgs)]) -> BaseUserManager[User, int]:
        async with uow:
            yield UserManager(uow.users)

    @staticmethod
    def get_jwt_strategy() -> JWTStrategy:
        return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


AuthServiceInstance = AuthService()
