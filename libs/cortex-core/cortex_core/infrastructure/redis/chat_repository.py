"""
Chat thread persistence — Redis DB 0.

Ključevi:
  cortex:thread:{thread_id}           → metadata (case_id, user_id)
  cortex:thread:{thread_id}:messages  → lista poruka (RPUSH)

Prefer module_platform.chat_store for new code; this class uses plain dicts
to avoid coupling cortex-core to module DTOs.
"""

from datetime import UTC, datetime
import json

from cortex_core.infrastructure.redis.client import RedisCacheAdapter

THREAD_TTL_SECONDS = 86400


class ChatRepository:
    """Repository pattern iznad Redis-a za chat sesije (gateway piše, ai-agents čita)."""

    def __init__(self, cache: RedisCacheAdapter | None = None) -> None:
        self._cache = cache or RedisCacheAdapter()

    def _thread_key(self, thread_id: str) -> str:
        return f"cortex:thread:{thread_id}"

    def _messages_key(self, thread_id: str) -> str:
        return f"cortex:thread:{thread_id}:messages"

    def save_thread(self, thread_id: str, case_id: int, user_id: int) -> None:
        payload = {
            "thread_id": thread_id,
            "case_id": case_id,
            "user_id": user_id,
            "created_at": datetime.now(UTC).isoformat(),
        }
        self._cache.set_json(self._thread_key(thread_id), payload, ttl_seconds=THREAD_TTL_SECONDS)

    def get_thread(self, thread_id: str) -> dict | None:
        return self._cache.get_json(self._thread_key(thread_id))

    def append_message(self, thread_id: str, role: str, content: str) -> dict:
        msg = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        key = self._messages_key(thread_id)
        client = self._cache._client
        client.rpush(key, json.dumps(msg))
        client.expire(key, THREAD_TTL_SECONDS)
        return msg

    def get_messages(self, thread_id: str) -> list[dict]:
        raw = self._cache._client.lrange(self._messages_key(thread_id), 0, -1)
        return [json.loads(m) for m in raw]
