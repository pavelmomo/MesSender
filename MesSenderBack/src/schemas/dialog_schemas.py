import enum
from typing import Optional

from pydantic import BaseModel

class CreateStatus(str, enum.Enum):
    created = 'created'
    existed = 'existed'

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
    status: CreateStatus
    dialog_id: Optional[int] = None

class DualDialogCreateReqDTO(BaseModel):
    remote_uid: int