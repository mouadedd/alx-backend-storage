#!/usr/bin/env python3
""" redis drill """
import redis
from typing import Union, Callable, Optional
from uuid import uuid4


# r = redis.Redis(host='localhost', port=6379, db=0)
# r.set('key'= uuid4, 'value')

class Cache:
    """Writing strings to Redis"""
    def __init__(self):
        """ preparing the basics"""

        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: [str, bytes, int, float]) -> str:
        """ set data to redis"""

        gen_key = str(uuid4())
        self._redis.set(gen_key, data)
        return gen_key
