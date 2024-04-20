from fastapi import HTTPException, Response, Request, WebSocket
from fastapi import APIRouter
from src.config import JWT_COOKIE_NAME
from src.api.dependencies import UOW
from src.schemas import UserCreateDTO, UserLoginDTO, UserDTO
from src.services import (
    AuthService,
    UserAlreadyExist,
    UserNotExist,
    InvalidCredentials,
    InvalidToken,
    TokenExpire,
)


router = APIRouter(prefix="/api/auth", tags=["Auth"])  # создание роутера


@router.post("/register")
async def register(new_user: UserCreateDTO, uow: UOW):
    try:
        return await AuthService.register(new_user, uow)
    except UserAlreadyExist:
        raise HTTPException(status_code=409, detail="User alrady exist")


@router.post("/login")
async def login(user: UserLoginDTO, uow: UOW, response: Response):
    try:
        token = await AuthService.login(user, uow)
        response.set_cookie(key=JWT_COOKIE_NAME, value=token)
        response.status_code = 204
        return response

    except (UserNotExist, InvalidCredentials):
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=JWT_COOKIE_NAME)
    response.status_code = 204
    return response


async def authorize_http_endpoint(request: Request, uow: UOW) -> UserDTO:
    if not JWT_COOKIE_NAME in request.cookies:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:

        return await AuthService.authorize(request.cookies[JWT_COOKIE_NAME], uow)

    except (InvalidToken, TokenExpire):
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

    except UserNotExist:
        raise HTTPException(status_code=401, detail="Token user not exist")


async def authorize_ws_endpoint(websocket: WebSocket, uow: UOW) -> UserDTO | None:
    if not JWT_COOKIE_NAME in websocket.cookies:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:

        return await AuthService.authorize(websocket.cookies[JWT_COOKIE_NAME], uow)

    except (InvalidToken, TokenExpire, UserNotExist):
        return None
