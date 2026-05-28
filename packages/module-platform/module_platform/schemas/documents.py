from datetime import datetime

from pydantic import BaseModel

from cortex_core.enums import DocumentStatus


class DocumentSummary(BaseModel):
    id: int
    case_id: int
    filename: str
    mime_type: str
    status: DocumentStatus
    page_count: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentDetail(BaseModel):
    id: int
    case_id: int
    filename: str
    mime_type: str
    status: DocumentStatus
    page_count: int | None
    alfresco_node_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
