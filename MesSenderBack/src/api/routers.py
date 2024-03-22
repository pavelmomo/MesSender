from .users_router import router as users_router
from .dialogs_router import router as dialogs_router
from .messages_router import router as messanges_router

"""
Определим массив со всеми роутерами, для дальнейшего удобства их включения
"""

all_routers = [
    users_router,
    dialogs_router,
    messanges_router
]
