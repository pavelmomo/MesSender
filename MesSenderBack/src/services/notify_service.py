from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from schemas import PackageDTO, MessageDTO, EventType, SetMessageViewedDTO
from repositories import AbstractUOW


class NotifyService:
    """
    Сервис выполняет функции 'горячего' оповещения пользователей о новых сообщениях,
    а также об изменении статуса прочтения текущих сообщений.
    Регистрирует и контролирует текущие подключения по Websocket

    """

    connections: dict[int, list[WebSocket]] = dict()

    # метод регистрации на оповещения
    # выполняется при входе пользователя на вкладку 'Диалоги'
    @staticmethod
    async def register(websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in NotifyService.connections:
            NotifyService.connections[user_id] = [websocket]
        else:
            NotifyService.connections[user_id].append(websocket)

    # метод отключения от оповещений
    @staticmethod
    async def unregister(websocket: WebSocket, user_id: int, status_code: int = 1000):
        if (
            user_id not in NotifyService.connections
            or websocket not in NotifyService.connections[user_id]
        ):
            return
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close(status_code)
        NotifyService.connections[user_id].remove(websocket)
        if len(NotifyService.connections[user_id]) == 0:
            del NotifyService.connections[user_id]

    # метод отключения от оповещений всех устройств пользователя с опред. id
    @staticmethod
    async def unregister_by_id(user_id: int, status_code: int = 1008):
        if user_id not in NotifyService.connections:
            return
        for item in NotifyService.connections[user_id]:
            if item.client_state == WebSocketState.CONNECTED:
                await item.close(status_code)

        del NotifyService.connections[user_id]


    # метод отправки 'пакета' по Websocket
    @staticmethod
    async def send_package(package: PackageDTO, user_ids: list[int]):
        if len(user_ids) == 0:
            return
        joined_ids: list = list()
        for i in user_ids:
            if i in NotifyService.connections:
                joined_ids.append(i)
        for id in joined_ids:
            for i in NotifyService.connections[id]:
                try:
                    await i.send_json(package.json())
                except WebSocketDisconnect:
                    await NotifyService.unregister(i, id)

    # метод обработки пакетов пользователя по Websocket
    @staticmethod
    async def handle_user_package(
        package: PackageDTO, uow: AbstractUOW, user_id: int
    ) -> bool:
        from services import MessageService

        if package.event == "send_message":
            package.data.user_id = user_id
            await MessageService.send_message(uow, package.data)
        elif package.event == "set_message_viewed":
            await MessageService.set_message_viewed(
                uow, package.data.message_ids, package.data.dialog_id, user_id
            )

    @staticmethod
    async def notify_about_message(message: MessageDTO, user_ids: list[int]):
        pack_to_send = PackageDTO(event=EventType.send_message, data=message)
        await NotifyService.send_package(pack_to_send, user_ids)

    @staticmethod
    async def notify_about_message_status(
        dialog_id: int, message_ids: list[int], user_ids: list[int]
    ):
        pack_to_send = PackageDTO(
            event=EventType.set_message_viewed,
            data=SetMessageViewedDTO(dialog_id=dialog_id, message_ids=message_ids),
        )

        await NotifyService.send_package(pack_to_send, user_ids)
