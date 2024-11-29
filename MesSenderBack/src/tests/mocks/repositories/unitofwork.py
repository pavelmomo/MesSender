import pytest

from repositories.abstract_repository import AbstractUOW
from sqlalchemy.exc import InterfaceError
from db.exceptions import DbConnectionError
from tests.mocks.repositories.dialog_repository import MockDialogRepository
from tests.mocks.repositories.message_repository import MockMessageRepository
from tests.mocks.repositories.user_repository import MockUserRepository


class MockUnitOfWork(AbstractUOW):
    def __init__(self):
        self.users = MockUserRepository()
        self.messages = MockMessageRepository()
        self.dialogs = MockDialogRepository()

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
    return MockUnitOfWork()
