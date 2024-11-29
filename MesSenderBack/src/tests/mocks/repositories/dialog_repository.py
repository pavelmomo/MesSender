from itertools import islice
from typing import Sequence
from models.dialog import Dialog, DialogUser
from repositories.abstract_repository import AbstractDialogRepository


class MockDialogRepository(AbstractDialogRepository):
    def __init__(self):
        self.dialogs: list[Dialog] = []
        self.dialog_users: list[DialogUser]  = []

    async def get_active_user_dialogs(
        self, user_id: int, limit: int, offset: int
    ) -> Sequence[DialogUser]:
        pass

    async def get_dual_dialog_id(self, uid: int, remote_uid: int) -> int:
        pass

    async def create_dual_dialog(self, user_id: int, remote_user_id: int) -> int:
        pass

    async def get_dialog_users(self, dialog_id: int) -> list[int]:
        users_ids = []
        for dialog_user in self.dialog_users:
            if dialog_user.dialog_id == dialog_id:
                users_ids.append(dialog_user.user_id)
        return users_ids