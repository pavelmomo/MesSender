from sqlalchemy.ext.asyncio import (async_sessionmaker,
                                    create_async_engine,
                                    AsyncSession,
                                    AsyncEngine)
from src.config import (DB_HOST,
                      DB_PORT,
                      DB_NAME,
                      DB_USER,
                      DB_PASS)

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import insert


class Base(DeclarativeBase):
    pass


class DatabasePgs:
    engine: AsyncEngine
    session_factory: async_sessionmaker
    url = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # self.url = 'sqlite+aiosqlite:///db/messenger.db'
    @classmethod
    async def init_db(cls):
        DatabasePgs.engine = create_async_engine(
            url=DatabasePgs.url,
            echo=True
        )
        # await DatabasePgs.create_and_init_tables()
        DatabasePgs.session_factory = async_sessionmaker(DatabasePgs.engine,
                                                         class_=AsyncSession,
                                                         expire_on_commit=False)

    @classmethod
    async def create_and_init_tables(cls):
        from ..models import User, Dialog, DialogUser
        async with DatabasePgs.engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(
                insert(User),
                [
                    {'username': "mark", 'email': 'mark@mail.ru', 'password_hash': 'kram', 'role': 'user'},
                    {'username': "jack", 'email': 'jack@mail.ru', 'password_hash': 'kcaj', 'role': 'user'}
                ])
            # await conn.execute(
            #     insert(Dialog),
            #     [{'id': 1}]
            # )
            # await conn.execute(
            #     insert(DialogUser),
            #     [
            #         {'dialog_id': 1, 'user_id': 2, 'remote_uid': 1 },
            #         {'dialog_id': 1, 'user_id': 1, 'remote_uid': 2  }
            #     ]
            # )
            await conn.commit()
