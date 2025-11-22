from ast import literal_eval
from functools import lru_cache
from os import getenv
from urllib import parse
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
    WORKERS: int = int(getenv("BOT_WORKERS", "64"))
    OWNER_ID: str = int(getenv("OWNER_ID"))
    PROXY: dict|None = literal_eval(getenv("BOT_PROXY", "None"))

     

class GuardJoin(BaseModel):
    API_ID: int = int(getenv("GJ_API_ID") or Bot().API_ID)
    API_HASH: str = getenv("GJ_API_HASH") or Bot().API_HASH
    TOKEN: str |None = getenv("GJ_TOKEN")


class ForceJoinExtraAPI(BaseModel):
    USE: bool = literal_eval(getenv("FORCE_JOIN_EXTRA_API_USE", "False"))
    URL: str = getenv("FORCE_JOIN_EXTRA_API_URL")
    KEY: str = getenv("FORCE_JOIN_EXTRA_API_KEY")
    
class API(BaseModel):
    TOKEN: str = getenv("HTTP_TOKEN")
    ACTIVE: bool = literal_eval(getenv("API_ACTIVE"))


class Database(BaseModel):
    host: str = get_key(".env", "DB_HOST")
    port: str = get_key(".env", "DB_PORT")
    user: str = get_key(".env", "DB_USER")
    password: str = get_key(".env", "DB_PASSWORD")
    name: str = get_key(".env", "DB_NAME")
    max_connections: int = int(getenv("DB_MAX_CONNECTIONS", "100")) 

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
    ttl: int = int(getenv("CACHE_TTL", "5"))
    PROCESS_FORCED_JOIN: int = int(getenv("CACHE_TTL_PROCESS_FORCED_JOIN", "1"))
    
class Message(BaseModel):
    WLECOME :str = get_string("MESSAGE_WLECOME")
    JOIN :str = get_string("MESSAGE_JOIN")
    BUT_JOIN :str = get_string("BUT_JOIN")
    BUT_JOIN_URL: str |None = get_string("BUT_JOIN_URL")