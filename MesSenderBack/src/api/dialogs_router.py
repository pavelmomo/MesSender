from fastapi import APIRouter, Depends
from src.api.dependencies import (UOW, DialogService,
                                  MessageService, Paginator)

from src.schemas import (DialogCreateRespDTO, MessageCreateRespDTO,
                         MessageCreateDTO, MessageDTO)

router = APIRouter(
    prefix="/api/dialogs",
    tags=["Dialogs"]
)  # создание роутера


@router.get("/", response_model=int)  # получение id диалога по id участников
async def get_dialog_id(uid: int, remote_uid: int, uow: UOW):
    result = await DialogService.get_dual_dialog_id(uow, uid, remote_uid)
    return result


@router.post("/", response_model=DialogCreateRespDTO)  # создание диалога на 2 чел.
async def create_dialog(uid: int, remote_uid: int, uow: UOW):
    result = await DialogService.create_dual_dialog(uow, uid, remote_uid)
    return result


@router.post("/{id}/messages", response_model=MessageCreateRespDTO)  # отправка сообщения в диалог
async def send_message(id: int, message: MessageCreateDTO, uow: UOW):
    message.dialog_id = id
    result = await MessageService.send_message(uow, message)
    return result


@router.get("/{id}/messages", response_model=list[MessageDTO])  # запрос сообщений из диалога
async def get_messages(id: int, uow: UOW, paginator: Paginator = Depends()):
    result = await MessageService.get_dialog_messages(uow, id, paginator.limit, paginator.offset)
    return result
