from datetime import datetime

from pydantic import BaseModel


class ComponentStatus(BaseModel):
    name: str
    status: str  # ok | degraded | down
    latency_ms: float | None = None
    detail: str | None = None


class SystemStatusResponse(BaseModel):
    overall: str  # ok | degraded | down
    components: list[ComponentStatus]
    checked_at: datetime
