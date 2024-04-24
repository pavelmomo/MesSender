from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, WebSocket

from starlette.websockets import WebSocketDisconnect
from api.dependencies import UOW, CurrentUser, Paginator
from api.auth_router import authorize_ws_endpoint
from schemas import (
    MessageCreateDTO,
    MessageDTO,
    PackageDTO,
    UserDTO,
)
from services import MessageService, NotifyService
from services.exceptions import AccessDenied


router = APIRouter(prefix="/api", tags=["Messages"])  # создание роутера


# эндпоинт отправки сообщений в диалогв, данный момент не используется
# по причине перевода отправки сообщений на ws эндпоинт, может быть резервным
@router.post("/dialogs/{id}/messages")
async def send_message(
    dialog_id: int, message: MessageCreateDTO, uow: UOW, user: CurrentUser
):
    try:
        message.dialog_id = dialog_id
        message.user_id = user.id
        return await MessageService.send_message(uow, message)

    except AccessDenied as e:
        raise HTTPException(status_code=403, detail="Access denied") from e


# эндпоинт получения сообщений из диалога
@router.get("/dialogs/{dialog_id}/messages", response_model=list[MessageDTO])
async def get_messages(
    dialog_id: int, user: CurrentUser, uow: UOW, paginator: Paginator = Depends()
):
    try:
        return await MessageService.get_dialog_messages(
            uow, dialog_id, user.id, paginator.limit, paginator.offset
        )
    except AccessDenied as e:
        raise HTTPException(status_code=403, detail="Access denied") from e


# эндпоинт Websocket, используется для отправки сообщений, а также для оповещения
# пользователей о новом сообщении иле смене его статуса
@router.websocket("/messages/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    uow: UOW,
    user: Annotated[UserDTO, Depends(authorize_ws_endpoint)],
):
    if user is None:
        await websocket.close(code=1008)
        return
    user_id = user.id
    try:
        await NotifyService.register(websocket, user_id)
        while True:
            data = await websocket.receive_json()
            await NotifyService.handle_user_package(
                PackageDTO.model_validate(data), uow, user_id
            )

    except AccessDenied:
        NotifyService.unregister(websocket, user_id)
        await websocket.close(code=403)

    except WebSocketDisconnect:
        NotifyService.unregister(websocket, user_id)

    except Exception as e:
        NotifyService.unregister(websocket, user_id)
        raise e
