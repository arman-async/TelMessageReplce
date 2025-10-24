import asyncio
from . import config

async def start_bot():
    if config.Bot().ACTIVE:
        from .bot import run
        await run()

async def start_api():
    if config.API().ACTIVE:
        from .api import run
        await run()


async def main():
    tasks = []
    if config.Bot().ACTIVE:
        tasks.append(asyncio.create_task(start_bot()))
    if config.API().ACTIVE:
        tasks.append(asyncio.create_task(start_api()))
    if tasks:
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())