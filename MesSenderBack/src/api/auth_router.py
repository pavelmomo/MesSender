from logging import getLogger
from typing import Annotated
from fastapi import (
    Depends,
    HTTPException,
    Response,
    Request,
    WebSocket,
    APIRouter,
    status,
)
from config import JWT_COOKIE_NAME, JWT_EXPIRATION_TIME
from api.dependencies import UOW
from schemas import UserCreateDTO, UserLoginDTO, UserDTO
from services import AuthService
from services.exceptions import (
    UserAlreadyExist,
    UserNotExist,
    InvalidCredentials,
    TokenExpire,
    InvalidToken,
    UserIsBanned,
)

logger = getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Auth"])  # создание роутера


# эндпоинт регистрации
@router.post("/register", response_model=UserDTO)
async def register(new_user: UserCreateDTO, uow: UOW):
    try:
        result_user = await AuthService.register(new_user, uow)
        logger.info(
            "User (id=%s,username=%s) has successfully registered",
            result_user.id,
            result_user.username,
        )
        return result_user
    except UserAlreadyExist as e:
        logger.info(
            "Registration rejected: User with the same cridentials (username=%s,email=%s) already exist",
            new_user.username,
            new_user.email,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist"
        ) from e


# эндпоинт входа в аккаунт
@router.post("/login")
async def login(user: UserLoginDTO, uow: UOW, response: Response):
    try:
        token = await AuthService.login(user, uow)
        logger.info("User (username=%s) has successfully logged in", user.username)
        response.set_cookie(
            key=JWT_COOKIE_NAME, value=token, max_age=JWT_EXPIRATION_TIME
        )
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    except (UserNotExist, InvalidCredentials) as e:
        logger.info(
            "Login operation rejected: Invalid cridentials (username=%s)", user.username
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        ) from e
    except UserIsBanned as e:
        logger.info(
            "Login operation rejected: User (username=%s) is banned", user.username
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user is banned"
        ) from e


# эндпоинт выхода из аккаунта
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=JWT_COOKIE_NAME)
    response.status_code = status.HTTP_204_NO_CONTENT
    logger.info("Logout operation success")
    return response


# метод авторизации эндпоинта http, используется при помощи Depends
async def authorize_http_endpoint(request: Request, uow: UOW) -> UserDTO:
    if not JWT_COOKIE_NAME in request.cookies:
        logger.info("HTTP authorization rejected: cookies is empty")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        user = await AuthService.authorize(request.cookies[JWT_COOKIE_NAME], uow)
        logger.debug(
            "HTTP authorization success: User (username=%s) is verified", user.username
        )
        return user

    except (InvalidToken, TokenExpire) as e:
        logger.warning("HTTP authorization rejected: Token is invalid or expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
        ) from e

    except UserNotExist as e:
        logger.warning("HTTP authorization rejected: Token user not exist")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token user not exist"
        ) from e

    except UserIsBanned as e:
        logger.info("HTTP authorization rejected: The user is banned")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user is banned"
        ) from e


# метод авторизации эндпоинта ws, используется при помощи Depends
async def authorize_ws_endpoint(websocket: WebSocket, uow: UOW) -> UserDTO | None:
    if not JWT_COOKIE_NAME in websocket.cookies:
        logger.info("WS authorization rejected: cookies is empty")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
    try:
        user = await AuthService.authorize(websocket.cookies[JWT_COOKIE_NAME], uow)
        return user

    except (InvalidToken, TokenExpire, UserNotExist, UserIsBanned):
        logger.info("WS authorization rejected: invalid cridentials")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None


async def authorize_http_admin(
    user: Annotated[UserDTO, Depends(authorize_http_endpoint)]
):
    if user.role != "admin":
        logger.info(
            "Authorization rejected: User (username=%s) is not administrator",
            user.username,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not an administrator"
        )
    return user


CurrentUser = Annotated[UserDTO, Depends(authorize_http_endpoint)]
CurrentAdmin = Annotated[UserDTO, Depends(authorize_http_admin)]
