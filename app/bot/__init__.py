from pyrogram.methods.utilities.idle import idle

from .client import *
from .handler import *



async def run():
    await client.start()
    if config.GuardJoin().TOKEN:
        print(f"{guard_join} started")
        await guard_join.start()
        await idle()    
    print(f"{client} started")
    await idle()
