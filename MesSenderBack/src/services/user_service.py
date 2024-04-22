from repositories import AbstractUOW
from schemas import UserReadShortDTO
from models import User


class UserService:
    """
    Сервис выполняет бизнес-логику по работе с пользователями
    (помимо авторизации/аутенфикации/обновления)
    """

    # метод поиска пользователей по вхождению в username
    @staticmethod
    async def get_users_by_partly_username(
        username: str, uow: AbstractUOW
    ) -> list[UserReadShortDTO]:
        async with uow:
            users = await uow.users.get_by_partly_username(username)
            return [
                UserReadShortDTO.model_validate(x, from_attributes=True) for x in users
            ]

    # метод получения пользователя по username
    @staticmethod
    async def get_user_by_username(username: str, uow: AbstractUOW) -> User:
        async with uow:
            user = await uow.users.get_by_username(username)
            return user
