from repositories import AbstractUOW
from schemas import PackageDTO
from fastapi import WebSocket

class NotifyService:
    connections: dict[int, list[WebSocket]] = dict()

    @staticmethod
    async def register(websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in NotifyService.connections:
            NotifyService.connections[user_id] = [websocket]
        else:
            NotifyService.connections[user_id].append(websocket)

    @staticmethod
    def unregister(websocket: WebSocket, user_id: int):
        if (user_id not in NotifyService.connections
                or websocket not in NotifyService.connections[user_id]):
            return
        NotifyService.connections[user_id].remove(websocket)
        if len(NotifyService.connections[user_id]) == 0:
            del NotifyService.connections[user_id]

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

    @staticmethod
    async def handle_user_package(package: PackageDTO, uow : AbstractUOW, user_id: int) -> bool:
        from src.services import MessageService
        if package.event == 'send_message':
            package.data.user_id = user_id
            result = await MessageService.send_message(uow, package.data)
            if result is None:
                return False
        elif package.event == 'set_message_viewed':
            result = await MessageService.set_message_viewed(uow, package.data.message_ids,
                                                             package.data.dialog_id, user_id)
            return result
