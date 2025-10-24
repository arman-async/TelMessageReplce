import json
import hashlib
import functools
from typing import Callable, Any, Awaitable
from redis.asyncio import Redis
from app import config


@functools.lru_cache
def get_redis() -> Redis:
    """Return a cached async Redis client."""
    return Redis(**config.Redis().model_dump())


def redis_cache(ttl: int = 60):
    """
    Async decorator to cache function results in Redis with TTL.
    
    Args:
        ttl (int): Time-to-live in seconds for the cached value.
    """
    def decorator(func: Callable[..., Awaitable[Any]]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            client = get_redis()

            # Generate a unique cache key based on function name and arguments
            key_data = {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs
            }
            key_str = json.dumps(key_data, sort_keys=True, default=str)
            key_hash = hashlib.sha256(key_str.encode()).hexdigest()
            cache_key = f"cache:{func.__module__}:{func.__name__}:{key_hash}"

            # Try to get from Redis
            cached = await client.get(cache_key)
            if cached is not None:
                return json.loads(cached)

            # Run the function and store result
            result = await func(*args, **kwargs)
            await client.setex(cache_key, ttl, json.dumps(result, default=str))
            return result

        return wrapper
    return decorator



