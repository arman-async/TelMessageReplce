import aiohttp
from pyrogram import enums
from pyrogram.client import Client
from pyrogram.errors import UserNotParticipant
from sqlalchemy import select

from app import config, db


async def is_user_in_channel(client: Client, user_id: int, channel_id: str) -> bool:
    if channel_id == "!":
        return False
    try:
        chat = await client.get_chat(channel_id)
        member = await client.get_chat_member(chat.id, user_id)
        return member.status != enums.ChatMemberStatus.LEFT
    except UserNotParticipant:
        return False


async def forced_join(
    client: Client,
    user_chat: int | str,
) -> list[db.models.ForcedSubscription]:
    async with db.get_session() as session:
        result = await session.execute(select(db.models.ForcedSubscription))
        channels = result.scalars().all()
    result = []

    # ===== Add channels =====
    for channel in channels:
        # skip !(Fake) channels
        if channel.channel_id == "!":
            continue
        try:
            user_join = await is_user_in_channel(client, user_chat, channel.channel_id)
        except AttributeError:
            pass
        if user_join:
            continue
        result.append(channel)

    if not result:
        return result

    # ===== Add !(Fake) channel =====
    for channel in channels:
        if channel.channel_id != "!":
            continue
        result.append(channel)

    return result


async def forced_join_extra(
    API: config.ForceJoinExtraAPI,
    user_chat: int | str,
) -> list[db.models.ForcedSubscription]:
    # ==== Get channels =====
    async with db.get_session() as session:
        result = await session.execute(select(db.models.ForcedSubscription))
        channels = result.scalars().all()

    result = []
    # ===== Add channels =====
    for channel in channels:
        # skip !(Fake) channels
        if channel.channel_id == "!":
            continue
        async with aiohttp.ClientSession() as http:
            url = API.URL.format(USER=user_chat, CHANNEL=channel.channel_id)
            async with http.get(url) as response:
                data = await response.json()
                if not isinstance(data, dict):
                    continue
                if data.get(API.KEY):
                    continue
                result.append(channel)

    if not result:
        return result

    # ===== Add !(Fake) channel =====
    for channel in channels:
        if channel.channel_id != "!":
            continue
        result.append(channel)

    return result
