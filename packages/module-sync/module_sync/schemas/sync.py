from datetime import datetime

from cortex_core.enums import SyncJobStatus
from pydantic import BaseModel


class SyncJobResponse(BaseModel):
    id: str
    case_id: int
    status: SyncJobStatus
    progress: int
    total_documents: int
    message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SyncJobCreateResponse(BaseModel):
    job_id: str
    message: str = "Sync job enqueued"
