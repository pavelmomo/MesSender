from fastapi import APIRouter, Depends
from sqlalchemy import delete

from src.db.db_pgs import DatabasePgs
from .dependencies import (UOW, DialogService,
                           MessageService, Paginator)

from src.schemas import (DialogCreateRespDTO, CommonStatusDTO,
                         MessageCreateDTO, MessageDTO)
from ..models import Message

router = APIRouter(
    prefix="/api/messages",
    tags=["Messages"]
)   # создание роутера


@router.delete("/{id}")
async def delete_message(id: int):
    async with DatabasePgs.session_factory() as session:
        query = delete(Message).where(Message.id == id).returning(Message.id)
        result = await session.execute(query)
        result = result.scalars().one_or_none()
        await session.commit()
    return {'status': False if result is None else True}


