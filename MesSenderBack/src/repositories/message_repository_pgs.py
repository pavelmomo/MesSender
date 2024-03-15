from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Message, MessageStatus, Dialog
from sqlalchemy import select, update
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
                 .filter(Message.dialog_id == dialog_id)
                 .order_by(Message.created_at.desc())
                 .limit(limit)
                 .offset(offset))
        messages = await self.session.execute(query)
        messages = messages.scalars().all()
        for message in messages:
            if message.status == MessageStatus.not_viewed and message.user_id != user_id:
                message.status = MessageStatus.viewed
        await self.session.commit()

        return messages
