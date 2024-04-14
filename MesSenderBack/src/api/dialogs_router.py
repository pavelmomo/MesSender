from fastapi import APIRouter, Depends, HTTPException

from src.schemas import DialogCreateRespDTO, DialogDTO
from src.services import DialogService

from .dependencies import UOW, CurrentUser, Paginator

router = APIRouter(prefix="/api/dialogs", tags=["Dialogs"])  # создание роутера


@router.get(
    "/", response_model=list[DialogDTO]
)  # получение списка диалогов пользователя
async def get_active_user_dialogs(
    uow: UOW, user: CurrentUser, paginator: Paginator = Depends()
):
    result = await DialogService.get_active_user_dialogs(
        uow, user.id, paginator.limit, paginator.offset
    )
    if result is None:
        raise HTTPException(status_code=403, detail="Incorrect parameters")
    return result


@router.post("/dual", response_model=DialogCreateRespDTO)  # создание диалога на 2 чел.
async def create_dual_dialog(user: CurrentUser, remote_uid: int, uow: UOW):
    result = await DialogService.create_dual_dialog(uow, user.id, remote_uid)
    if result is None:
        raise HTTPException(status_code=403, detail="Incorrect parameters")
    return result


@router.get("/uuu")
async def uuu(user: CurrentUser):
    return f"Привет!{user.username}"
