from pydantic import BaseModel


class AgentChatRequest(BaseModel):
    message: str
    thread_id: str
    case_id: int | None = None
