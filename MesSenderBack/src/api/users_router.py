from fastapi import APIRouter, Depends
from src.schemas import DialogDTO, UserRead
from src.services import DialogService
from .dependencies import UOW, Paginator, CurrentUser

router = APIRouter(prefix="/api/users", tags=["Users"])  # создание роутера


@router.get(
    "/current", response_model=UserRead
)  # получение списка диалогов пользователя
async def get_current_user(current_user: CurrentUser):
    return UserRead.from_orm(current_user)
