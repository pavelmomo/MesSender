from itertools import islice
from models.user import Role, User
from repositories.abstract_repository import AbstractUserRepository


class MockUserRepository(AbstractUserRepository):
    def __init__(self):
        self.users: list[User] = []

    async def get_by_id(self, user_id: int) -> User | None:
        search_user = None
        for user in self.users:
            if user.id == user_id:
                search_user = user
                break
        return search_user

    async def get_by_username(self, username: str) -> User | None:
        search_user = None
        for user in self.users:
            if user.username == username:
                search_user = user
                break
        return search_user

    async def get_by_username_or_email(self, username: str, email: str) -> User | None:
        search_user = None
        for user in self.users:
            if user.username == username or user.email == email:
                search_user = user
                break
        return search_user

    async def check_user_existing(self, user_id: int) -> bool:
        check = await self.get_by_id(user_id)
        return True if check else False

    async def get_active_by_partly_username(self, username: str) -> list[User]:
        search_users = []
        for user in self.users:
            if username in user.username and not user.is_banned:
                search_users.append(user)

        return search_users

    async def get_all(self, limit: int, offset: int) -> list[User]:
        sampled_users = list(islice(islice(self.users, offset, None), limit))
        return sampled_users

    async def create_user(self, user: User) -> User:
        new_id = 0
        if len(self.users) > 0:
            new_id = self.users[-1].id + 1
        user.id = new_id
        user.is_banned = False
        user.role = Role.user
        self.users.append(user)
        return user

    async def update_user(self, update_dict: dict) -> None:
        user_id = update_dict['id']
        index = None
        for ind, user in enumerate(self.users):
            if user.id == user_id:
                index = ind
        for key, val in update_dict.items():
            setattr(self.users[index], key, val)
            