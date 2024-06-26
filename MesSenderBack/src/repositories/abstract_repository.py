from abc import ABC, abstractmethod
from typing import Sequence
from models import DialogUser, Message, User


class AbstractDialogRepository(ABC):
    """
    Репозиторий для сущности Dialog и DialogUser
    """

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def get_active_user_dialogs(
        self, user_id: int, limit: int, offset: int
    ) -> Sequence[DialogUser]:
        raise NotImplementedError

    @abstractmethod
    async def get_dual_dialog_id(self, uid: int, remote_uid: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def create_dual_dialog(self, user_id: int, remote_user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_dialog_users(self, dialog_id: int) -> list[int]:
        raise NotImplementedError


class AbstractUserRepository(ABC):
    """
    Репозиторий для сущности User
    """

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username_or_email(self, username: str, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_active_by_partly_username(self, username: str) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def check_user_existing(self, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, update_dict: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[User]:
        raise NotImplementedError


class AbstractMessageRepository(ABC):
    """
    Репозиторий для сущности Меssage
    """

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, message: Message) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_messages(
        self, dialog_id: int, user_id: int, limit: int, offset: int
    ) -> Sequence[Message]:
        raise NotImplementedError

    @abstractmethod
    async def set_viewed_status(self, ids: list[int], dialog_id: int) -> bool:
        raise NotImplementedError


class AbstractUOW(ABC):
    """
    Определение интерфейса для паттерна Unit Of Work
    """

    users: AbstractUserRepository
    messages: AbstractMessageRepository
    dialogs: AbstractDialogRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
