import pytest

from models.user import Role, User
from repositories.abstract_repository import AbstractUOW
from schemas.user_schemas import UserCreateDTO, UserLoginDTO
from tests.stubs.repositories.unitofwork import uow
from services.auth_service import AuthService

class TestAuthService:

    @pytest.fixture(scope='class', autouse=True)
    def fill_repository(self, uow):
        uow.users.users.append(User(id=1, 
                              username='test',
                              email='test@mail.ru',
                              password='$2b$12$LiK.Aij0y6/lR4dcMk2QuOXbd4khAvw8NZR3bOpFYg3f.782MIS5.',
                              is_banned = False,
                              role=Role.user))

    async def test_register(self, uow: AbstractUOW):
        new_user = UserCreateDTO(username='new_user',
                                 email='new_user@example.com',
                                 password='P@ssw0rd')
        await AuthService.register(new_user, uow)
        found_user = None
        for user in uow.users.users:
            if user.username == new_user.username:
                found_user = user

        assert found_user != None

    async def test_login_and_authorize(self, uow):
        user = UserLoginDTO(username='test', password='P@ssw0rd')
        jwt_token = await AuthService.login(user, uow)
        assert jwt_token != None
        authorized_user = await AuthService.authorize(jwt_token, uow)
        assert authorized_user != None
        assert authorized_user.username == 'test'