from fastapi import APIRouter, HTTPException, Response
from schemas import UserReadShortDTO, UserDTO, UserUpdateDTO
from services import UserService, AuthService, UserAlreadyExist, InvalidCredentials
from api.dependencies import UOW, CurrentUser

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
        return Response(status_code=201)
    except UserAlreadyExist as e:
        raise HTTPException(
            status_code=409, detail="User with this username or e-mail alrady exist"
        ) from e
    except InvalidCredentials as e:
        raise HTTPException(status_code=401, detail="Invalid password") from e
