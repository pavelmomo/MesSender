import datetime
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from src.models import Message, MessageStatus, Dialog, DialogUser, User
from sqlalchemy import select, update, and_, text
from . import AbstractMessageRepository


class MessageRepositoryPgs(AbstractMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_message(self, message: Message) -> int:
        self.session.add(message)
        await self.session.commit()
        return message.id

    async def get_messages(self, dialog_id: int, user_id: int,
                           limit: int, offset: int) -> Sequence[Message]:
        query = (select(Message)
                 .join(Dialog, Message.dialog_id == dialog_id)
                 .join(DialogUser, and_(DialogUser.user_id == user_id, DialogUser.dialog_id == Dialog.id))
                 .filter(and_(Message.dialog_id == dialog_id, Message.created_at > DialogUser.border_date))
                 .order_by(Message.created_at.desc())
                 .limit(limit)
                 .offset(offset))
        messages = await self.session.execute(query)
        messages = messages.unique().scalars().all()
        for message in messages:
            if message.status == MessageStatus.not_viewed and message.user_id != user_id:
                message.status = MessageStatus.viewed
        await self.session.commit()
        return messages

    async def get_last_message_datetime(self, user_id: int) -> datetime.datetime | None:
        query = \
        """select m.created_at  from messages m 
            inner join dialogs d on m.dialog_id = d.id
            inner join dialogs_users du on d.id = du.dialog_id
                where du.user_id = :uid
                order by m.created_at desc 
                limit 1
        """
        dateTime = await self.session.scalar(text(query), { 'uid': user_id })
        return dateTime