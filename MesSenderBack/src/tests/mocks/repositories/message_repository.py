from itertools import islice
from datetime import datetime, timezone

from models.message import Message, MessageStatus
from repositories.abstract_repository import AbstractMessageRepository


class MockMessageRepository(AbstractMessageRepository):
    def __init__(self):
        self.messages: list[Message] = []
        
    async def send_message(self, message: Message) -> int:
        last_id = -1
        if len(self.messages) > 0:
            last_id = self.messages[-1].id
        message.id = last_id + 1
        self.messages.append(message)
        message.created_at = datetime.now(timezone.utc)
        message.status = MessageStatus.not_viewed
        return message.id

    async def get_messages(self, dialog_id: int, user_id: int, limit: int, offset: int) -> tuple[list[Message], list[int]]:
        search_messages = []
        for message in self.messages:
            if message.dialog_id == dialog_id:
                search_messages.append(message)

        search_messages = list(islice(islice(search_messages, offset, None), limit))
        changed_status_msg_ids: list[int] = []
        for message in search_messages:
            if message.status == MessageStatus.not_viewed and message.user_id != user_id:
                changed_status_msg_ids.append(message.id)
                message.status = MessageStatus.viewed
        
        return search_messages, changed_status_msg_ids

    async def set_viewed_status(self, ids: list[int], dialog_id: int):
        for message in self.messages:
            if message.id in ids and message.dialog_id == dialog_id:
                message.status = MessageStatus.viewed
