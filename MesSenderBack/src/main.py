import uvicorn
from src.db.db_pgs import DatabasePgs
from api.routers import all_routers
from fastapi import FastAPI

app = FastAPI(title="Web Application", debug=True)  # создание экземпляра приложения Fastapi
for router in all_routers:  # добавление всех роутеров
    app.include_router(router)


@app.on_event('startup')
async def database_init():
    await DatabasePgs.init_db()


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)  # запуск веб-сервера uvicorn
