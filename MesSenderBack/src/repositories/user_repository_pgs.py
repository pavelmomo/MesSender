from typing import Type, Optional

from fastapi_users.models import UP
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Dialog, User, DialogUser, Message
from sqlalchemy import insert, select, update, or_, and_, func
from . import AbstractUserRepository
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


class UserRepositoryPgs(AbstractUserRepository, SQLAlchemyUserDatabase):
    def __init__(self, session: AsyncSession):
        SQLAlchemyUserDatabase.__init__(self, session, User)
    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(User).where(User.username == username)
        return await self._get_user(statement)
    async def get_by_username_or_email(self, username: str, email: str) -> Optional[UP]:
        statement = select(User).where(or_(User.username == username, User.email == email))
        return await self._get_user(statement)
    async def check_user_existing(self, user_id: int) -> bool:
        result = await self.session.get(User, user_id)
        return False if result is None \
            else True

