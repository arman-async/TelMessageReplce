import asyncio
import re

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from sqlalchemy import select
from redis import Redis
from app import config, db

from .. import utils
from ..client import client
from . import keyborad

BOT_ID = int(config.Bot().TOKEN.split(":")[0])
cache_async = db.cache.RedisCacheFunction(
    Redis(**config.Redis().model_dump())
).cache_async

MESSAGE = config.Message()

user_processing_locks: dict[str, asyncio.locks.Lock] = {}


def user_processing_lock(user_id: int | str) -> asyncio.locks.Lock:
    user_id = str(user_id)
    if user_id not in user_processing_locks:
        lock = asyncio.Lock()

        # keep reference to original release method
        original_release = lock.release

        def auto_cleanup_release():
            """Release the lock and remove it from the pool if unlocked."""
            original_release()
            # if not lock.locked():
            #     user_processing_locks.pop(user_id, None)

        # replace release() with our wrapped version
        lock.release = auto_cleanup_release  # type: ignore

        user_processing_locks[user_id] = lock

    return user_processing_locks[user_id]


# ======= PROCESS FORCED JOIN ========
async def process_forced_join(
    client: Client,
    message: Message,
    user_id: int,
    chat_id: int,
) -> bool:
    @cache_async(expire=5)
    async def check(message: Message) -> bool:
        """
        Manages Forced membership to channels
        + Database-level locking to prevent duplicate messages
        + Delete messages if you are not a member.
        """
        join_message = db.func.ForcedJoinMessage(chat_id, db.get_session)
        await client.send_message(user_id, "Run Check Join")
        
        message_id = await join_message.get_message_id()
        if message_id:
            await client.delete_messages(user_id, int(message_id))
            await join_message.delete()

        channels = await utils.forced_join(client, user_id)
        if not channels:
            return False

        await message.delete()
        keyboard = keyborad.forced_join(channels, MESSAGE.BUT_JOIN, MESSAGE.BUT_JOIN_URL)
        new_message = await client.send_message(
            user_id,
            f"{MESSAGE.JOIN} - {chat_id=}, {user_id=}",
            reply_markup=keyboard,
        )
        await join_message.add(new_message.id)
        return True

    if await check(message):
        return True
    return False


# ======== PROCESS FOR MESSAGE ACTIONS ========
async def process_message_actions(
    client: Client,
    message: Message,
    user_id: int,
) -> bool:
    """
    Handle message actions
    Returns (true) only if the message is an advertisement.
    """
    async with db.get_session() as session:
        result = await session.execute(select(db.models.MessageAction))
        actions = result.scalars().all()

    for action in actions:
        if not re.search(action.regex, message.text):
            continue

        if action.acction == db.enums.MessageActions.ADS:
            return True

        if action.acction == db.enums.MessageActions.IGNORE:
            continue

        if action.acction == db.enums.MessageActions.DELETE:
            await message.delete()

        elif action.acction == db.enums.MessageActions.REPLACE:
            await message.delete()
            await client.send_message(user_id, action.message_replace)


# ======== HANDLER FOR ALL MESSAGES ========
@client.on_message()
async def all_message(client: Client, message: Message):
    message_from_bot = False
    user_id = message.chat.id
    chat_id = message.chat.id
    if message.from_user.id != BOT_ID:
        user_id = message.from_user.id
        message_from_bot = True

    async with user_processing_lock(user_id) as lock:
        if message_from_bot:
            if await process_forced_join(client, message, user_id, chat_id):
                return

        if await process_message_actions(client, message, user_id):
            return

        if await process_forced_join(client, message, user_id, chat_id):
            return
