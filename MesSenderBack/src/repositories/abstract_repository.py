from abc import ABC, abstractmethod
from typing import Sequence
from src.models import Dialog



class AbstractUserRepository(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError


class AbstractDialogRepository(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def get_user_dialogs(self, user_id: int)-> Sequence[Dialog]:
        raise NotImplementedError

    @abstractmethod
    async def create_pair_dialog(self, user_id: int, remote_user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete_user_dialog(self, dialog_id: int, user_id: int):
        raise NotImplementedError


class AbstractMessageRepository(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError


class AbstractUOW(ABC):
    users: AbstractUserRepository
    messages: AbstractMessageRepository
    dialogs_dual: AbstractDialogRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    def __aexit__(self,*args):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
