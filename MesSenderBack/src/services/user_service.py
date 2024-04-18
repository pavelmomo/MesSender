from src.repositories import AbstractUOW
from src.schemas import UserReadShortDTO


class UserService:
    @staticmethod
    async def get_users_by_partly_username(
        uow: AbstractUOW, username: str
    ) -> list[UserReadShortDTO]:
        async with uow:
            users = await uow.users.get_by_partly_username(username)
            return [
                UserReadShortDTO.model_validate(x, from_attributes=True) for x in users
            ]
