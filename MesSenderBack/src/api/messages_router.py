from fastapi import APIRouter, Depends, HTTPException

from src.schemas import CommonStatusDTO, MessageCheckDTO, MessageCreateDTO, MessageDTO
from src.services import MessageService

from .dependencies import UOW, CurrentUser, Paginator

router = APIRouter(prefix="/api", tags=["Messages"])  # создание роутера


@router.get(
    "/messages/check", response_model=MessageCheckDTO
)  # получение списка диалогов пользователя
async def get_last_message_datetime(current_user: CurrentUser, uow: UOW):
    result = await MessageService.get_last_message_datetime(uow, current_user.id)
    if result is None:
        raise HTTPException(status_code=403, detail="Incorrect parameters")
    return result


@router.post(
    "/dialogs/{id}/messages", response_model=CommonStatusDTO
)  # отправка сообщения в диалог
async def send_message(id: int, message: MessageCreateDTO, uow: UOW, user: CurrentUser):
    message.dialog_id = id
    message.user_id = user.id
    result = await MessageService.send_message(uow, message)
    if result is None:
        raise HTTPException(status_code=403, detail="Incorrect parameters")
    return result


@router.get(
    "/dialogs/{id}/messages", response_model=list[MessageDTO]
)  # запрос сообщений из диалога
async def get_messages(
    id: int, user: CurrentUser, uow: UOW, paginator: Paginator = Depends()
):
    result = await MessageService.get_dialog_messages(
        uow, id, user.id, paginator.limit, paginator.offset
    )
    if result is None:
        raise HTTPException(status_code=403, detail="Incorrect parameters")
    return result
