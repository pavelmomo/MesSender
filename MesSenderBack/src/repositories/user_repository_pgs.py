from typing import Type, Optional

from fastapi_users.models import UP
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Dialog, User, DialogUser, Message
from sqlalchemy import insert, select, update, or_, and_, func
from . import AbstractUserRepository
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


class UserRepositoryPgs(AbstractUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        return await self.session.scalar(query)

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return await self.session.scalar(query)

    async def get_by_username_or_email(self, username: str, email: str) -> User | None:
        query = (
            select(User)
            .where(or_(User.username == username, User.email == email))
            .limit(1)
        )
        return await self.session.scalar(query)

    async def check_user_existing(self, user_id: int) -> bool:
        result = await self.session.get(User, user_id)
        return False if result is None else True

    async def get_by_partly_username(self, username: str) -> list[User]:
        query = select(User).where(User.username.contains(username))
        result = await self.session.scalars(query)
        return result.all()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user
