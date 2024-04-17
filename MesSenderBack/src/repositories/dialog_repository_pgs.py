from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Dialog, User, DialogUser, Message
from sqlalchemy import insert, select, update, or_, and_
from sqlalchemy.orm import joinedload, contains_eager
from . import AbstractDialogRepository


class DialogRepositoryPgs(AbstractDialogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_user_dialogs(self, user_id: int, limit: int, offset: int) -> Sequence[DialogUser]:
        subquery = (select(Message.id)
                     .filter(and_(Message.dialog_id == Dialog.id, Message.created_at > DialogUser.border_date))
                     .order_by(Message.created_at.desc())
                     .limit(1)
                     .scalar_subquery()
                     .correlate(Dialog, DialogUser)
                     )
        query = (select(DialogUser)
                 .join(DialogUser.dialog)
                 .filter(DialogUser.user_id == user_id)
                 .join(Message, Message.id == subquery)  # замена с outerjoin, вывод только диалогов с посл. сообщением
                 .outerjoin(User, User.id == DialogUser.remote_user_id)
                 .options(contains_eager(DialogUser.remote_user))
                 .options(contains_eager(DialogUser.dialog,
                                         Dialog.messages))
                 .order_by(Message.created_at.desc())
                 .limit(limit)
                 .offset(offset)
                 )

        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def get_dual_dialog_id(self, uid: int, remote_uid: int) -> int:

        query = (select(DialogUser)
                 .filter(and_(DialogUser.user_id == uid,
                              DialogUser.remote_user_id == remote_uid,
                              Dialog.is_multiply == False))
                 .limit(1)
                 )
        result = await self.session.execute(query)
        result = result.scalars().one_or_none()
        return -1 if result is None \
            else result.dialog_id

    async def create_dual_dialog(self, user_id: int, remote_user_id: int) -> int:
        new_dialog = Dialog()
        self.session.add(new_dialog)
        await self.session.flush()
        new_dialog_users = [DialogUser(dialog_id=new_dialog.id,
                                       user_id=user_id,
                                       remote_user_id=remote_user_id),
                            DialogUser(dialog_id=new_dialog.id,
                                       user_id=remote_user_id,
                                       remote_user_id=user_id)
                            ]
        self.session.add_all(new_dialog_users)
        await self.session.commit()
        return new_dialog.id

    async def get_dialog_users(self, dialog_id: int) -> list[int]:
        query = (select(DialogUser.user_id)
                 .filter(DialogUser.dialog_id == dialog_id))
        users = await self.session.scalars(query)
        users = users.all()
        return users
