from typing import Optional
from pydantic import BaseModel


class CommonStatusDTO(BaseModel):
    success: bool
    id: Optional[int] = None
