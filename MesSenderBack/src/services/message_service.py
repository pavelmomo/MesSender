from src.repositories import AbstractUOW
from src.models import Message
from src.schemas import (MessageCreateDTO, CommonStatusDTO,
                         MessageDTO, Package, EventType, SetMessageViewed)
from . import NotifyService


class MessageService:
    @staticmethod
    async def send_message(uow: AbstractUOW, message: MessageCreateDTO) -> CommonStatusDTO | None:
        message_to_send = Message(dialog_id=message.dialog_id,
                                  user_id=message.user_id,
                                  text=message.text)
        async with uow:
            user_ids_list = await uow.dialogs.get_dialog_users(message.dialog_id)
            if message_to_send.user_id not in user_ids_list:
                return None
            message_id = await uow.messages.send_message(message_to_send)

            pack_to_send = Package(event = EventType.send_message,
                                   data = MessageDTO.model_validate(message_to_send, from_attributes=True))

            await NotifyService.send_package(pack_to_send, user_ids_list)
            return CommonStatusDTO(success=True, id=message_id)


    @staticmethod
    async def get_dialog_messages(uow: AbstractUOW, dialog_id: int, user_id: int,
                                  limit: int, offset: int) -> list[MessageDTO] | None:
        async with uow:

            user_ids_list = await uow.dialogs.get_dialog_users(dialog_id)
            if user_id not in user_ids_list:
                return None

            messages, changed_status_msg_ids = await uow.messages.get_messages(dialog_id, user_id, limit, offset)
            if (len(changed_status_msg_ids) > 0):
                user_ids_list.remove(user_id)
                pack_to_send = Package(event=EventType.set_message_viewed,
                                       data= SetMessageViewed(dialog_id=dialog_id,
                                                              message_ids=changed_status_msg_ids))
                await NotifyService.send_package(pack_to_send, user_ids_list)
            messages_dto = [MessageDTO.model_validate(m, from_attributes=True) for m in messages[::-1]]
            return messages_dto

    @staticmethod
    async def set_message_viewed(uow: AbstractUOW, ids: list[int], dialog_id: int, user_id: int) -> bool:
        async with uow:
            user_ids_list = await uow.dialogs.get_dialog_users(dialog_id)
            if user_id not in user_ids_list:
                return False
            await uow.messages.set_viewed_status(ids, dialog_id)
            pack_to_send = Package(event=EventType.set_message_viewed,
                                   data=SetMessageViewed(dialog_id=dialog_id,
                                                         message_ids=ids))
            await NotifyService.send_package(pack_to_send, user_ids_list)
            return True

