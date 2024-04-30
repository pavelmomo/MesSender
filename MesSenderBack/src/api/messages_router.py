from logging import getLogger
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status

from starlette.websockets import WebSocketDisconnect
from api.auth_router import CurrentUser
from api.dependencies import UOW, Paginator
from api.auth_router import authorize_ws_endpoint
from schemas import (
    MessageCreateDTO,
    MessageDTO,
    PackageDTO,
    UserDTO,
)
from services import MessageService, NotifyService
from services.exceptions import AccessDenied

logger = getLogger(__name__)
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
        logger.warning(
            "Message send operation rejected: Access denied (user_id=%s,dialog_id=%s)",
            user.id,
            dialog_id,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        ) from e


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
        logger.warning(
            "Get messages operation rejected: Access denied (user_id=%s,dialog_id=%s)",
            user.id,
            dialog_id,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        ) from e


# эндпоинт Websocket, используется для отправки сообщений, а также для оповещения
# пользователей о новом сообщении иле смене его статуса
@router.websocket("/messages/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    uow: UOW,
    user: Annotated[UserDTO, Depends(authorize_ws_endpoint)],
):
    if user is None:
        return
    user_id = user.id
    try:
        await NotifyService.register(websocket, user_id)
        logger.info(
            "WS messages endpoint: User (username=%s) successfully connected", user.username
        )
        while True:
            data = await websocket.receive_json()
            await NotifyService.handle_user_package(
                PackageDTO.model_validate(data), uow, user_id
            )

    except AccessDenied:
        logger.warning(
            "WS messages endpoint: Access for User (id=%s) denied, disconnect... ", user.id
        )
        NotifyService.unregister(websocket, user_id)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    except WebSocketDisconnect:
        logger.info("WS messages endpoint: User (username=%s) disconnect", user.username)
        NotifyService.unregister(websocket, user_id)

    except Exception as e:
        NotifyService.unregister(websocket, user_id)
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        raise e
