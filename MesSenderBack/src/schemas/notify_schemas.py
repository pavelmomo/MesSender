import enum
from pydantic import BaseModel
from . import MessageDTO, MessageCreateDTO

class SetMessageViewedDTO(BaseModel):
    message_ids: list[int]
    dialog_id: int


class EventType(str,enum.Enum):
    send_message = 'send_message',
    set_message_viewed = 'set_message_viewed'


class PackageDTO(BaseModel):
    event: EventType
    data : MessageDTO | MessageCreateDTO | SetMessageViewedDTO

