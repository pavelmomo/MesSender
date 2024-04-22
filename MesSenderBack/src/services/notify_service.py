from fastapi import WebSocket
from schemas import PackageDTO
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
    def unregister(websocket: WebSocket, user_id: int):
        if (
            user_id not in NotifyService.connections
            or websocket not in NotifyService.connections[user_id]
        ):
            return
        NotifyService.connections[user_id].remove(websocket)
        if len(NotifyService.connections[user_id]) == 0:
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
                await i.send_json(package.json())

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
