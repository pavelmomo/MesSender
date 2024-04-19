from fastapi import APIRouter
from src.schemas import UserReadShortDTO
from src.services import UserService
from .dependencies import UOW, CurrentUser

router = APIRouter(prefix="/api/users", tags=["Users"])  # создание роутера


@router.get("/all", response_model=list[UserReadShortDTO])
async def get_users_by_partly_username(uow: UOW, user: CurrentUser, username: str):
    return await UserService.get_users_by_partly_username(uow, username)
