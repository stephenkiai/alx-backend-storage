import requests
from cachetools import TTLCache
import redis
from functools import wraps
from typing import Dict

# Redis client
redis_client = redis.Redis()

# Cache with a time-to-live (TTL) of 10 seconds
cache = TTLCache(maxsize=100, ttl=10)


def cache_decorator(func):
    @wraps(func)
    def wrapper(url):
        # Check if the result is already in the cache
        cached_result = cache.get(url)
        if cached_result:
            print(f"Cache hit for {url}")
            return cached_result

        # If not in cache, call the original function
        result = func(url)

        # Store the result in the cache with the URL as the key
        cache[url] = result

        # Update the count for the URL in Redis
        update_url_count(url)

        return result

    return wrapper


def update_url_count(url: str) -> None:
    # Update the count for the URL in Redis
    count_key = f"count:{url}"
    count = redis_client.get(count_key)
    count = int(count) + 1 if count else 1
    redis_client.set(count_key, count)
    print(f"Accessed {url} {count} times")


@cache_decorator
def get_page(url: str) -> str:
    # Make a request to the URL
    response = requests.get(url)

    # Return the HTML content
    return response.text


# Test the function
if __name__ == "__main__":
    # Test with a slow response URL
    slow_url = "http://slowwly.robertomurray.co.uk"
    html_content = get_page(slow_url)
    print(html_content)
