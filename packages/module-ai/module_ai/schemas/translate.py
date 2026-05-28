from pydantic import BaseModel


class AgentTranslateRequest(BaseModel):
    document_id: int
    text: str
    source_lang: str | None = None
    target_lang: str = "de"


class TranslateRequest(BaseModel):
    target_lang: str = "de"
    source_lang: str | None = None


class TranslateResponse(BaseModel):
    document_id: int
    source_lang: str
    target_lang: str
    translated_text: str
