from typing import Annotated
from fastapi import Depends
from src.repositories import UnitOfWorkPgs, AbstractUOW
from src.services import DialogService, MessageService

class Paginator:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit = limit
        self.offset = offset

UOW = Annotated[AbstractUOW, Depends(UnitOfWorkPgs)]


