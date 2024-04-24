from db.db_pgs import DatabasePgs
from . import AbstractUOW, MessageRepositoryPgs, UserRepositoryPgs, DialogRepositoryPgs


class UnitOfWorkPgs(AbstractUOW):

    def __init__(self):
        self.session_factory = DatabasePgs.session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepositoryPgs(self.session)
        self.messages = MessageRepositoryPgs(self.session)
        self.dialogs = DialogRepositoryPgs(self.session)

    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
