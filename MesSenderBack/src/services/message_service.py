from src.repositories import AbstractUOW
from src.models import MessageStatus, Message
from src.schemas import (MessageCreateDTO, CommonStatusDTO,
                         MessageDTO, MessageCheckDTO)


class MessageService:
    @staticmethod
    async def send_message(uow: AbstractUOW, message: MessageCreateDTO) -> CommonStatusDTO | None:
        message_to_send = Message(dialog_id=message.dialog_id,
                                  user_id=message.user_id,
                                  text=message.text)
        async with uow:
            ids_list = await uow.dialogs.get_dialog_users(message.dialog_id)
            if message.user_id not in ids_list:
                return None
            message_id = await uow.messages.send_message(message_to_send)

            #отправка в вебсокет сообщения активному пользователю

            return CommonStatusDTO(success=True, id=message_id)


    @staticmethod
    async def get_dialog_messages(uow: AbstractUOW, dialog_id: int, user_id: int,
                                  limit: int, offset: int) -> list[MessageDTO] | None:
        async with uow:
            messages = await uow.messages.get_messages(dialog_id, user_id, limit, offset)
            messages_dto = [MessageDTO.model_validate(m, from_attributes=True) for m in messages[::-1]]
            return messages_dto

    @staticmethod
    async def get_last_message_datetime(uow: AbstractUOW, user_id : int) -> MessageCheckDTO | None:
        async with uow:
            result = await uow.messages.get_last_message_datetime(user_id)
            if not result:
                return MessageCheckDTO(has_messages=False)

            return MessageCheckDTO(has_messages=True, last_message_datetime=result)