from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel, Field
from models import User
from repositories import UnitOfWorkPgs, AbstractUOW


class Paginator(BaseModel):
    limit: Annotated[int, Field(ge=0)]
    offset: Annotated[int, Field(ge=0)]

    def __init__(self, limit: int = 30, offset: int = 0):
        super().__init__(limit=limit, offset=offset)


async def _get_uow():
    yield UnitOfWorkPgs()


UOW = Annotated[AbstractUOW, Depends(_get_uow)]

from api.auth_router import authorize_http_endpoint

CurrentUser = Annotated[User, Depends(authorize_http_endpoint)]
