import enum
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class Role(enum.Enum):
    user = 'user',
    moderator = 'moderator'


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[Role]
