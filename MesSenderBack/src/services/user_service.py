from repositories import AbstractUOW
from db.exceptions import IncorrectData as IncorrectDataRepo
from schemas.user_schemas import UserDTO
from services.exceptions import IncorrectData as IncorrectDataService, OperationNotPermitted
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
            users = await uow.users.get_active_by_partly_username(username)
            return [
                UserReadShortDTO.model_validate(x, from_attributes=True) for x in users
            ]

    # метод получения пользователя по username
    @staticmethod
    async def get_user_by_username(username: str, uow: AbstractUOW) -> User:
        async with uow:
            user = await uow.users.get_by_username(username)
            return user

    # метод блокировки пользователя
    @staticmethod
    async def ban_user(user_id: int, is_banned: bool, uow: AbstractUOW):
        try:
            async with uow:
                user = await uow.users.get_by_id(user_id)
                if user is None:
                    raise IncorrectDataService
                if user.role == 'admin':
                    raise OperationNotPermitted
                update_dict = {"id": user_id, "is_banned": is_banned}
                await uow.users.update_user(update_dict)

        except IncorrectDataRepo as e:
            raise OperationNotPermitted from e

    # метод получения списка всех пользователей
    @staticmethod
    async def get_all_users(limit: int, offset: int, uow: AbstractUOW) -> list[UserDTO]:
        async with uow:
            users = await uow.users.get_all(limit, offset)
            return [
                UserDTO.model_validate(x, from_attributes=True) for x in users
            ]