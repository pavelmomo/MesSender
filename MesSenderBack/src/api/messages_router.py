import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, WebSocket

from starlette.websockets import WebSocketDisconnect
from api.auth_router import authorize_ws_endpoint
from schemas import (
    CommonStatusDTO,
    MessageCreateDTO,
    MessageDTO,
    PackageDTO,
    UserDTO,
)
from services import MessageService, NotifyService

from .dependencies import UOW, CurrentUser, Paginator

router = APIRouter(prefix="/api", tags=["Messages"])  # создание роутера


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


@router.websocket("/messages/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    uow: UOW,
    user: Annotated[UserDTO, Depends(authorize_ws_endpoint)],
):
    if user is None:
        await websocket.close(code=401)
        return
    user_id = user.id
    await NotifyService.register(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            res = await NotifyService.handle_user_package(
                PackageDTO.model_validate(data), uow, user_id
            )
            if res is False:
                NotifyService.unregister(websocket, user_id)
                await websocket.close(code=403)
    except WebSocketDisconnect:
        NotifyService.unregister(websocket, user_id)
