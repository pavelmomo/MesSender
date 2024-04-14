import datetime

from src.models import MessageStatus
from typing import Optional
from pydantic import BaseModel, Field


class MessageCreateDTO(BaseModel):
    dialog_id: Optional[int] = None
    user_id: Optional[int] = None
    text: str = Field(max_length=500)



class MessageDTO(BaseModel):
    id: int
    dialog_id: int
    user_id: int
    text: str
    status: MessageStatus
    created_at: datetime.datetime

class MessageCheckDTO(BaseModel):
    has_messages: bool
    last_message_datetime: Optional[datetime.datetime] = None