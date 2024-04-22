from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers
from db.db_pgs import DatabasePgs


app = FastAPI(
    title="Web Application", debug=True
)  # создание экземпляра приложения Fastapi


app.add_middleware(  # разрешение ограничений CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in all_routers:  # добавление всех роутеров
    app.include_router(router)


@app.on_event("startup")
async def database_init():  # инициализация БД при запуске
    await DatabasePgs.init_db()
