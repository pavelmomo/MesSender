from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import UserReadShortDTO, UserDTO, UserUpdateDTO
from services import UserService, AuthService, UserAlreadyExist, InvalidCredentials
from api.auth_router import CurrentUser, CurrentAdmin
from api.dependencies import UOW, Paginator
from services.exceptions import IncorrectData, OperationNotPermitted

logger = getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["Users"])  # создание роутера


# эндпоинт получения объекта текущего пользователя
@router.get("/me", response_model=UserDTO)
async def get_current_user(current_user: CurrentUser):
    return current_user


# эндпоинт поиска пользователей по части username
@router.get("/search", response_model=list[UserReadShortDTO])
async def get_users_by_partly_username(user: CurrentUser, username: str, uow: UOW):
    return await UserService.get_users_by_partly_username(username, uow)


# эндпоинт получения списка всех пользователей
@router.get("/all", response_model=list[UserDTO])
async def get_all_users(user: CurrentAdmin, uow: UOW, paginator: Paginator = Depends()):
    return await UserService.get_all_users(paginator.limit, paginator.offset, uow)


# эндпоинт обовления данных аккаунта
@router.patch("/me")
async def update_current_user(update: UserUpdateDTO, user: CurrentUser, uow: UOW):
    try:
        await AuthService.update_user(update, user.id, uow)
        logger.info("User (id=%s) updated successfully", user.id)
        return Response(status_code=201)
    except UserAlreadyExist as e:
        logger.info(
            "User update operation rejected for User (id=%s): username or e-mail alrady exist",
            user.id,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or e-mail alrady exist",
        ) from e
    except InvalidCredentials as e:
        logger.info(
            "User update operation rejected for User (id=%s): invalid password",
            user.id,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        ) from e


@router.patch("/{id_to_block}")
async def ban_user(id_to_ban: int, is_banned: bool, user: CurrentAdmin, uow: UOW):
    try:

        await UserService.ban_user(id_to_ban, is_banned, uow)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IncorrectData as e:
        logger.info(
            "User ban operation rejected for User (id=%s): incorect data (id_to_ban=%s)",
            user.id,
            id_to_ban,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect data"
        ) from e
    except OperationNotPermitted as e:
        logger.info(
            "User ban operation rejected for User (id=%s): operation not permitted (id_to_ban=%s)",
            user.id,
            id_to_ban,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not permitted. You can not ban admins",
        ) from e
