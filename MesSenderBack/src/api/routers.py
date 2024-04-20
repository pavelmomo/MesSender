from api.users_router import router as users_router
from api.dialogs_router import router as dialogs_router
from api.messages_router import router as messages_router
from api.auth_router import router as auth_router

"""
Определим массив со всеми роутерами, для дальнейшего удобства их включения
"""

all_routers = [users_router, dialogs_router, messages_router, auth_router]
