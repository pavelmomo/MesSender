from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Message
from sqlalchemy import select
from . import AbstractMessageRepository


class MessageRepositoryPgs(AbstractMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_message(self, message: Message) -> int:
        self.session.add(message)
        await self.session.commit()
        return message.id

    async def get_messages(self, dialog_id: int, limit: int, offset: int) -> Sequence[Message]:
        query = (select(Message)
                 .filter(Message.dialog_id == dialog_id)
                 .limit(limit)
                 .offset(offset))
        messages = await self.session.execute(query)
        return messages.scalars().all()