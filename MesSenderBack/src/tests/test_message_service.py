from datetime import datetime

import pytest

from models.dialog import Dialog, DialogUser
from models.message import Message, MessageStatus
from models.user import User
from repositories.abstract_repository import AbstractUOW
from schemas.message_schemas import MessageCreateDTO
from tests.stubs.repositories.unitofwork import uow
from services.message_service import MessageService

class TestMessageService:
    default_message = Message(id=1, 
                              text='Hello from test',
                              created_at=datetime.now(),
                              dialog_id = 1,
                              user_id = 1,
                              status = MessageStatus.not_viewed)
    
    @pytest.fixture(scope='class', autouse=True)
    def fill_repository(self, uow):
        uow.users.users.append(User(id=1, 
                              username='test_1',
                              email='test1@mail.ru',
                              password='P@ssw0rd',
                              is_banned = False))
        uow.users.users.append(User(id=2, 
                              username='test_2',
                              email='test2@mail.ru',
                              password='P@ssw0rd',
                              is_banned = False))
        uow.dialogs.dialogs.append(Dialog(id=1, 
                                          is_multiply=False))
        uow.dialogs.dialog_users.append(DialogUser(dialog_id=1, 
                                                   user_id=1,
                                                   remote_user_id=2,
                                                   border_date=datetime.fromisoformat("1970-01-01T00:00:00+00:00")))
        uow.dialogs.dialog_users.append(DialogUser(dialog_id=1, 
                                                   user_id=2,
                                                   remote_user_id=1,
                                                   border_date=datetime.fromisoformat("1970-01-01T00:00:00+00:00")))


    async def test_send_message(self, uow: AbstractUOW):
        all_messages_old, _ = await uow.messages.get_messages(1, 1, 100, 0)
        new_message = MessageCreateDTO(dialog_id=1,
                                       user_id=1,
                                       text="Это будет новое сообщение 1 польз.")
        await MessageService.send_message(uow, new_message)
        all_messages, _ = await uow.messages.get_messages(1, 1, 100, 0)
        assert all_messages != None
        assert (len(all_messages) - len(all_messages_old)) == 1

    async def test_set_message_viewed(self, uow: AbstractUOW):
        uow.messages.messages.append(Message(id=2, 
                                             text='Сообщение для проверки статуса',
                                             status= MessageStatus.not_viewed,
                                             created_at=datetime.now(),
                                             dialog_id=1,
                                             user_id=1))
        
        await MessageService.set_message_viewed(uow, [2], 1, 1)
        all_messages, _ = await uow.messages.get_messages(1, 1, 100, 0)
        assert all_messages != None
        index = -1
        for i, message in enumerate(all_messages):
            if message.id == 2:
                index = i
        assert index > -1
        assert all_messages[index].status == MessageStatus.viewed
        