import redis
from cortex_core.settings import get_settings

_redis_client: redis.Redis | None = None


def _get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(get_settings().redis_url, decode_responses=True)
    return _redis_client


def ping_redis() -> bool:
    try:
        return _get_redis().ping()
    except Exception:
        return False
