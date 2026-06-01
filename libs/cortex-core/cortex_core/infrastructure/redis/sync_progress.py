"""
Sync progress pub/sub — alternativa polling-u preko WebSocket gateway-a.

Kanal:
  cortex:sync:progress:{job_id}

Worker publish-uje, gateway/web-client subscribe (future).
Trenutno MVP koristi PostgreSQL SyncJob polling — ovaj sloj je priprema.
"""

from cortex_core.infrastructure.redis.client import RedisCacheAdapter


class SyncProgressPublisher:
    def __init__(self, cache: RedisCacheAdapter | None = None) -> None:
        self._cache = cache or RedisCacheAdapter()

    def _channel(self, job_id: str) -> str:
        return f"cortex:sync:progress:{job_id}"

    def publish(self, job_id: str, *, progress: int, message: str, status: str) -> None:
        import json

        payload = json.dumps(
            {
                "job_id": job_id,
                "progress": progress,
                "message": message,
                "status": status,
            }
        )
        self._cache.publish(self._channel(job_id), payload)

    def channel_name(self, job_id: str) -> str:
        """Za Redis SUBSCRIBE u gateway WebSocket handleru."""
        return self._channel(job_id)
