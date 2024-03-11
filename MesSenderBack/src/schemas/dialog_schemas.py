import enum
from src.models import DialogStatus
from pydantic import BaseModel, Field


class DialogAddDTO(BaseModel):
    current_user_id: int
    remote_user_id: int

class DialogDTO(BaseModel):
    id: int
    name: str
    status: DialogStatus
