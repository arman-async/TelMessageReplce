from pyrogram import Client

from app import config

client = Client(
    "bot",
    in_memory=True,
    api_id=config.Bot().API_ID,
    api_hash=config.Bot().API_HASH,
    bot_token=config.Bot().TOKEN,
    proxy={"scheme": "socks5", "hostname": "192.168.1.100", "port": 2080},
)