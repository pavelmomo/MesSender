from fastapi import APIRouter, Depends
from sqlalchemy import delete, update

from src.db.db_pgs import DatabasePgs
from .dependencies import UOW, Paginator, CurrentUser
from src.services import DialogService, MessageService

from src.schemas import (
    DialogCreateRespDTO,
    CommonStatusDTO,
    MessageCreateDTO,
    MessageDTO,
    MessageUpdateDTO,
)
from src.models import Message

router = APIRouter(prefix="/api/messages", tags=["Messages"])  # создание роутера
