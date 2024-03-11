import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base
from sqlalchemy import ForeignKey


class DialogStatus(enum.Enum):
    not_viewed = 'not_viewed',
    viewed = 'viewed',
    deleted = 'hidden'


class Dialog(Base):
    __tablename__ = "dialogs"
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[list["Message"]] = relationship(back_populates="dialog")
    is_blocked: Mapped[bool] = mapped_column(default=False)


class DialogUser(Base):
    __tablename__ = "dialogs_users"
    dialog_id: Mapped[int] = mapped_column(
        ForeignKey("dialogs.id"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("dialogs.id"),
        primary_key=True
    )
    status: Mapped[DialogStatus]
