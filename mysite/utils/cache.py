import logging
from functools import wraps
from hashlib import md5

from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

logger = logging.getLogger(__name__)

try:
    cache = caches['redis']
except (InvalidCacheBackendError, ImportError) as e:
    # Use local memory cache
    logger.warning('Occured error [%s] when loading redis, Use main memory', e)
    cache = caches['default']


def cache_decorator(func, expiration=3 * 60):
    @wraps(func)
    def wrapper(func):
        def news(*args, **kwargs):
            unique_str = repr((func, args, kwargs))
            m = md5.new(unique_str)
            key = m.hexdigest()
            value = cache.get(key)
            if value:
                return value
            else:
                value = func(*args, **kwargs)
                cache.set(key, value, expiration)
                return value

        return news

    return wrapper
