from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from src.schemas import UserRead, UserCreate
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
    AuthServiceInstance.fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["Auth"],
)


@app.on_event("startup")
async def database_init():
    await DatabasePgs.init_db()


@app.get("/")
async def index():
    return RedirectResponse("/docs")
