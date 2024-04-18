from src.api.users_router import router as users_router
from src.api.dialogs_router import router as dialogs_router
from src.api.messages_router import router as messages_router

"""
Определим массив со всеми роутерами, для дальнейшего удобства их включения
"""

all_routers = [users_router, dialogs_router, messages_router]
