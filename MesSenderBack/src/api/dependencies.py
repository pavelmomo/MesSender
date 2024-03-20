from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel, Field

from src.repositories import UnitOfWorkPgs, AbstractUOW
from src.services import DialogService, MessageService


class Paginator(BaseModel):
    limit: Annotated[int, Field(ge=0)]
    offset: Annotated[int, Field(ge=0)]

    def __init__(self, limit: int = 10, offset: int = 0):
        super().__init__(limit=limit, offset=offset)


UOW = Annotated[AbstractUOW, Depends(UnitOfWorkPgs)]
