from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.schemas import UserReadDTO, UserCreateDTO, UserUpdateDTO
from src.api.routers import all_routers
from src.db.db_pgs import DatabasePgs
from src.services import AuthServiceInstance


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



app.include_router(
    AuthServiceInstance.fastapi_users.get_auth_router(AuthServiceInstance.auth_backend),
    prefix="/api/auth",
    tags=["Auth"]
)
app.include_router(
    AuthServiceInstance.fastapi_users.get_register_router(UserReadDTO, UserCreateDTO),
    prefix="/api/auth",
    tags=["Auth"],
)
app.include_router(
    AuthServiceInstance.fastapi_users.get_users_router(UserReadDTO,UserUpdateDTO),
    prefix="/api/users",
    tags=["Users"],
)   
app.mount("/", StaticFiles(directory="public", html=True))


@app.on_event("startup")
async def database_init():
    await DatabasePgs.init_db()
