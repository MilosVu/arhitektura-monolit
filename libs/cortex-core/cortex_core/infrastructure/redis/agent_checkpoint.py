"""
LangGraph checkpoint store — perzistencija agent state-a između koraka grafa.

Ključevi:
  cortex:agent:checkpoint:{thread_id}  → serializovano AgentState

U produkciji: LangGraph RedisSaver; ovde stub interfejs.
"""

from typing import Any

from cortex_core.infrastructure.redis.client import RedisCacheAdapter

CHECKPOINT_TTL = 86400


class LangGraphCheckpointStore:
    """Čuva stanje LangGraph agenta (messages, tool_calls, retrieved_chunks)."""

    def __init__(self, cache: RedisCacheAdapter | None = None) -> None:
        self._cache = cache or RedisCacheAdapter()

    def _key(self, thread_id: str) -> str:
        return f"cortex:agent:checkpoint:{thread_id}"

    def load(self, thread_id: str) -> dict[str, Any] | None:
        return self._cache.get_json(self._key(thread_id))

    def save(self, thread_id: str, state: dict[str, Any]) -> None:
        self._cache.set_json(self._key(thread_id), state, ttl_seconds=CHECKPOINT_TTL)

    def clear(self, thread_id: str) -> None:
        self._cache.delete(self._key(thread_id))
