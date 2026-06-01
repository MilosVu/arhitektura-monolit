import asyncio
import logging
import time
from datetime import UTC, datetime

from cortex_core.ingestion_worker_celery import get_ingestion_celery_app
from cortex_models import Document, SyncJob, get_session_factory

from module_ingestion.worker_deps import register_worker_dependencies

celery_app = get_ingestion_celery_app()
_worker_deps = register_worker_dependencies()
_documents = _worker_deps.documents
_ocr = _worker_deps.ocr
_search = _worker_deps.search

logger = logging.getLogger(__name__)


def _update_job_progress(job_id: str, increment: int, message: str) -> None:
    session = get_session_factory()()
    try:
        job = session.query(SyncJob).filter(SyncJob.id == job_id).first()
        if job:
            job.progress = min(job.progress + increment, 95)
            job.message = message
            job.updated_at = datetime.now(UTC)
            session.commit()
    finally:
        session.close()


@celery_app.task(name="module_ingestion.tasks.ingest_document", bind=True)
def ingest_document(self, document_id: int, job_id: str) -> dict:
    session = get_session_factory()()
    try:
        doc = session.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return {
                "status": "failed",
                "document_id": document_id,
                "reason": "not found",
            }

        _documents.mark_ingesting(document_id, session)

        _update_job_progress(job_id, 10, f"OCR processing {doc.filename}...")

        extraction = asyncio.run(_ocr.extract_text(doc.filename, b""))
        chunks = asyncio.run(_ocr.chunk(extraction.plain_text))

        time.sleep(1)

        _update_job_progress(job_id, 5, f"Generating embeddings for {doc.filename}...")

        chunk_count = _search.upsert_document_chunks(
            document_id=document_id,
            case_id=doc.case_id,
            filename=doc.filename,
            chunks=chunks,
        )
        logger.info("Weaviate upsert: doc=%s chunks=%d", document_id, chunk_count)

        _documents.mark_ready(document_id, session, page_count=len(extraction.pages))

        return {
            "status": "ready",
            "document_id": document_id,
            "filename": doc.filename,
            "weaviate_chunks": chunk_count,
        }
    except Exception as exc:
        _documents.mark_failed(document_id, str(exc), session)
        raise
    finally:
        session.close()
