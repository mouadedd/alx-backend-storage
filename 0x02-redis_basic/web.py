#!/usr/bin/env python3
"""  Implementing an expiring web cache and tracker """
import redis
from typing import Union, Callable, Optional
from requests import get
from functools import wraps


r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """ count the calls of requests """
    @wraps(method)
    def wrapper(url):
        """ wrapper for decorator """
        r.incr(f"count:{url}")
        cache = r.get(f"cached:{url}")
        if cache:
            return cache.decode('utf-8')
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """ Obtain the HTML content of a particular URL and returns it """
    return get(url).text
