from typing import Annotated
from fastapi import Depends
from src.repositories import UnitOfWorkPgs, AbstractUOW
from src.services import DialogService

UOW = Annotated[AbstractUOW, Depends(UnitOfWorkPgs)]
