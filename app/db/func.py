from typing import AsyncContextManager, Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


class ForcedJoinMessage:
    def __init__(
        self,
        chat_id,
        get_db_session: Callable[[], AsyncContextManager[AsyncSession]],
    ):
        self.chat_id = chat_id
        self.get_session = get_db_session

    async def add(self, message_id:str):
        async with self.get_session() as session:
            session.add(
                models.ForcedJoinMessage(
                    chat_id=self.chat_id,
                    message_id=message_id,
                )
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    async def delete(self):
        async with self.get_session() as session:
            lock = await session.get(
                models.ForcedJoinMessage,
                self.chat_id,
            )
            if not lock:
                return
            await session.delete(lock)

    
    async def get_message_id(self)-> str | None:
        async with self.get_session() as session:
            lock = await session.get(
                models.ForcedJoinMessage,
                self.chat_id,
            )
            if not lock:
                return None
        return lock.message_id
