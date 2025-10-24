import base64
import inspect
import pickle
from functools import wraps
from typing import Any

from redis import Redis


class RedisCacheFunction:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def gen_key(self, *args, **kwargs) -> str:
        return base64.b64encode(
            pickle.dumps({"args": args, "kwargs": kwargs})
        ).decode()

    def get_cache(self, key: str) -> Any:
        cached_data = self.redis_client.get(key)
        if isinstance(cached_data, bytes):
            return pickle.loads(cached_data)
        return None

    def set_cache(self, key: str, data: Any, expire: int | None = None):
        self.redis_client.set(key, pickle.dumps(data), ex=expire)

    def filter_inputs(
        self,
        params: dict[str, Any],
        exclude: set[str] | None = None,
        include: set[str] | None = None,
    ) -> dict[str, Any]:
        if include:
            return {k: v for k, v in params.items() if k in include}
        if exclude:
            return {k: v for k, v in params.items() if k not in exclude}
        return params

    def cache_async(
        self,
        expire: int | None = None,
        exclode: set[str] | None = None,
        include: set[str] | None = None,
    ):
        def decorator(func):
            sig = inspect.signature(func)

            @wraps(func)
            async def wrapper(*args, **kwargs):
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                params_dict: dict[str, Any] = dict(bound.arguments)
                params = self.filter_inputs(params_dict, exclode, include)
                key = self.gen_key(params)
                is_cache = self.get_cache(key)
                if is_cache:
                    return is_cache

                response = await func(*args, **kwargs)
                self.set_cache(key, response, expire)

                return response

            return wrapper

        return decorator
