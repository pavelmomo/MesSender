from sqlalchemy import create_engine, insert, Engine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy import text
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, MODERATOR_PASS


class DatabasePgs:
    engine: AsyncEngine
    session_factory: async_sessionmaker
    url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    @staticmethod
    async def init_db():
        sync_engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}")
        is_db_exist = DatabasePgs.check_db_existing(sync_engine)
        sync_engine.dispose()
        DatabasePgs.engine = create_async_engine(url=DatabasePgs.url, echo=False)
        if not is_db_exist:
            await DatabasePgs.create_and_init_tables(DatabasePgs.engine)
        DatabasePgs.session_factory = async_sessionmaker(
            DatabasePgs.engine, class_=AsyncSession, expire_on_commit=False
        )

    @staticmethod
    async def create_and_init_tables(engine: AsyncEngine):
        from src.models import Base, User
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(
                insert(User),
                [
                    {
                        "username": "moderator",
                        "email": "moderator@example.com",
                        "password": MODERATOR_PASS,
                        "role": "moderator",
                    },
                ],
            )
            await conn.commit()

    @staticmethod
    def check_db_existing(engine: Engine):
        with engine.connect() as conn:
            res = conn.execute(text("select datname from pg_database;"))
            exist_db = res.scalars().all()
            if DB_NAME not in exist_db:
                conn.execute(text("commit"))
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                return False
            return True