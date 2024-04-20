import time
import jwt
from passlib.context import CryptContext
from repositories import AbstractUOW
from config import JWT_SECRET, JWT_EXPIRATION_TIME, JWT_ALGORITHM
from models import User
from schemas import UserCreateDTO, UserDTO, UserLoginDTO, UserUpdateDTO
from . import UserService


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
    async def update_user(update: UserUpdateDTO, user_id: str, uow: AbstractUOW):
        async with uow:
            db_user = await uow.users.get_by_id(user_id)
            updated_user = {"id": db_user.id}
            if db_user.username != update.username or db_user.email != update.email:
                check = await uow.users.get_by_username_or_email(update.username, update.email)
                if check is not None and check.id != user_id:
                    raise UserAlreadyExist()
                updated_user["email"] = update.email
                updated_user["username"] = update.username
            pass_verify = AuthService.crypto_context.verify(update.password, db_user.password)
            if not pass_verify:
                raise InvalidCredentials
            if update.new_password != "":
                new_pass = AuthService.crypto_context.hash(update.new_password)
                updated_user["password"] = new_pass
            await uow.users.update_user(updated_user)
            


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

