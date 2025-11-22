from pyrogram import Client, enums

from app import config


client = Client(
    "bot",
    api_id=config.Bot().API_ID,
    api_hash=config.Bot().API_HASH,
    bot_token=config.Bot().TOKEN,
    workers=config.Bot().WORKERS,
    proxy=config.Bot().PROXY,
    parse_mode=enums.ParseMode.MARKDOWN,
)

if config.GuardJoin().TOKEN is None:
    guard_join = Client(
        "guard_join",
        api_id=config.GuardJoin().API_ID,
        api_hash=config.GuardJoin().API_HASH,
        bot_token=config.GuardJoin().TOKEN,
        proxy=config.Bot().PROXY,
        parse_mode=enums.ParseMode.MARKDOWN,
    )
else:
    guard_join = client