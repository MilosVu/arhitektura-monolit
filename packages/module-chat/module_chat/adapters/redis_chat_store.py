"""Redis implementacija ChatStorePort."""

from __future__ import annotations

from typing import Any

from module_chat.infrastructure import chat_store as _store
from module_chat.schemas import ChatMessage


class RedisChatStore:
    def save_thread(self, thread_id: str, case_id: int, user_id: int) -> None:
        _store.save_thread(thread_id, case_id, user_id)

    def get_thread(self, thread_id: str) -> dict[str, Any] | None:
        return _store.get_thread(thread_id)

    def append_message(self, thread_id: str, role: str, content: str) -> None:
        _store.append_message(thread_id, role, content)

    def get_messages(self, thread_id: str) -> list[ChatMessage]:
        return _store.get_messages(thread_id)
