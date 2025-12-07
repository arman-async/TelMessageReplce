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


class ForcedJoinMessage(Base):
    __tablename__ = "forced_join_messages"
    chat_id: Mapped[INT] = mapped_column(nullable=False, primary_key=True)
    message_id: Mapped[INT] = mapped_column(nullable=False)


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class MessageAction(Base):
    __tablename__ = "message_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    regex: Mapped[str] = mapped_column(nullable=False)
    action: Mapped[enums.MessageActions] = mapped_column(nullable=False)
    message_replace: Mapped[TEXT] = mapped_column(nullable=True)
    entities: Mapped[TEXT | None] = mapped_column(nullable=True)
    inline_keyboard_json: Mapped[TEXT | None] = mapped_column(
        nullable=True, default=None
    )
    run_after_join_check: Mapped[bool] = mapped_column(nullable=False, default=False)
    max_total_uses: Mapped[int | None] = mapped_column(nullable=True, default=None)
    max_uses_per_user: Mapped[int | None] = mapped_column(nullable=True, default=None)

    # # Relationship
    # user_usages: Mapped[list["MessageActionUserUsage"]] = relationship(
    #     back_populates="message_action", cascade="all, delete-orphan"
    # )


class MessageActionUserUsage(Base):
    __tablename__ = "message_action_user_uses"

    id: Mapped[int] = mapped_column(primary_key=True)

    message_action_id: Mapped[int] = mapped_column(nullable=False)
    # message_action_id: Mapped[int] = mapped_column(
    #     ForeignKey("message_actions.id"), nullable=False
    # )

    chat_id: Mapped[str] = mapped_column(nullable=False)
    uses: Mapped[int] = mapped_column(nullable=False, default=0)

    # # Relationship
    # message_action: Mapped["MessageAction"] = relationship(back_populates="user_usages")
