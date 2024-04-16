from src.repositories import AbstractUOW
from src.schemas import Package
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
    async def send_package(package: Package, user_ids: list[int]):
        for id in user_ids:
            for i in NotifyService.connections[id]:
                await i.send_json(package.json())
    @staticmethod
    async def handle_user_package(package: Package, uow : AbstractUOW, user_id: int) -> bool:
        from src.services import MessageService
        if package.event == 'send_message':
            package.data.user_id = user_id
            result = await MessageService.send_message(uow, package.data)
            if result is None:
                return False
