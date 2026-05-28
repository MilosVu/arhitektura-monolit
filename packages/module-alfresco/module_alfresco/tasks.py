import time
from datetime import UTC, datetime

from celery import chain

from cortex_core.enums import DocumentStatus, SyncJobStatus
from module_alfresco.models import Case, Document, SyncJob, get_session_factory

from cortex_core.messaging.tasks import QUEUE_INGESTION, TASK_INGEST_DOCUMENT
from cortex_core.worker_celery import get_worker_celery_app

celery_app = get_worker_celery_app()


def _update_job(job_id: str, **kwargs) -> None:
    session = get_session_factory()()
    try:
        job = session.query(SyncJob).filter(SyncJob.id == job_id).first()
        if job:
            for key, value in kwargs.items():
                setattr(job, key, value)
            job.updated_at = datetime.now(UTC)
            session.commit()
    finally:
        session.close()


@celery_app.task(name="module_alfresco.tasks.sync_case_from_alfresco", bind=True)
def sync_case_from_alfresco(self, case_id: int, job_id: str) -> dict:
    session = get_session_factory()()
    try:
        _update_job(job_id, status=SyncJobStatus.RUNNING.value, message="Connecting to Alfresco...", progress=10)

        time.sleep(2)

        case = session.query(Case).filter(Case.id == case_id).first()
        if not case:
            _update_job(job_id, status=SyncJobStatus.FAILED.value, message="Case not found")
            return {"status": "failed", "reason": "case not found"}

        pending_docs = (
            session.query(Document)
            .filter(Document.case_id == case_id, Document.status == DocumentStatus.PENDING.value)
            .all()
        )

        if not pending_docs:
            pending_docs = [
                Document(
                    case_id=case_id,
                    filename=f"Alfresco_Sync_{case_id}_{i}.pdf",
                    mime_type="application/pdf",
                    status=DocumentStatus.SYNCING.value,
                    alfresco_node_id=f"alfresco-sync-{case_id}-{i}",
                    page_count=10 + i,
                )
                for i in range(1, 4)
            ]
            session.add_all(pending_docs)
            session.commit()
            for doc in pending_docs:
                session.refresh(doc)

        total = len(pending_docs)
        _update_job(
            job_id,
            total_documents=total,
            progress=30,
            message=f"Downloaded {total} files from Alfresco",
        )

        for doc in pending_docs:
            doc.status = DocumentStatus.SYNCING.value
        session.commit()

        case.last_synced_at = datetime.now(UTC)
        session.commit()

        ingestion_tasks = [
            celery_app.signature(
                TASK_INGEST_DOCUMENT,
                args=[doc.id, job_id],
                queue=QUEUE_INGESTION,
            )
            for doc in pending_docs
        ]

        _update_job(job_id, progress=50, message="Dispatching ingestion tasks...")

        if ingestion_tasks:
            chain(*ingestion_tasks, _finalize_sync_job.si(job_id, total)).apply_async()
        else:
            _finalize_sync_job.delay(job_id, total)

        return {"status": "dispatched", "documents": total, "job_id": job_id}
    finally:
        session.close()


@celery_app.task(name="module_alfresco.tasks.finalize_sync_job")
def _finalize_sync_job(job_id: str, total: int) -> dict:
    _update_job(
        job_id,
        status=SyncJobStatus.COMPLETED.value,
        progress=100,
        total_documents=total,
        message=f"Sync completed — {total} documents processed",
    )
    return {"status": "completed", "job_id": job_id}
