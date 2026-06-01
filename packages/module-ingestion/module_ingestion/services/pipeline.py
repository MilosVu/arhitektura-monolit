"""Ingestion pipeline — OCR → chunk → embed → Weaviate."""

from datetime import UTC, datetime

from cortex_core.base.service import BaseService
from cortex_core.enums import DocumentStatus
from cortex_core.infrastructure.llm.stub_router import StubLLMRouter
from cortex_models import Document
from sqlalchemy.orm import Session

from module_ingestion.adapters.ocr_adapter import StubOCRAdapter
from module_ingestion.adapters.weaviate_store import upsert_document_chunks


class IngestionPipelineService(BaseService):
    """
    CPU/GPU bound koraci:
      1. OCRPort.extract_text
      2. OCRPort.chunk
      3. LLMPort.embed (MaaS)
      4. Weaviate upsert
      5. Document.status = READY
    """

    def __init__(
        self,
        session: Session,
        ocr: StubOCRAdapter | None = None,
        llm: StubLLMRouter | None = None,
    ) -> None:
        self._session = session
        self._ocr = ocr or StubOCRAdapter()
        self._llm = llm or StubLLMRouter()

    async def ingest(self, document_id: int) -> dict:
        doc = self._session.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return {"status": "failed", "reason": "not found"}

        doc.status = DocumentStatus.INGESTING.value
        doc.updated_at = datetime.now(UTC)
        self._session.commit()

        extracted = await self._ocr.extract_text(doc.filename, b"mock-bytes")
        chunks = await self._ocr.chunk(extracted.plain_text)
        _vectors = await self._llm.embed(chunks)

        count = upsert_document_chunks(
            document_id=doc.id,
            case_id=doc.case_id,
            filename=doc.filename,
            chunks=chunks,
        )

        doc.status = DocumentStatus.READY.value
        doc.updated_at = datetime.now(UTC)
        self._session.commit()

        return {
            "status": "ready",
            "chunks": count,
            "vectors_dim": len(_vectors[0]) if _vectors else 0,
        }
