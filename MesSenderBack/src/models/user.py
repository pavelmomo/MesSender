import enum

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from . import Base, DialogUser


class Role(enum.Enum):
    user = 'user',
    moderator = 'moderator'


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=20), unique=True, index=True, nullable=False)
    role: Mapped[Role] = mapped_column(default='user')
    email: Mapped[str] = mapped_column(
        String(length=30), unique=True, index=True, nullable=False
    )



