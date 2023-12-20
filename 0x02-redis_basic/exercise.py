import redis
import uuid
from typing import Union, Callable
from functools import wraps

r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    @wraps(method)
    def wrapper(self, data: Union[str, bytes, int, float]) -> str:
        """Wrapper function."""
        key = method.__qualname__
        count_key = f"count_calls:{key}"

        # Increment the count for the method
        r.incr(count_key)

        # Call the original method and return its result
        result = method(self, data)
        return result

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function."""
    @wraps(method)
    def wrapper(self, data: Union[str, bytes, int, float]) -> str:
        """Wrapper function."""
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        # Append the input arguments to the inputs list
        input_str = str(data)
        r.rpush(inputs_key, input_str)

        # Call the original method to retrieve the output
        output = method(self, data)

        # Store the output in the outputs list
        r.rpush(outputs_key, output)

        return output

    return wrapper


class Cache:
    """A class to handle caching using Redis."""

    def __init__(self):
        """Initialize the cache instance and flush the Redis database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis."""
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
