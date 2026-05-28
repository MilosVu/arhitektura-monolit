from datetime import datetime

from pydantic import BaseModel


class ChatThreadCreate(BaseModel):
    case_id: int


class ChatThreadResponse(BaseModel):
    thread_id: str
    case_id: int
    created_at: datetime


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime | None = None


class ChatMessageRequest(BaseModel):
    message: str
    case_id: int | None = None


class AssistantMessageSave(BaseModel):
    content: str


class ChatHistoryResponse(BaseModel):
    thread_id: str
    messages: list[ChatMessage]
