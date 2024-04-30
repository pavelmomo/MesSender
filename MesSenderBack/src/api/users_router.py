from logging import getLogger
from fastapi import APIRouter, HTTPException, Response, status
from schemas import UserReadShortDTO, UserDTO, UserUpdateDTO
from services import UserService, AuthService, UserAlreadyExist, InvalidCredentials
from api.auth_router import CurrentUser, CurrentAdmin
from api.dependencies import UOW

logger = getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["Users"])  # создание роутера


# эндпоинт получения объекта текущего пользователя
@router.get("/me", response_model=UserDTO)
async def get_current_user(current_user: CurrentUser):
    return current_user


# эндпоинт поиска пользователей по части username
@router.get("/all", response_model=list[UserReadShortDTO])
async def get_users_by_partly_username(user: CurrentUser, username: str, uow: UOW):
    return await UserService.get_users_by_partly_username(username, uow)


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
async def block_user(id_to_block: int, user: CurrentAdmin):
    pass
