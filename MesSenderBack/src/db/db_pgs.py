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
        await DatabasePgs.create_tables()
        DatabasePgs.session_factory = async_sessionmaker(DatabasePgs.engine,
                                                         class_=AsyncSession,
                                                         expire_on_commit=False)

    @classmethod
    async def create_tables(cls):
        import src.models
        async with DatabasePgs.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
