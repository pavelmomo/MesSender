from fastapi import APIRouter, Depends, HTTPException
from .dependencies import (UOW, Paginator, CurrentUser)
from src.services import DialogService, MessageService
from src.schemas import (DialogCreateRespDTO, CommonStatusDTO,
                         MessageCreateDTO, MessageDTO, UserRead, DialogDTO)


router = APIRouter(
    prefix="/api/dialogs",
    tags=["Dialogs"]
)  # создание роутера

@router.get("/", response_model=list[DialogDTO])  # получение списка диалогов пользователя
async def get_active_user_dialogs(uow: UOW, user: CurrentUser ,paginator: Paginator = Depends()):
    result = await DialogService.get_active_user_dialogs(uow, user.id, paginator.limit, paginator.offset)
    if result is None:
        raise HTTPException(status_code=403,detail="Incorrect parameters")
    return result

@router.post("/", response_model=DialogCreateRespDTO)  # создание диалога на 2 чел.
async def create_dialog(user: CurrentUser, remote_uid: int, uow: UOW):
    result = await DialogService.create_dual_dialog(uow, user.id, remote_uid)
    if result is None:
        raise HTTPException(status_code=403,detail="Incorrect parameters")
    return result


@router.post("/{id}/messages", response_model=CommonStatusDTO)  # отправка сообщения в диалог
async def send_message(id: int, message: MessageCreateDTO, uow: UOW, user: CurrentUser):
    message.dialog_id = id
    message.user_id = user.id
    result = await MessageService.send_message(uow, message)
    if result is None:
        raise HTTPException(status_code=403,detail="Incorrect parameters")
    return result


@router.get("/{id}/messages", response_model=list[MessageDTO])  # запрос сообщений из диалога
async def get_messages(id: int, user: CurrentUser, uow: UOW, paginator: Paginator = Depends()):
    result = await MessageService.get_dialog_messages(uow, id, user.id, paginator.limit, paginator.offset)
    if result is None:
        raise HTTPException(status_code=403,detail="Incorrect parameters")
    return result


@router.get("/uuu")
async def uuu(user: CurrentUser):
    return f"Привет!{user.username}"