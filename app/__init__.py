import asyncio
from app.db import create_all_tables

def init_db():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(create_all_tables())
    else:
        loop.run_until_complete(create_all_tables())

init_db()