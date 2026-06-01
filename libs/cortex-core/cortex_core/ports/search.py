"""Port ka vektorskoj pretrazi (Weaviate) — read u AI, write u ingestion."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkHit:
    document_id: int
    filename: str
    content: str
    score: float


class SearchPort(ABC):
    """Interfejs prema vektorskoj / hybrid pretrazi chunkova."""

    @abstractmethod
    def search_chunks(
        self,
        query: str,
        case_id: int | None = None,
        limit: int = 5,
    ) -> list[ChunkHit]:
        """BM25 / hybrid pretraga po chunkovima."""

    @abstractmethod
    def upsert_document_chunks(
        self,
        document_id: int,
        case_id: int,
        filename: str,
        chunks: list[str],
    ) -> int:
        """Upsert chunkova za dokument; vraća broj upisanih chunkova."""
