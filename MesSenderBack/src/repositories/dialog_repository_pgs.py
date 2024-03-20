from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Dialog, User, DialogUser, Message
from sqlalchemy import insert, select, update, or_, and_
from sqlalchemy.orm import joinedload, contains_eager
from . import AbstractDialogRepository
from src.models import DialogStatus


class DialogRepositoryPgs(AbstractDialogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_dialogs(self, user_id: int, limit: int, offset: int) -> Sequence[DialogUser]:
        subquery = (select(Message.id)
                    .filter(Message.dialog_id == Dialog.id)
                    .order_by(Message.created_at.desc())
                    .limit(1)
                    .scalar_subquery()
                    .correlate(Dialog)
                    )
        query = (select(DialogUser)
                 .join(DialogUser.dialog)
                 .filter(and_(Dialog.is_multiply == False,
                              DialogUser.user_id == user_id,
                              DialogUser.status == DialogStatus.default))
                 .outerjoin(Message, Message.id == subquery)
                 .outerjoin(User, User.id == DialogUser.remote_uid)
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
                              DialogUser.remote_uid == remote_uid))
                 .limit(1)
                 )
        result = await self.session.execute(query)
        result = result.scalars().first()
        return -1 if result is None \
            else result.dialog_id


    async def check_dialog_user_existing(self, dialog_id: int, user_id: int) -> bool:
        query = (select(DialogUser)
                 .filter(and_(DialogUser.user_id == user_id,
                              DialogUser.dialog_id == dialog_id))
                 .limit(1)
                 )
        result = await self.session.execute(query)
        result = result.scalars().all()
        return False if len(result) == 0 \
            else True


    async def check_dialog_existing(self, dialog_id: int) -> bool:
        dialog = await self.session.get(Dialog,dialog_id)
        return False if dialog is None \
            else True


    async def create_dual_dialog(self, user_id: int, remote_user_id: int) -> int:
        new_dialog = Dialog()
        self.session.add(new_dialog)
        await self.session.flush()
        new_dialog_users = [DialogUser(dialog_id=new_dialog.id,
                                       user_id=user_id,
                                       remote_uid=remote_user_id),
                            DialogUser(dialog_id=new_dialog.id,
                                       user_id=remote_user_id,
                                       remote_uid=user_id)
                            ]
        self.session.add_all(new_dialog_users)
        await self.session.commit()
        return new_dialog.id
