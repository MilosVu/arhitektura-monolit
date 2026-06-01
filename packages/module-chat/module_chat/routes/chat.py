from typing import Annotated

from cortex_models import User, get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from module_chat.api import ChatModule
from module_chat.deps import get_chat_module, get_current_user
from module_chat.schemas import (
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
    chat: Annotated[ChatModule, Depends(get_chat_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return chat.create_thread(body.case_id, current_user, db)


@router.get("/threads/{thread_id}", response_model=ChatHistoryResponse)
def get_thread_history(
    thread_id: str,
    chat: Annotated[ChatModule, Depends(get_chat_module)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return chat.get_history(thread_id, current_user)


@router.post("/threads/{thread_id}/messages")
async def send_chat_message(
    thread_id: str,
    body: ChatMessageRequest,
    chat: Annotated[ChatModule, Depends(get_chat_module)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if body.case_id is None:
        raise HTTPException(status_code=400, detail="case_id is required")
    return await chat.send_message(thread_id, body.message, body.case_id, current_user)


@router.post("/threads/{thread_id}/assistant")
def save_assistant_message(
    thread_id: str,
    body: AssistantMessageSave,
    chat: Annotated[ChatModule, Depends(get_chat_module)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return chat.save_assistant_message(thread_id, body.content, current_user)
