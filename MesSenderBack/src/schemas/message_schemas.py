import datetime

from src.models import MessageStatus
from typing import Optional
from pydantic import BaseModel


class MessageCreateDTO(BaseModel):
    dialog_id: Optional[int] = None
    user_id: int
    text: str

class MessageCreateRespDTO(BaseModel):
    success: bool
    message_id: Optional[int] = None


class MessageDTO(BaseModel):
    id: int
    user_id: int
    text: str
    status: MessageStatus
    created_at: datetime.datetime