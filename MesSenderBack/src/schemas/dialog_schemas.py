import enum
from typing import Optional

from pydantic import BaseModel

class CreateStatus(enum.Enum):
    created = 'created'
    existed = 'existed'

class DialogViewStatus(enum.Enum):
    not_viewed = 'not_viewed',
    viewed = 'viewed',


class DialogDTO(BaseModel):
    id: int
    dialog_name: str
    view_status: DialogViewStatus
    last_message: str


class DialogCreateRespDTO(BaseModel):
    status: CreateStatus
    dialog_id: Optional[int] = None
