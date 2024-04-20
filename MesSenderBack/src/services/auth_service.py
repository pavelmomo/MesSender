from datetime import datetime
import time
from . import UserService
import jwt
from passlib.context import CryptContext
from src.repositories import AbstractUOW
from src.config import JWT_SECRET, JWT_COOKIE_NAME, JWT_EXPIRATION_TIME, JWT_ALGORITHM
from src.models import User
from src.schemas import UserCreateDTO, UserDTO, UserLoginDTO


class UserNotExist(Exception):
    pass


class UserAlreadyExist(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidToken(Exception):
    pass


class TokenExpire(Exception):
    pass


class AuthService:
    crypto_context = CryptContext(schemes=["bcrypt"])

    @staticmethod
    async def register(
        user: UserCreateDTO,
        uow: AbstractUOW,
    ) -> UserDTO:
        async with uow:
            check = await uow.users.get_by_username_or_email(user.username, user.email)
            if check is not None:
                raise UserAlreadyExist()
            hashed_password = AuthService.crypto_context.hash(user.password)
            new_user = User(
                username=user.username, email=user.email, password=hashed_password
            )
            new_user = await uow.users.create_user(new_user)
            return UserDTO.model_validate(new_user, from_attributes=True)

    @staticmethod
    async def login(user: UserLoginDTO, uow: AbstractUOW) -> str:
        db_user = await UserService.get_user_by_username(user.username, uow)
        if db_user is None:
            raise UserNotExist
        pass_verify = AuthService.crypto_context.verify(user.password, db_user.password)
        if not pass_verify:
            raise InvalidCredentials
        token = AuthService.create_jwt_token(db_user.id)
        return token

    @staticmethod
    async def authorize(token: str, uow: AbstractUOW):
        decoded_token = AuthService.verify_jwt_token(token)
        if (
            decoded_token is None
            or "sub" not in decoded_token
            or "exp" not in decoded_token
        ):
            raise InvalidToken

        if decoded_token["exp"] - int(time.time()) < 0:
            raise TokenExpire
        user_id = decoded_token["sub"]
        async with uow:
            user = await uow.users.get_by_id(user_id)
            if user is None:
                raise UserNotExist
            return UserDTO.model_validate(user, from_attributes=True)

    @staticmethod
    def create_jwt_token(user_id: int):
        expiration_date = int(time.time()) + JWT_EXPIRATION_TIME
        token_payload = {"sub": user_id, "exp": expiration_date}
        token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            decoded_data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_data
        except jwt.PyJWTError:
            return None
