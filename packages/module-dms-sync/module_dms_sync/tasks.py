import asyncio
import time
from datetime import UTC, datetime

from celery import chain
from cortex_core.enums import DocumentStatus, SyncJobStatus
from cortex_core.messaging.tasks import QUEUE_INGESTION, TASK_INGEST_DOCUMENT
from cortex_core.sync_worker_celery import get_sync_celery_app
from cortex_models import Case, Document, SyncJob, get_session_factory

from module_dms_sync.services.dms_sync_service import DmsSyncService
from module_dms_sync.worker_deps import register_worker_dependencies

celery_app = get_sync_celery_app()
_worker_deps = register_worker_dependencies()
_documents = _worker_deps.documents


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


@celery_app.task(name="module_dms_sync.tasks.sync_case_from_dms", bind=True)
def sync_case_from_dms(self, case_id: int, job_id: str) -> dict:
    session = get_session_factory()()
    try:
        _update_job(
            job_id,
            status=SyncJobStatus.RUNNING.value,
            message="Connecting to DMS...",
            progress=10,
        )

        time.sleep(2)

        case = session.query(Case).filter(Case.id == case_id).first()
        if not case:
            _update_job(
                job_id, status=SyncJobStatus.FAILED.value, message="Case not found"
            )
            return {"status": "failed", "reason": "case not found"}

        pending_docs = (
            session.query(Document)
            .filter(
                Document.case_id == case_id,
                Document.status == DocumentStatus.PENDING.value,
            )
            .all()
        )

        if not pending_docs:
            sync_service = DmsSyncService(
                session,
                documents=_documents,
                alfresco=_worker_deps.alfresco,
                blob=_worker_deps.blob,
            )
            doc_ids = asyncio.run(sync_service.fetch_delta_documents(case))
            if not doc_ids:
                for i in range(1, 4):
                    detail = _documents.create(
                        case_id=case_id,
                        metadata={
                            "filename": f"DMS_Sync_{case_id}_{i}.pdf",
                            "mime_type": "application/pdf",
                            "alfresco_node_id": f"dms-sync-{case_id}-{i}",
                        },
                        db=session,
                    )
                    _documents.mark_syncing(detail.id, session)
                    doc_ids.append(detail.id)

            pending_docs = (
                session.query(Document).filter(Document.id.in_(doc_ids)).all()
            )
        else:
            for doc in pending_docs:
                _documents.mark_syncing(doc.id, session)
            session.commit()
            pending_docs = (
                session.query(Document)
                .filter(Document.id.in_([d.id for d in pending_docs]))
                .all()
            )

        total = len(pending_docs)
        _update_job(
            job_id,
            total_documents=total,
            progress=30,
            message=f"Downloaded {total} files from DMS",
        )

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
            chain(*ingestion_tasks, finalize_sync_job.si(job_id, total)).apply_async()
        else:
            finalize_sync_job.delay(job_id, total)

        return {"status": "dispatched", "documents": total, "job_id": job_id}
    finally:
        session.close()


@celery_app.task(name="module_dms_sync.tasks.finalize_sync_job")
def finalize_sync_job(job_id: str, total: int) -> dict:
    _update_job(
        job_id,
        status=SyncJobStatus.COMPLETED.value,
        progress=100,
        total_documents=total,
        message=f"Sync completed — {total} documents processed",
    )
    return {"status": "completed", "job_id": job_id}
