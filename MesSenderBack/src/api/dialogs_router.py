from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    DialogCreateRespDTO,
    DialogDTO,
    DualDialogCreateReqDTO,
    DialogExistResDTO,
)
from services import DialogService
from services.exceptions import IncorrectData
from api.auth_router import CurrentUser
from api.dependencies import (
    UOW,
    Paginator,
)

logger = getLogger(__name__)
router = APIRouter(prefix="/api/dialogs", tags=["Dialogs"])  # создание роутера


# эндпоинт получения списка диалогов пользователя
@router.get("/", response_model=list[DialogDTO])
async def get_active_user_dialogs(
    uow: UOW, user: CurrentUser, paginator: Paginator = Depends()
):
    dialogs = await DialogService.get_active_user_dialogs(
        uow, user.id, paginator.limit, paginator.offset
    )
    return dialogs


# эндпоинт проверки наличия диалогов между пользователями
@router.post("/dual/check", response_model=DialogExistResDTO)
async def check_dual_dialogs_existing(remote_uid: int, uow: UOW, user: CurrentUser):
    stat = await DialogService.check_dual_dialogs_existing(user.id, remote_uid, uow)
    
    return stat


# эндпоинт создания диалога (на 2 чел)
@router.post("/dual", response_model=DialogCreateRespDTO)
async def create_dual_dialog(
    user: CurrentUser, dialog_create: DualDialogCreateReqDTO, uow: UOW
):
    try:
        stat = await DialogService.create_dual_dialog(uow, user.id, dialog_create)
        logger.info(
            "Dialog (id=%s) with users (id=%s;id=%s) created successfully",
            stat.dialog_id,
            user.id,
            dialog_create.remote_uid,
        )
        return stat

    except IncorrectData as e:
        logger.info(
            "Dialog create operation with users (id=%s;id=%s) rejected: incorrect parameters",
            user.id,
            dialog_create.remote_uid,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect parameters"
        ) from e
