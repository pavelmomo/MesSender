from fastapi import APIRouter, Depends
from src.schemas import DialogDTO
from src.api.dependencies import (UOW,
                                  DialogService,
                                  Paginator)

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)  # создание роутера


@router.get("/{id}/dialogs", response_model=list[DialogDTO])  # получение списка диалогов пользователя
async def get_user_dialogs(id: int, uow: UOW, paginator: Paginator = Depends()):
    result = await DialogService.get_user_dialogs(uow, id, paginator.limit, paginator.offset)
    return result
