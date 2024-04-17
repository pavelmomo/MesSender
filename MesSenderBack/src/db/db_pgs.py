from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


class DatabasePgs:
    engine: AsyncEngine
    session_factory: async_sessionmaker
    url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    @classmethod
    async def init_db(cls):
        DatabasePgs.engine = create_async_engine(url=DatabasePgs.url, echo=False)
        #await DatabasePgs.create_and_init_tables()
        DatabasePgs.session_factory = async_sessionmaker(
            DatabasePgs.engine, class_=AsyncSession, expire_on_commit=False
        )

    @classmethod
    async def create_and_init_tables(cls):
        from src.models import Base

        async with DatabasePgs.engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            # await conn.execute(
            #     insert(User),
            #     [
            #         {'username': "mark", 'email': 'mark@mail.ru', 'password_hash': 'kram', 'role': 'user'},
            #         {'username': "jack", 'email': 'jack@mail.ru', 'password_hash': 'kcaj', 'role': 'user'}
            #     ])
            await conn.commit()
