from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers
from db.db_pgs import DatabasePgs


app = FastAPI(
    title="Web Application", debug=True
)  # создание экземпляра приложения Fastapi
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in all_routers:  # добавление всех роутеров
    app.include_router(router)


@app.on_event("startup")
async def database_init():
    await DatabasePgs.init_db()
