"""Redis implementacija ChatStorePort."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from cortex_core.infrastructure.redis.client import get_redis_client

from module_chat.schemas import ChatMessage

THREAD_TTL_SECONDS = 86400  # 24h


class RedisChatStore:
    def _thread_key(self, thread_id: str) -> str:
        return f"cortex:thread:{thread_id}"

    def _messages_key(self, thread_id: str) -> str:
        return f"cortex:thread:{thread_id}:messages"

    def save_thread(self, thread_id: str, case_id: int, user_id: int) -> None:
        r = get_redis_client()
        data = {
            "thread_id": thread_id,
            "case_id": case_id,
            "user_id": user_id,
            "created_at": datetime.now(UTC).isoformat(),
        }
        r.setex(self._thread_key(thread_id), THREAD_TTL_SECONDS, json.dumps(data))

    def get_thread(self, thread_id: str) -> dict[str, Any] | None:
        raw = get_redis_client().get(self._thread_key(thread_id))
        if not raw:
            return None
        return json.loads(raw)

    def append_message(self, thread_id: str, role: str, content: str) -> None:
        r = get_redis_client()
        msg = ChatMessage(role=role, content=content, timestamp=datetime.now(UTC))
        r.rpush(self._messages_key(thread_id), msg.model_dump_json())
        r.expire(self._messages_key(thread_id), THREAD_TTL_SECONDS)

    def get_messages(self, thread_id: str) -> list[ChatMessage]:
        raw_messages = get_redis_client().lrange(self._messages_key(thread_id), 0, -1)
        return [ChatMessage.model_validate_json(m) for m in raw_messages]
