#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
import redis
from typing import Callable
from requests import get
from functools import wraps


r = redis.Redis()
CACHE_EXPIRATION_TIME = 10


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a function"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function for counting calls and caching results"""
        r.incr(f"count:{url}")
        cache = r.get(f"cached:{url}")
        if cache:
            return cache.decode('utf-8')
        try:
            html = method(url)
            r.setex(f"cached:{url}", CACHE_EXPIRATION_TIME, html)
            return html
        except Exception as e:
            return str(e)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and return it"""
    return get(url).text
