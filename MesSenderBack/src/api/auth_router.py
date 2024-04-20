from fastapi import HTTPException, Response
from fastapi import APIRouter
from src.config import JWT_COOKIE_NAME
from src.api.dependencies import UOW
from src.schemas import UserCreateDTO, UserLoginDTO
from src.services import AuthService, UserAlreadyExist, UserNotExist, InvalidCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])  # создание роутера


@router.post("/register")
async def register(new_user: UserCreateDTO, uow: UOW):
    try:
        return await AuthService.register(new_user, uow)
    except UserAlreadyExist:
        return HTTPException(status_code=409, detail="User alrady exist")


@router.post("/login")
async def login(user: UserLoginDTO, uow: UOW, response: Response):
    try:
        token = await AuthService.login(user, uow)
        response.set_cookie(key=JWT_COOKIE_NAME, value=token)
        response.status_code = 204
        return response

    except (UserNotExist, InvalidCredentials):
        return HTTPException(status_code=401, detail="Invalid credentials")
