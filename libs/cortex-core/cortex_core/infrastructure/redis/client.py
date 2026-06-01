"""Redis adapter — implementacija CachePort protokola."""

import json
from typing import Any, cast

from cortex_core.ports.cache import CachePort
from cortex_core.settings import get_settings

import redis

_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(get_settings().redis_url, decode_responses=True)
    return _client


class RedisCacheAdapter(CachePort):
    """
    Niskonivojski Redis wrapper.

    Koriste ga: AdSessionCache, ChatRepository, SyncProgressPublisher,
    LangGraphCheckpointStore.
    """

    def __init__(self, client: redis.Redis | None = None) -> None:
        self._client = client or get_redis_client()

    def get(self, key: str) -> str | None:
        return cast(str | None, self._client.get(key))

    def set(self, key: str, value: str, *, ttl_seconds: int | None = None) -> None:
        if ttl_seconds:
            self._client.setex(key, ttl_seconds, value)
        else:
            self._client.set(key, value)

    def delete(self, key: str) -> None:
        self._client.delete(key)

    def publish(self, channel: str, message: str) -> None:
        self._client.publish(channel, message)

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except Exception:
            return False

    def get_json(self, key: str) -> dict[str, Any] | None:
        raw = self.get(key)
        return json.loads(raw) if raw else None

    def set_json(
        self, key: str, payload: dict[str, Any], *, ttl_seconds: int | None = None
    ) -> None:
        self.set(key, json.dumps(payload), ttl_seconds=ttl_seconds)
