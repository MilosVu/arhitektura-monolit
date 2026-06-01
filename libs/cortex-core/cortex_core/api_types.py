"""Zajednički API response tipovi."""

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    """Standardni error envelope za sve API greške."""

    model_config = ConfigDict(frozen=True)

    status: int = Field(description="HTTP status kod")
    code: str = Field(description="Mašinski čitljiv kod greške")
    detail: str = Field(description="Poruka za debugging")
