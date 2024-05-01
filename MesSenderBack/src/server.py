from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers
from utils.middleware import ErrorHandlerMiddleware

app = FastAPI(
    title="Message Sender Application", debug=False
)  # создание экземпляра приложения Fastapi

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(  # разрешение ограничений CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in all_routers:  # добавление всех роутеров
    app.include_router(router)
