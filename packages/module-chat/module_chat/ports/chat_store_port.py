"""Port za chat thread persistence."""

from __future__ import annotations

from typing import Any, Protocol

from module_chat.schemas import ChatMessage


class ChatStorePort(Protocol):
    def save_thread(self, thread_id: str, case_id: int, user_id: int) -> None: ...

    def get_thread(self, thread_id: str) -> dict[str, Any] | None: ...

    def append_message(self, thread_id: str, role: str, content: str) -> None: ...

    def get_messages(self, thread_id: str) -> list[ChatMessage]: ...
