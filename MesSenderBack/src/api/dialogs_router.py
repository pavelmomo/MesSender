from fastapi import APIRouter, Depends, HTTPException

from schemas import DialogCreateRespDTO, DialogDTO, DualDialogCreateReqDTO
from services import DialogService
from services.exceptions import IncorrectData

from api.dependencies import UOW, CurrentUser, Paginator

router = APIRouter(prefix="/api/dialogs", tags=["Dialogs"])  # создание роутера

# эндпоинт получения списка диалогов пользователя
@router.get(
    "/", response_model=list[DialogDTO]
)  
async def get_active_user_dialogs(
    uow: UOW, user: CurrentUser, paginator: Paginator = Depends()
):
    return await DialogService.get_active_user_dialogs(
        uow, user.id, paginator.limit, paginator.offset
    )

# эндпоинт создания диалога (на 2 чел)
@router.post("/dual", response_model=DialogCreateRespDTO)
async def create_dual_dialog(
    user: CurrentUser, dialog_create: DualDialogCreateReqDTO, uow: UOW
):
    try:
        return await DialogService.create_dual_dialog(
            uow, user.id, dialog_create.remote_uid
        )
    except IncorrectData as e:
        raise HTTPException(status_code=400, detail="Incorrect parameters") from e
