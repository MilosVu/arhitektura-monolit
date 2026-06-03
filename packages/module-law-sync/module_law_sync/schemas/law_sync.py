from datetime import datetime

from cortex_core.enums import LawSyncJobStatus
from pydantic import BaseModel, Field


class LawSyncJobCreateRequest(BaseModel):
    scope: str = Field(default="federal", examples=["federal", "cantonal:ZH"])


class LawSyncJobCreateResponse(BaseModel):
    job_id: str
    message: str = "Law sync job enqueued"


class LawSyncJobResponse(BaseModel):
    id: str
    scope: str
    status: LawSyncJobStatus
    progress: int
    message: str | None
    stats_json: str | None
    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None

    model_config = {"from_attributes": True}
