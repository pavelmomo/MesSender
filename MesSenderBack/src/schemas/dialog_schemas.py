import enum
from typing import Optional

from pydantic import BaseModel


class DialogViewStatus(enum.Enum):
    not_viewed = 'not_viewed',
    viewed = 'viewed',


class DialogDTO(BaseModel):
    id: int
    dialog_name: str
    view_status: DialogViewStatus
    last_message: str


class DialogCreateRespDTO(BaseModel):
    is_created: bool
    dialog_id: Optional[int] = None
