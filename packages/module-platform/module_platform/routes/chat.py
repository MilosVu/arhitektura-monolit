from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_platform.api import PlatformModule
from module_platform.deps import get_current_user, get_platform_module
from module_platform.models import User, get_db
from module_platform.schemas import (
    AssistantMessageSave,
    ChatHistoryResponse,
    ChatMessageRequest,
    ChatThreadCreate,
    ChatThreadResponse,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/threads", response_model=ChatThreadResponse)
def create_thread(
    body: ChatThreadCreate,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return platform.create_chat_thread(body.case_id, current_user, db)


@router.get("/threads/{thread_id}", response_model=ChatHistoryResponse)
def get_thread_history(
    thread_id: str,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return platform.get_chat_history(thread_id, current_user)


@router.post("/threads/{thread_id}/messages")
async def send_chat_message(
    thread_id: str,
    body: ChatMessageRequest,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await platform.send_chat_message(thread_id, body.message, body.case_id, current_user)


@router.post("/threads/{thread_id}/assistant")
def save_assistant_message(
    thread_id: str,
    body: AssistantMessageSave,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return platform.save_assistant_message(thread_id, body.content, current_user)
