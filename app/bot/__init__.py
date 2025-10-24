from pyrogram.methods.utilities.idle import idle

from .client import *
from .handler import *



async def run():
    await client.start()
    print("Bot started")
    await idle()
