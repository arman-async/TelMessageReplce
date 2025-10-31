from pyrogram import Client

from app import config

proxy = {"scheme": "socks5", "hostname": "192.168.1.100", "port": 2080}
client = Client(
    "bot",
    api_id=config.Bot().API_ID,
    api_hash=config.Bot().API_HASH,
    bot_token=config.Bot().TOKEN,
    
    proxy=proxy,
)

if config.GuardJoin().TOKEN is None:
    guard_join = Client(
        "guard_join",
        api_id=config.GuardJoin().API_ID,
        api_hash=config.GuardJoin().API_HASH,
        bot_token=config.GuardJoin().TOKEN,
        proxy=proxy,
    )
else:
    guard_join = client