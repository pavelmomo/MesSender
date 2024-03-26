from fastapi import APIRouter, Depends
from sqlalchemy import delete, update

from src.db.db_pgs import DatabasePgs
from .dependencies import (UOW, DialogService,
                           MessageService, Paginator)

from src.schemas import (DialogCreateRespDTO, CommonStatusDTO,
                         MessageCreateDTO, MessageDTO, MessageUpdateDTO)
from src.models import Message

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

@router.post("/")
async def create_message(message: MessageCreateDTO):
    async with DatabasePgs.session_factory() as session:
        mes = Message(user_id = message.user_id,
                            text = message.text,
                            dialog_id= message.dialog_id)
        session.add(mes)
        await session.commit()

    return {'status': False if mes.id is None else True,
            'id': mes.id,
            'created_at': mes.created_at}

@router.put("/")
async def update_message(message: MessageUpdateDTO):
    async with DatabasePgs.session_factory() as session:

        query = (update(Message)
                 .where(Message.id == message.id)
                 .values(text = message.text)
                 .returning(Message.id))

        mes_id = await session.execute(query)
        await session.commit()

    return {'status': True if mes_id is not None else False }
