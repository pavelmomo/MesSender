from abc import ABC, abstractmethod
from typing import Sequence
from src.models import Dialog, DialogUser, Message


class AbstractUserRepository(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def check_user_existing(self, user_id: int) -> bool:
        raise NotImplementedError


class AbstractDialogRepository(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def get_user_dialogs(self, user_id: int, limit: int, offset: int) -> Sequence[DialogUser]:
        raise NotImplementedError

    @abstractmethod
    async def get_dual_dialog_id(self, uid: int, remote_uid: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_dialog_user_existing(self, dialog_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def check_dialog_existing(self, dialog_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_dual_dialog(self, user_id: int, remote_user_id: int) -> int:
        raise NotImplementedError


class AbstractMessageRepository(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, message: Message) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_messages(self, dialog_id: int, limit: int, offset: int) -> Sequence[Message]:
        raise NotImplementedError


class AbstractUOW(ABC):
    users: AbstractUserRepository
    messages: AbstractMessageRepository
    dialogs: AbstractDialogRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
