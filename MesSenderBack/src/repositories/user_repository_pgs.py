import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, or_, and_
from models import User
from db.exceptions import IncorrectData
from . import AbstractUserRepository


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

    async def get_active_by_partly_username(self, username: str) -> list[User]:
        query = select(User).where(
            and_(User.username.contains(username), User.is_banned is False)
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_all(self, limit: int, offset: int) -> list[User]:
        query = select(User).offset(offset).limit(limit)
        result = await self.session.scalars(query)
        return result.all()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_user(self, update_dict: dict) -> None:
        try:
            await self.session.execute(update(User), [update_dict])
            await self.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            raise IncorrectData from e
