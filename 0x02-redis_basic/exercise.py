#!/usr/bin/env python3
""" redis drill """
import redis
from typing import Union, Callable, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count the calls of the cache method below """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapped function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapped function """
        self._redis.rpush(inputs, str(args))
        value = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(value))
        return value
    return wrapper

# r = redis.Redis(host='localhost', port=6379, db=0)
# r.set('key'= uuid4, 'value')


class Cache:
    """Writing strings to Redis"""
    def __init__(self):
        """ preparing the basics"""

        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ set data to redis"""

        gen_key = str(uuid4())
        self._redis.set(gen_key, data)
        return gen_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Reading from Redis and recovering original type"""
        value = self._redis.get(key)
        if fn is None:
            return value
        return fn(value)

    def get_str(self, key: str) -> str:
        """
        automatically parametrize Cache.get with the correct conversion func
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        automatically parametrize Cache.get with the correct conversion func
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value


def replay(method: Callable):
    """Display the history of calls of a function"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    r = method.__self__._redis
    # Get the number of times the function was called
    n = r.get(key)
    if n:
        n = int(n.decode("utf-8"))
    else:
        n = 0
    print("{} was called {} times:".format(key, n))
    # Retrieve inputs and outputs from Redis
    inputList = r.lrange(inputs, 0, -1)
    outputList = r.lrange(outputs, 0, -1)
    # Zip inputs and outputs together for iteration
    redis_zipped = list(zip(inputList, outputList))
    for a, b in redis_zipped:
        attr, value = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, value))
