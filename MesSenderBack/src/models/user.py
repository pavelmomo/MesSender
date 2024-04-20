import enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class Role(str, enum.Enum):
    user = ("user",)
    moderator = "moderator"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(length=20), unique=True, nullable=False
    )
    role: Mapped[Role] = mapped_column(default="user")
    email: Mapped[str] = mapped_column(String(length=30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column()
