import datetime, enum
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class MessageStatus(str,enum.Enum):
    not_viewed = 'not_viewed',
    viewed = 'viewed'

class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc',now())"))
    status: Mapped[MessageStatus] = mapped_column(default=MessageStatus.not_viewed)
    dialog_id: Mapped[int] = mapped_column(ForeignKey("dialog.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    dialog: Mapped["Dialog"] = relationship(back_populates="messages")
    user: Mapped["User"] = relationship()