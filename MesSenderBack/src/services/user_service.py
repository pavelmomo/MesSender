from repositories import AbstractUOW
from schemas import UserReadShortDTO
from models import User


class UserService:
    @staticmethod
    async def get_users_by_partly_username(username: str,uow: AbstractUOW
    ) -> list[UserReadShortDTO]:
        async with uow:
            users = await uow.users.get_by_partly_username(username)
            return [
                UserReadShortDTO.model_validate(x, from_attributes=True) for x in users
            ]
    @staticmethod
    async def get_user_by_username(username: str, uow: AbstractUOW) -> User:
        async with uow:
            user = await uow.users.get_by_username(username)
            return user