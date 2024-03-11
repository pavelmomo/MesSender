from typing import List
from src.schemas.dialog_schemas import *
from src.repositories import AbstractUOW
from src.schemas.dialog_schemas import *


class DialogService:
    @classmethod
    async def get_user_dialogs(cls, uow: AbstractUOW, user_id: int) -> List[DialogDTO] | None:
        async with uow:
            dialogs = await uow.dialogs_dual.get_user_dialogs(user_id)
            dialogs_dto = []
            for dialog in dialogs:
                if dialog.first_user_id != user_id:
                    name = dialog.first_user.username
                else:
                    name = dialog.second_user.username
                dialogs_dto.append(DialogDTO(id=dialog.id,
                                             status=dialog.status,
                                             name=name))

            return dialogs_dto

    @classmethod
    async def create_dual_dialog(cls,uow: AbstractUOW, uid: int, remote_uid):
        ...