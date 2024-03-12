from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Dialog, User, DialogUser, Message
from sqlalchemy import insert, select, update, or_, and_
from . import AbstractUserRepository


class UserRepositoryPgs(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_user_existing(self, user_id: int) -> bool:
        result = await self.session.get(User, user_id)
        if result is None:
            return False
        else:
            return True
