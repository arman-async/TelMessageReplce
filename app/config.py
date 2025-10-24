from ast import literal_eval
from functools import lru_cache
from os import getenv

import yaml
from dotenv import get_key, load_dotenv
from pydantic import BaseModel

load_dotenv()

@lru_cache
def get_string(key: str) -> None|str:
    @lru_cache
    def load_string()-> dict:
        with open("strings.yaml") as f:
            return yaml.safe_load(f)

    return load_string().get(key)

class Bot(BaseModel):
    ACTIVE: bool = literal_eval(getenv("BOT_ACTIVE"))
    API_ID: str = int(getenv("API_ID"))
    API_HASH: str = getenv("API_HASH")
    TOKEN: str = getenv("BOT_TOKEN")
    OWNER_ID: str = int(getenv("OWNER_ID"))


class API(BaseModel):
    TOKEN: str = getenv("HTTP_TOKEN")
    ACTIVE: bool = literal_eval(getenv("API_ACTIVE"))


class Database(BaseModel):
    host: str = get_key(".env", "DB_HOST")
    port: str = get_key(".env", "DB_PORT")
    user: str = get_key(".env", "DB_USER")
    password: str = get_key(".env", "DB_PASSWORD")
    name: str = get_key(".env", "DB_NAME")

    def uri(self):
        return f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    def uri_sync(self):
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class Dashboard(BaseModel):
    USER: str = getenv("DASH_USER")
    PASSWORD: str = getenv("DASH_PASSWORD")

class Redis(BaseModel):
    host: str = getenv("REDIS_HOST")
    port: str = getenv("REDIS_PORT")
    db: str = getenv("REDIS_DB")
    password: str = getenv("REDIS_PASSWORD")

class CacheTTL(BaseModel):
    ttl: float = float(getenv("CACHE_TTL", "5"))
    PROCESS_FORCED_JOIN: float = float(getenv("CACHE_TTL_PROCESS_FORCED_JOIN", "1"))
    
class Message(BaseModel):
    WLECOME :str = get_string("MESSAGE_WLECOME")
    JOIN :str = get_string("MESSAGE_JOIN")
    BUT_JOIN :str = get_string("BUT_JOIN")
    BUT_JOIN_URL: str |None = get_string("BUT_JOIN_URL")