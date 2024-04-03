from src.repositories import AbstractUOW
from src.models import MessageStatus, Message
from src.schemas import (MessageCreateDTO, CommonStatusDTO,
                         MessageDTO)


class MessageService:
    @staticmethod
    async def send_message(uow: AbstractUOW, message: MessageCreateDTO) -> CommonStatusDTO | None:
        message_to_send = Message(dialog_id=message.dialog_id,
                                  user_id=message.user_id,
                                  text=message.text)
        async with uow:
            result = await uow.dialogs.check_dialog_user_existing(message.dialog_id,
                                                                  message.user_id)
            if not result:
                return None
            message_id = await uow.messages.send_message(message_to_send)
            return CommonStatusDTO(success=True, id=message_id)

    @staticmethod
    async def get_dialog_messages(uow: AbstractUOW, dialog_id: int, user_id: int,
                                  limit: int, offset: int) -> list[MessageDTO] | None:
        async with uow:
            # check_dialog = await uow.dialogs.check_dialog_user_existing(dialog_id, user_id)
            # if not check_dialog:
            #     return None
            messages = await uow.messages.get_messages(dialog_id, user_id, limit, offset)
            messages_dto = [MessageDTO.model_validate(m, from_attributes=True) for m in messages[::-1]]
            return messages_dto
