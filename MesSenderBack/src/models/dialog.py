import enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from . import Base, User


class DialogStatus(enum.Enum):
    default = 'default',
    hidden = 'hidden'


class DialogUser(Base):
    __tablename__ = "dialogs_users"
    dialog_id: Mapped[int] = mapped_column(
        ForeignKey("dialogs.id"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    remote_uid: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id")
    )
    status: Mapped["DialogStatus"] = mapped_column(
        default=DialogStatus.default
    )
    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id]
    )
    remote_user: Mapped["User"] = relationship(
        "User", foreign_keys=[remote_uid]
    )
    dialog: Mapped["Dialog"] = relationship(
        "Dialog", back_populates="users"
    )


class Dialog(Base):
    __tablename__ = "dialogs"
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[list["Message"]] = relationship(back_populates="dialog")
    is_multiply: Mapped[bool] = mapped_column(default=False)
    users: Mapped[list["DialogUser"]] = relationship(
        'DialogUser', back_populates='dialog'
    )
