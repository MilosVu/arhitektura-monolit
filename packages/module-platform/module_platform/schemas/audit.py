from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    action: str
    resource_type: str
    resource_id: str
    details: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
