import logging

from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

logger = logging.getLogger(__name__)

try:
    cache = caches['redis']
except (InvalidCacheBackendError, ImportError) as e:
    # Use local memory cache
    logger.warning('Occured error [%s] when loading redis, Use main memory', e)
    cache = caches['default']
