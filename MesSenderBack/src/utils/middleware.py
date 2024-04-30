from logging import getLogger
from fastapi import Response

from db.db_pgs import DatabasePgs
from db.exceptions import DbConnectionError

logger = getLogger(__name__)


class ErrorHandlerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            await self.custom_lifespan(send)
        try:
            await self.app(scope, receive, send)
        except DbConnectionError:
            logger.error("Error connecting to DB.")
            if scope["type"] == "http":
                response = Response(status_code=500)
                await response(scope, receive, send)

    async def custom_lifespan(self, send):
        try:
            await DatabasePgs.init_db()  # инициализация БД при запуске
        except DbConnectionError:
            logger.error("Error when connecting to the DB for the first time.")
            await send({"type": "lifespan.startup.failed"})
