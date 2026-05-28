"""Port za OCR / ekstrakciju teksta — implementacija u ingestion-worker."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ExtractedPage:
    page_number: int
    text: str
    confidence: float


@dataclass
class ExtractionResult:
    filename: str
    pages: list[ExtractedPage]
    plain_text: str


class OCRPort(ABC):
    """Ekstrakcija teksta iz PDF/slika (Tesseract, Azure DI stub, itd.)."""

    @abstractmethod
    async def extract_text(self, filename: str, content: bytes) -> ExtractionResult:
        """Puni OCR pipeline za jedan dokument."""

    @abstractmethod
    async def chunk(self, plain_text: str, *, max_tokens: int = 512) -> list[str]:
        """Podeli tekst na RAG chunkove."""
