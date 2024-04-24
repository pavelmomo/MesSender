from fastapi import HTTPException, Response, Request, WebSocket
from fastapi import APIRouter
from config import JWT_COOKIE_NAME
from api.dependencies import UOW
from schemas import UserCreateDTO, UserLoginDTO, UserDTO
from services import AuthService
from services.exceptions import (
    UserAlreadyExist,
    UserNotExist,
    InvalidCredentials,
    TokenExpire,
    InvalidToken,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])  # создание роутера


# эндпоинт регистрации
@router.post("/register", response_model=UserDTO)
async def register(new_user: UserCreateDTO, uow: UOW):
    try:
        return await AuthService.register(new_user, uow)
    except UserAlreadyExist as e:
        raise HTTPException(status_code=409, detail="User alrady exist") from e


# эндпоинт входа в аккаунт
@router.post("/login")
async def login(user: UserLoginDTO, uow: UOW, response: Response):
    try:
        token = await AuthService.login(user, uow)
        response.set_cookie(key=JWT_COOKIE_NAME, value=token)
        response.status_code = 204
        return response

    except (UserNotExist, InvalidCredentials) as e:
        raise HTTPException(status_code=401, detail="Invalid credentials") from e


# эндпоинт выхода из аккаунта
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=JWT_COOKIE_NAME)
    response.status_code = 204
    return response


# метод авторизации эндпоинта http, используется при помощи Depends
async def authorize_http_endpoint(request: Request, uow: UOW) -> UserDTO:
    if not JWT_COOKIE_NAME in request.cookies:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:

        return await AuthService.authorize(request.cookies[JWT_COOKIE_NAME], uow)

    except (InvalidToken, TokenExpire) as e:
        raise HTTPException(
            status_code=401, detail="Token is invalid or expired"
        ) from e

    except UserNotExist as e:
        raise HTTPException(status_code=401, detail="Token user not exist") from e


# метод авторизации эндпоинта ws, используется при помощи Depends
async def authorize_ws_endpoint(websocket: WebSocket, uow: UOW) -> UserDTO | None:
    if not JWT_COOKIE_NAME in websocket.cookies:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:

        return await AuthService.authorize(websocket.cookies[JWT_COOKIE_NAME], uow)

    except (InvalidToken, TokenExpire, UserNotExist):
        return None
