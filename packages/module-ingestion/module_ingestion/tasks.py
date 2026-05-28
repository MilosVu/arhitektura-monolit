import logging
import time
from datetime import UTC, datetime

from cortex_core.enums import DocumentStatus
from module_ingestion.models import Document, SyncJob, get_session_factory
from module_ingestion.adapters.weaviate_store import upsert_document_chunks

from cortex_core.worker_celery import get_worker_celery_app

celery_app = get_worker_celery_app()

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


def _mock_chunks(filename: str, document_id: int) -> list[str]:
    base = filename.replace(".pdf", "").replace("_", " ")
    return [
        f"Abschnitt 1 aus {base}: Die Parteien vereinbaren die Lieferung der Ware innerhalb von 30 Tagen.",
        f"Abschnitt 2 aus {base}: Zahlungsfrist beträgt 30 Tage netto ab Rechnungsdatum. Vertrag Klausel 3.2.",
        f"Abschnitt 3 aus {base}: Bei Vertragsbruch haftet die schuldige Partei gemäss OR Art. 41 für Schadenersatz.",
    ]


@celery_app.task(name="module_ingestion.tasks.ingest_document", bind=True)
def ingest_document(self, document_id: int, job_id: str) -> dict:
    session = get_session_factory()()
    try:
        doc = session.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return {"status": "failed", "document_id": document_id, "reason": "not found"}

        doc.status = DocumentStatus.INGESTING.value
        doc.updated_at = datetime.now(UTC)
        session.commit()

        _update_job_progress(job_id, 10, f"OCR processing {doc.filename}...")

        time.sleep(1)

        _update_job_progress(job_id, 5, f"Generating embeddings for {doc.filename}...")

        chunks = _mock_chunks(doc.filename, document_id)
        chunk_count = upsert_document_chunks(
            document_id=document_id,
            case_id=doc.case_id,
            filename=doc.filename,
            chunks=chunks,
        )
        logger.info("Weaviate upsert: doc=%s chunks=%d", document_id, chunk_count)

        doc.status = DocumentStatus.READY.value
        doc.updated_at = datetime.now(UTC)
        session.commit()

        return {
            "status": "ready",
            "document_id": document_id,
            "filename": doc.filename,
            "weaviate_chunks": chunk_count,
        }
    finally:
        session.close()
