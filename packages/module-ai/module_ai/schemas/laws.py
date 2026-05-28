from pydantic import BaseModel


class LawNodeResponse(BaseModel):
    ref: str
    title: str
    article: str
    content: str
    valid_from: str
    valid_to: str | None = None
