import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, WebSocket

from starlette.websockets import WebSocketDisconnect

from src.schemas import CommonStatusDTO, MessageCheckDTO, MessageCreateDTO, MessageDTO, PackageDTO, EventType
from src.services import MessageService, NotifyService, AuthServiceInstance

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
async def websocket_endpoint(websocket: WebSocket,
                             uow: UOW,
                             user_id: int = Depends(AuthServiceInstance.authorize_ws_endpoint)):
    if user_id == None:
        await websocket.close(code=401)
        return
    await NotifyService.register(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            res = await NotifyService.handle_user_package(PackageDTO.model_validate(data), uow, user_id)
            if res == False:
                NotifyService.unregister(websocket, user_id)
                await websocket.close(code=403)
    except WebSocketDisconnect:
        NotifyService.unregister(websocket, user_id)


