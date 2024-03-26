import datetime

from src.models import MessageStatus
from typing import Optional
from pydantic import BaseModel


class MessageCreateDTO(BaseModel):
    dialog_id: Optional[int] = None
    user_id: int
    text: str



class MessageDTO(BaseModel):
    id: int
    user_id: int
    text: str
    status: MessageStatus
    created_at: datetime.datetime

class MessageUpdateDTO(BaseModel):
    id: int
    text: str