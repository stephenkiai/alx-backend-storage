import redis
import uuid
from typing import Union, Callable


class Cache:
    """A class to handle caching using Redis."""

    def __init__(self):
        """Initialize the cache instance &
        flush the Redis database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate random key using uuid,
        store data in Redis,return the key."""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Callable = None):
        """Retrieve values from Redis."""
        data = self._redis.get(key)
        return fn(data) if fn and data is not None else data

    def get_str(self, key: str) -> str:
        """Get data and convert to string."""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get data and convert to integer."""
        return self.get(key, fn=lambda x: int(x))
