from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import CallbackQuery

from app import config, db
from .. import utils
from ..client import client
from . import keyborad

MESSAGE = config.Message()


@client.on_callback_query(filters.regex("check_join"))
async def check_join(client: Client, callback_query: CallbackQuery):
    message = callback_query.message
    user_id = message.chat.id
    
    # ====== CHECK JOIN ======
    channels = await utils.forced_join(client, user_id)
    if channels:
        keyboard = keyborad.forced_join(channels, MESSAGE.BUT_JOIN, MESSAGE.BUT_JOIN_URL)
        await message.delete()
        await client.send_message(user_id, MESSAGE.JOIN, reply_markup=keyboard)        
        return

    await message.delete()
    join_message = db.func.ForcedJoinMessage(user_id, db.get_session)
    await join_message.delete()
    await client.send_message(user_id, MESSAGE.WLECOME)
