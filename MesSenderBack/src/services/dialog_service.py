from typing import List
from repositories import AbstractUOW
from repositories.exceptions import IncorrectData as IncorrectDataRepo
from schemas import (
    DialogDTO,
    DialogViewStatus,
    DialogCreateRespDTO,
)
from models import MessageStatus
from .exceptions import IncorrectData as IncorrectDataService


class DialogService:
    """
    Сервис выполняет бизнес-логику по работе с диалогами
    """

    # метод получения диалогов пользователя
    @staticmethod
    async def get_active_user_dialogs(
        uow: AbstractUOW, user_id: int, limit: int, offset: int
    ) -> List[DialogDTO]:
        async with uow:
            dialogs = await uow.dialogs.get_active_user_dialogs(user_id, limit, offset)
            dialogs_dto = []
            for d in dialogs:
                dialog_dict = {
                    "id": d.dialog_id,
                    "dialog_name": (
                        "" if d.remote_user is None else d.remote_user.username
                    ),
                    "view_status": (
                        DialogViewStatus.viewed
                        if len(d.dialog.messages) == 0
                        or d.dialog.messages[0].user_id == user_id
                        or d.dialog.messages[0].status == MessageStatus.viewed
                        else DialogViewStatus.not_viewed
                    ),
                    "last_message": (
                        "" if len(d.dialog.messages) == 0 else d.dialog.messages[0].text
                    ),
                    "remote_uid": None if d.remote_user is None else d.remote_user.id,
                }
                dialogs_dto.append(DialogDTO.model_validate(dialog_dict))

            return dialogs_dto

    @staticmethod
    async def hide_dialog(dialog_id: int, user_id):
        raise NotImplementedError

    # метод создания нового диалога (в случае отсутствия)
    @staticmethod
    async def create_dual_dialog(
        uow: AbstractUOW, uid: int, remote_uid: int
    ) -> DialogCreateRespDTO:
        if uid == remote_uid:
            raise IncorrectDataService
        try:
            async with uow:
                dialog_id = await uow.dialogs.get_dual_dialog_id(uid, remote_uid)
                if dialog_id == -1:  # создаём новый диалог
                    result = await uow.dialogs.create_dual_dialog(uid, remote_uid)
                    return DialogCreateRespDTO(status="created", dialog_id=result)
                else:
                    return DialogCreateRespDTO(status="existed", dialog_id=dialog_id)
        except IncorrectDataRepo as e:
            raise IncorrectDataService from e
