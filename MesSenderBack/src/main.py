import uvicorn
from src.db.db_pgs import DatabasePgs
from fastapi import FastAPI
from api.routers import all_routers


app = FastAPI(title="Web Application")      #создание экземпляра приложения Fastapi
for router in all_routers:      #добавление всех роутеров
    app.include_router(router)

@app.on_event('startup')
async def database_init():
    await DatabasePgs.init_db()

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)    #запуск веб-сервера uvicorn


