from typing import List
from src.repositories import AbstractUOW
from src.schemas import (DialogDTO, DialogViewStatus,
                         DialogCreateRespDTO, CommonStatusDTO)
from src.models import MessageStatus


class DialogService:
    @classmethod
    async def get_active_user_dialogs(cls, uow: AbstractUOW, user_id: int, limit: int, offset: int) -> List[DialogDTO]:
        async with uow:
            user_check = await uow.users.check_user_existing(user_id)
            if not user_check:
                return []
            dialogs = await uow.dialogs.get_active_user_dialogs(user_id, limit, offset)
            dialogs_dto = []
            for d in dialogs:
                dialog_dict = {'id': d.dialog_id,
                               'dialog_name': '' if d.remote_user == None else d.remote_user.username,
                               'view_status': DialogViewStatus.viewed
                               if len(d.dialog.messages) == 0
                                  or d.dialog.messages[0].status == MessageStatus.viewed
                               else DialogViewStatus.not_viewed,
                               'last_message': '' if len(d.dialog.messages) == 0 else d.dialog.messages[0].text
                               }
                dialogs_dto.append(DialogDTO.model_validate(dialog_dict))

            return dialogs_dto

    @classmethod
    async def get_dual_dialog_id(cls, uow: AbstractUOW, uid: int, remote_uid: int) -> CommonStatusDTO:
        async with uow:
            result = await uow.dialogs.get_dual_dialog_id(uid, remote_uid)
            if result < 0:
                return CommonStatusDTO(success=False)
            return CommonStatusDTO(success=True, id=result)

    @classmethod
    async def hide_dialog(cls, dialog_id: int, user_id):
        raise NotImplementedError

    @classmethod
    async def unhide_dialog(cls, dialog_id: int, user_id):
        raise NotImplementedError

    @classmethod
    async def create_dual_dialog(cls, uow: AbstractUOW, uid: int, remote_uid: int) -> DialogCreateRespDTO:
        if (uid == remote_uid):
            return DialogCreateRespDTO(is_created=False)
        async with uow:
            uid_check = await uow.users.check_user_existing(uid)
            remote_uid_check = await uow.users.check_user_existing(remote_uid)
            if not (uid_check and remote_uid_check):
                return DialogCreateRespDTO(is_created=False)
            dialog_id = await uow.dialogs.get_dual_dialog_id(uid, remote_uid)
            if dialog_id == -1:
                result = await uow.dialogs.create_dual_dialog(uid, remote_uid)
                return DialogCreateRespDTO(is_created=True, dialog_id=result)

            return DialogCreateRespDTO(is_created=False)
