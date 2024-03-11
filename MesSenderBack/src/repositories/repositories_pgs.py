from typing import Sequence
from src.db.db_pgs import DatabasePgs
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Dialog, User
from sqlalchemy import insert, select, update, or_
from sqlalchemy.orm import joinedload
from . import (AbstractUserRepository,
               AbstractDialogRepository,
               AbstractMessageRepository,
               AbstractUOW)
from src.models.dialog import DialogStatus


class UserRepositoryPgs(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


class DialogRepositoryPgs(AbstractDialogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_dialogs(self, user_id: int) -> Sequence[Dialog]:
        query = (select(Dialog)
                 .where(or_ (Dialog.first_user_id == user_id,
                             Dialog.second_user_id == user_id))
                 .options(joinedload(Dialog.first_user)
                          , joinedload(Dialog.second_user))
                 )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_pair_dialog(self, user_id: int, remote_user_id: int):
        raise NotImplementedError

    async def delete_user_dialog(self, dialog_id: int, user_id: int):
        raise NotImplementedError


class MessageRepositoryPgs(AbstractMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


class UnitOfWorkPgs(AbstractUOW):

    def __init__(self):
        self.session_factory = DatabasePgs.session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepositoryPgs(self.session)
        self.dialogs_dual = DialogRepositoryPgs(self.session)
        self.messages = MessageRepositoryPgs(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
