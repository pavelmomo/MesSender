import pytest

from repositories.abstract_repository import AbstractUOW
from sqlalchemy.exc import InterfaceError
from db.exceptions import DbConnectionError
from tests.stubs.repositories.dialog_repository import StubDialogRepository
from tests.stubs.repositories.message_repository import StubMessageRepository
from tests.stubs.repositories.user_repository import StubUserRepository


class StubUnitOfWork(AbstractUOW):
    def __init__(self):
        self.users = StubUserRepository()
        self.messages = StubMessageRepository()
        self.dialogs = StubDialogRepository()

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        if (
            exc_type is OSError
            or exc_type is ConnectionError
            or exc_type is InterfaceError
            or exc_type is ConnectionRefusedError
        ):
            raise DbConnectionError from exc
    async def commit(self):
        pass

    async def rollback(self):
        pass


@pytest.fixture(scope='class')
def uow():
    return StubUnitOfWork()
