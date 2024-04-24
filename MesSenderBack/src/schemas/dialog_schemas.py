import enum
import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DialogViewStatus(str,enum.Enum):
    not_viewed = 'not_viewed',
    viewed = 'viewed',


class DialogDTO(BaseModel):
    id: int
    dialog_name: str
    view_status: DialogViewStatus
    last_message: str
    remote_uid: Optional[int] = None


class DialogCreateRespDTO(BaseModel):
    dialog_id: int
    first_message_id: int
    created_at: datetime.datetime

class DualDialogCreateReqDTO(BaseModel):
    remote_uid: int
    first_message: str = Field(min_length=1)

class DialogExistResDTO(BaseModel):
    is_exist: bool
    dialog_id: int | None = None
