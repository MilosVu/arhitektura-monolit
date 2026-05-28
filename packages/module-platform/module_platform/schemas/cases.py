from datetime import datetime

from pydantic import BaseModel

from module_platform.schemas.auth import UserResponse


class CaseSummary(BaseModel):
    id: int
    case_number: str
    title: str
    description: str | None
    document_count: int = 0
    last_synced_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CaseDetail(BaseModel):
    id: int
    case_number: str
    title: str
    description: str | None
    owner: UserResponse
    last_synced_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
