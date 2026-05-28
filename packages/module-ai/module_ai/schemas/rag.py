from pydantic import BaseModel, Field


class RagSearchRequest(BaseModel):
    query: str
    case_id: int | None = None
    limit: int = Field(default=5, le=20)


class RagChunk(BaseModel):
    document_id: int
    filename: str
    content: str
    score: float


class RagSearchResponse(BaseModel):
    query: str
    chunks: list[RagChunk]
