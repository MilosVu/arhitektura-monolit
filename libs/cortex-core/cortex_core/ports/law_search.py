"""Port for law chunk vector search — write in law-sync, read in AI."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LawChunkHit:
    law_ref: str
    version_id: int
    content: str
    score: float


class LawSearchPort(ABC):
    """Hybrid / vector search over law chunks (Weaviate LawChunk collection)."""

    @abstractmethod
    def search_law_chunks(
        self,
        query: str,
        *,
        jurisdiction: str | None = None,
        canton_code: str | None = None,
        as_of: date | None = None,
        limit: int = 5,
    ) -> list[LawChunkHit]:
        """Search law chunks with optional jurisdiction and temporal filter."""

    @abstractmethod
    def upsert_law_chunks(
        self,
        *,
        version_id: int,
        law_ref: str,
        jurisdiction: str,
        canton_code: str | None,
        law_code: str,
        article: str | None,
        valid_from: date,
        valid_to: date | None,
        chunks: list[str],
    ) -> int:
        """Upsert chunks for a law version; returns count written."""
