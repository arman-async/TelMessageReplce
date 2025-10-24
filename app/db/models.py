from typing import NewType

from sqlalchemy import types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from . import enums

TEXT = NewType("TEXT", str)
INT = NewType("INT", int)

class Base(DeclarativeBase):
    type_annotation_map = {
        str: types.String(256),
        INT: types.BIGINT,
        TEXT: types.Text,
    }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


class ForcedSubscription(Base):
    __tablename__ = "forced_subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    channel_id: Mapped[str] = mapped_column(nullable=False)
    invite_link: Mapped[str] = mapped_column(nullable=False)


class MessageAction(Base):
    __tablename__ = "message_actions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    regex: Mapped[str] = mapped_column(nullable=False)
    acction: Mapped[enums.MessageActions] = mapped_column(nullable=False)
    message_replace: Mapped[TEXT] = mapped_column(nullable=True)


class ForcedJoinMessage(Base):
    __tablename__ = "forced_join_messages"
    chat_id: Mapped[INT] = mapped_column(nullable=False, primary_key=True)
    message_id : Mapped[INT] = mapped_column(nullable=False)
