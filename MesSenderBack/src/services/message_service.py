from repositories import AbstractUOW
from models import Message
from schemas import (
    MessageCreateDTO,
    MessageDTO,
)
from services.exceptions import AccessDenied
from . import NotifyService


class MessageService:
    """
    Сервис выполняет бизнес-логику работы с сообщениями
    """

    # метод отправки сообщения
    @staticmethod
    async def send_message(uow: AbstractUOW, message: MessageCreateDTO) -> int:
        message_to_send = Message(
            dialog_id=message.dialog_id, user_id=message.user_id, text=message.text
        )
        async with uow:
            user_ids_list = await uow.dialogs.get_dialog_users(message.dialog_id)
            if message_to_send.user_id not in user_ids_list:
                raise AccessDenied
            message_id = await uow.messages.send_message(message_to_send)
            message_dto = MessageDTO.model_validate(
                message_to_send, from_attributes=True
            )

            await NotifyService.notify_about_message(message_dto, user_ids_list)
            return message_id

    # метод получения сообщений диалога
    @staticmethod
    async def get_dialog_messages(
        uow: AbstractUOW, dialog_id: int, user_id: int, limit: int, offset: int
    ) -> list[MessageDTO]:
        async with uow:

            user_ids = await uow.dialogs.get_dialog_users(dialog_id)
            if user_id not in user_ids:
                raise AccessDenied

            messages, changed_status_msg_ids = await uow.messages.get_messages(
                dialog_id, user_id, limit, offset
            )
            if len(changed_status_msg_ids) > 0:
                user_ids.remove(user_id)
                await NotifyService.notify_about_message_status(
                    dialog_id, changed_status_msg_ids, user_ids
                )

            messages_dto = [
                MessageDTO.model_validate(m, from_attributes=True)
                for m in messages[::-1]
            ]
            return messages_dto

    # метод изменения статуса прочтения сообщения
    @staticmethod
    async def set_message_viewed(
        uow: AbstractUOW, message_ids: list[int], dialog_id: int, user_id: int
    ):
        async with uow:
            user_ids = await uow.dialogs.get_dialog_users(dialog_id)
            if user_id not in user_ids:
                raise AccessDenied
            await uow.messages.set_viewed_status(message_ids, dialog_id)
            await NotifyService.notify_about_message_status(
                dialog_id, message_ids, user_ids
            )
