import pytest

from models.user import User
from repositories.abstract_repository import AbstractUOW
from tests.stubs.repositories.unitofwork import uow
from services.user_service import UserService

class TestUserService:

    @pytest.fixture(scope='class', autouse=True)
    def fill_repository(self, uow):
        uow.users.users.append(User(id=1, 
                              username='test',
                              email='test@mail.ru',
                              password='P@ssw0rd',
                              is_banned = False))

    async def test_get_users_by_partly_username(self, uow: AbstractUOW):
        test_username = 'te'
        found_users = await UserService.get_users_by_partly_username(test_username,
                                                                     uow)
        assert found_users != None
        assert found_users[0].username == 'test'

    async def test_ban_user(self, uow: AbstractUOW):
        await UserService.ban_user(1, True, uow)
        banned_user = await uow.users.get_by_id(1)
        assert banned_user != None
        assert banned_user.is_banned == True

    async def test_get_all_users(self, uow: AbstractUOW):
        uow.users.users.append(User(id=2, 
                               username='test_testovich',
                               email='test1@mail.ru',
                               password='P@ssw0rd',
                               is_banned = False))
        
        recieved_users = await UserService.get_all_users(0,0,uow)
        expected_users = await uow.users.get_all(0,0)
        assert recieved_users != None and expected_users != None
        assert len(recieved_users) == len(expected_users)
