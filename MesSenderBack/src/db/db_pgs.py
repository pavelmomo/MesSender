from sqlalchemy import insert
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.exc import InterfaceError
from db.exceptions import DbConnectionError
from sqlalchemy import text
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, ADMIN_PASS


class DatabasePgs:
    engine: AsyncEngine
    session_factory: async_sessionmaker
    url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    @staticmethod
    async def init_db():
        try:
            test_engine = create_async_engine(
                f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}",
                echo=False,
            )
            is_db_exist = await DatabasePgs.check_db_existing(test_engine)
            await test_engine.dispose()
            DatabasePgs.engine = create_async_engine(url=DatabasePgs.url, echo=False)
            if not is_db_exist:
                await DatabasePgs.create_and_init_tables(DatabasePgs.engine)

            DatabasePgs.session_factory = async_sessionmaker(
                DatabasePgs.engine, class_=AsyncSession, expire_on_commit=False
            )
        except (OSError, InterfaceError, ConnectionError, ConnectionRefusedError) as e:
            raise DbConnectionError from e

    @staticmethod
    async def create_and_init_tables(engine: AsyncEngine):
        from models import Base, User

        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(
                insert(User),
                [
                    {
                        "id": 1,
                        "username": "admin",
                        "email": "admin@example.com",
                        "password": ADMIN_PASS,
                        "role": "admin",
                    },
                ],
            )
            await conn.commit()

    @staticmethod
    async def check_db_existing(engine: AsyncEngine):
        async with engine.connect() as conn:
            res = await conn.execute(text("select datname from pg_database;"))
            exist_db = res.scalars().all()
            if DB_NAME not in exist_db:
                await conn.execute(text("commit"))
                await conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                return False
            return True
