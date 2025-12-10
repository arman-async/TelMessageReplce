import asyncio
import json
import re

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from redis import Redis
from sqlalchemy import select

from app import config, db, logger

from .. import utils
from ..client import client, guard_join
from . import keyborad

LOGGER = logger.get_logger(__name__)
BOT_ID = int(config.Bot().TOKEN.split(":")[0])
cache_async = db.cache.RedisCacheFunction(
    Redis(**config.Redis().model_dump())
).cache_async

ForceJoinExtraAPI = config.ForceJoinExtraAPI()
CACHE_TTL = config.CacheTTL().PROCESS_FORCED_JOIN
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

    @cache_async(expire=CACHE_TTL, include={"chat_id"})
    async def check(
        message: Message,
        chat_id: int = chat_id,
        user_id: int = user_id,
    ) -> bool:
        """
        Manages Forced membership to channels
        + Database-level locking to prevent duplicate messages
        + Delete messages if you are not a member.
        """
        join_message = db.func.ForcedJoinMessage(chat_id, db.get_session)

        message_id = await join_message.get_message_id()
        if message_id:
            await client.delete_messages(user_id, int(message_id))
            await join_message.delete()

        if ForceJoinExtraAPI.USE:
            channels = await utils.forced_join_extra(ForceJoinExtraAPI, user_id)
        else:
            channels = await utils.forced_join(guard_join, user_id)

        if not channels:
            return False

        keyboard = keyborad.forced_join(
            channels, MESSAGE.BUT_JOIN, MESSAGE.BUT_JOIN_URL
        )
        new_message = await client.send_message(
            user_id,
            f"{MESSAGE.JOIN}",
            reply_markup=keyboard,
        )
        await join_message.add(new_message.id)
        return True

    if await check(message):
        await message.delete()
        return True
    return False


# ======== PROCESS FOR MESSAGE ACTIONS ========
async def process_message_actions(
    client: Client,
    message: Message,
    user_id: int,
    has_passed_join_check: bool,
) -> bool:
    """
    Handle message actions
    Returns (true) only if the message is an advertisement.
    """

    async with db.get_session() as session:
        result = await session.execute(select(db.models.MessageAction))
        actions = result.scalars().all()

        for action in actions:
            if message.text is None:
                continue

            should_run_action = (
                action.run_after_join_check and not has_passed_join_check
            ) or (not action.run_after_join_check and has_passed_join_check)

            if should_run_action:
                continue

            if not re.search(action.regex, message.text):
                continue

            if action.action == db.enums.MessageActions.IGNORE:
                continue

            if isinstance(action.max_total_uses, int):
                action.max_total_uses -= 1
                if action.max_total_uses <= 0:
                    action.max_total_uses = None
                    action.action = db.enums.MessageActions.IGNORE
                    await session.commit()
                    continue

            if isinstance(action.max_uses_per_user, int):
                user_usages = await session.execute(
                    select(db.models.MessageActionUserUsage)
                    .where(
                        db.models.MessageActionUserUsage.message_action_id == action.id
                    )
                    .where(db.models.MessageActionUserUsage.chat_id == user_id)
                )
                user_usages = user_usages.scalar_one_or_none()

                if user_usages is None:
                    user_usages = db.models.MessageActionUserUsage(
                        message_action_id=action.id,
                        chat_id=user_id,
                        uses=0,
                    )
                    session.add(user_usages)

                if user_usages.uses > action.max_uses_per_user:
                    continue

                user_usages.uses += 1
                await session.commit()

            if action.action == db.enums.MessageActions.ADS:
                return True

            if action.action == db.enums.MessageActions.DELETE:
                await message.delete()

            if action.action == db.enums.MessageActions.REPLACE:
                await message.delete()
                await client.send_message(user_id, action.message_replace)

            if action.action == db.enums.MessageActions.EDIT:
                inline_keyboard = None
                if action.inline_keyboard_json is not None:
                    inline_keyboard = keyborad.json_to_keyboard(
                        action.inline_keyboard_json
                    )
                entities = None
                if action.entities is not None:
                    try:
                        entities_list = json.loads(action.entities)
                    except json.JSONDecodeError:
                        entities_list = None
                    if entities_list is not None:
                        entities = utils.list_to_entitie(entities_list)

                await message.edit(
                    action.message_replace,
                    reply_markup=inline_keyboard,
                    entities=entities,
                )
                # اینجا امیر گفت میخوام وقتی ادیت شد بقیه ادیت ها نادیده گرفته شود
                break


# ======== HANDLER FOR ALL MESSAGES ========
@client.on_message(filters.private)
async def all_message(client: Client, message: Message):

    message_from_bot = False
    user_id = message.chat.id
    chat_id = message.chat.id
    if message.from_user.id != BOT_ID:
        user_id = message.from_user.id
        message_from_bot = True

    LOGGER.info(f"Processing message from User ID={user_id}")

    async with user_processing_lock(user_id) as lock:
        if message_from_bot:
            if await process_forced_join(client, message, user_id, chat_id):
                return

        if await process_message_actions(client, message, user_id, False):
            return

        if await process_forced_join(client, message, user_id, chat_id):
            return

        if await process_message_actions(client, message, user_id, True):
            return
