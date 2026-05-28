"""Chat thread persistence in Redis — platform-owned."""

import json
from datetime import UTC, datetime

from module_platform.infrastructure.redis import _get_redis
from module_platform.schemas import ChatMessage

THREAD_TTL_SECONDS = 86400  # 24h


def _thread_key(thread_id: str) -> str:
    return f"cortex:thread:{thread_id}"


def _messages_key(thread_id: str) -> str:
    return f"cortex:thread:{thread_id}:messages"


def save_thread(thread_id: str, case_id: int, user_id: int) -> None:
    r = _get_redis()
    data = {
        "thread_id": thread_id,
        "case_id": case_id,
        "user_id": user_id,
        "created_at": datetime.now(UTC).isoformat(),
    }
    r.setex(_thread_key(thread_id), THREAD_TTL_SECONDS, json.dumps(data))


def get_thread(thread_id: str) -> dict | None:
    raw = _get_redis().get(_thread_key(thread_id))
    if not raw:
        return None
    return json.loads(raw)


def append_message(thread_id: str, role: str, content: str) -> ChatMessage:
    r = _get_redis()
    msg = ChatMessage(role=role, content=content, timestamp=datetime.now(UTC))
    r.rpush(_messages_key(thread_id), msg.model_dump_json())
    r.expire(_messages_key(thread_id), THREAD_TTL_SECONDS)
    return msg


def get_messages(thread_id: str) -> list[ChatMessage]:
    raw_messages = _get_redis().lrange(_messages_key(thread_id), 0, -1)
    return [ChatMessage.model_validate_json(m) for m in raw_messages]
