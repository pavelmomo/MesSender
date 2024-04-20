import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from . import Base


class DialogUser(Base):
    __tablename__ = "dialog_user"
    dialog_id: Mapped[int] = mapped_column(
        ForeignKey("dialog.id"),
        primary_key=True
    )
    border_date : Mapped[datetime.datetime] \
        = mapped_column(server_default=text("TIMEZONE('utc',now())"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        primary_key=True
    )
    remote_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user.id")
    )
    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id]
    )
    remote_user: Mapped["User"] = relationship(
        "User", foreign_keys=[remote_user_id]
    )
    dialog: Mapped["Dialog"] = relationship(
        "Dialog", back_populates="users"
    )



class Dialog(Base):
    __tablename__ = "dialog"
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[list["Message"]] = relationship(back_populates="dialog")
    is_multiply: Mapped[bool] = mapped_column(default=False)
    users: Mapped[list["DialogUser"]] = relationship(
        'DialogUser', back_populates='dialog'
    )
