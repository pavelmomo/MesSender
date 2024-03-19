from src.db.db_pgs import DatabasePgs
from src.api.routers import all_routers
from fastapi import FastAPI

app = FastAPI(title="Web Application", debug=True)  # создание экземпляра приложения Fastapi
for router in all_routers:  # добавление всех роутеров
    app.include_router(router)


@app.on_event('startup')
async def database_init():
    await DatabasePgs.init_db()
