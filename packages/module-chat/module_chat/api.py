"""Public facade for the chat domain module."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from cortex_core.domain.exceptions import ForbiddenError
from cortex_models import Case, User
from fastapi import HTTPException
from module_ai.api import AiModule
from sqlalchemy.orm import Session

from module_chat.ports.chat_store_port import ChatStorePort
from module_chat.schemas import ChatHistoryResponse, ChatMessage, ChatThreadResponse


class ChatModule:
    """In-process facade — persists threads via ChatStorePort, streams via AiModule."""

    def __init__(
        self,
        ai_module: AiModule | None = None,
        chat_store: ChatStorePort | None = None,
    ) -> None:
        from module_chat.adapters.redis_chat_store import RedisChatStore

        self._ai = ai_module or AiModule()
        self._store = chat_store or RedisChatStore()

    def _assert_case_access(self, case_id: int, user: User, db: Session) -> Case:
        case = (
            db.query(Case).filter(Case.id == case_id, Case.owner_id == user.id).first()
        )
        if not case:
            raise ForbiddenError(f"Case {case_id} not accessible")
        return case

    def create_thread(
        self, case_id: int, user: User, db: Session
    ) -> ChatThreadResponse:
        try:
            self._assert_case_access(case_id, user, db)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

        thread_id = str(uuid.uuid4())
        self._store.save_thread(thread_id, case_id, user.id)
        self._store.append_message(
            thread_id,
            "assistant",
            "Willkommen bei Cortex AI. Wie kann ich Ihnen bei diesem Fall helfen?",
        )

        return ChatThreadResponse(
            thread_id=thread_id,
            case_id=case_id,
            created_at=datetime.now(UTC),
        )

    def get_history(self, thread_id: str, user: User) -> ChatHistoryResponse:
        thread = self._store.get_thread(thread_id)
        if thread and thread.get("user_id") != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        messages = self._store.get_messages(thread_id)
        if not messages:
            messages = [
                ChatMessage(
                    role="assistant",
                    content="Willkommen bei Cortex AI. Wie kann ich Ihnen bei diesem Fall helfen?",
                    timestamp=datetime.now(UTC),
                )
            ]

        return ChatHistoryResponse(thread_id=thread_id, messages=messages)

    async def send_message(
        self, thread_id: str, message: str, case_id: int, user: User
    ):
        thread = self._store.get_thread(thread_id)
        if thread and thread.get("user_id") != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        self._store.append_message(thread_id, "user", message)
        return await self._ai.stream_chat(message, thread_id, case_id)

    def save_assistant_message(self, thread_id: str, content: str, user: User) -> dict:
        thread = self._store.get_thread(thread_id)
        if thread and thread.get("user_id") != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        self._store.append_message(thread_id, "assistant", content)
        return {"status": "saved"}
