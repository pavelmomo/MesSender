from . import MessageDTO, MessageCreateDTO
import enum
from pydantic import BaseModel

class SetMessageViewed(BaseModel):
    message_ids: list[int]
    dialog_id: int


class EventType(str,enum.Enum):
    send_message = 'send_message',
    set_message_viewed = 'set_message_viewed'


class Package(BaseModel):
    event: EventType
    data : MessageDTO | MessageCreateDTO | SetMessageViewed

