"""Sync orchestration — enqueue Celery + audit log."""

from cortex_core.base.service import BaseService
from cortex_core.enums import SyncJobStatus
from cortex_models import AuditLog, Case, SyncJob, User
from sqlalchemy.orm import Session

from module_sync.sync_trigger import enqueue_sync_job


class SyncOrchestrator(BaseService):
    """
    Gateway ne radi sync sam — delegira sync-worker-u preko RabbitMQ.

    Flow:
      trigger_sync -> SyncJob(PENDING) -> enqueue_sync_job -> sync-worker
    """

    def __init__(self, db: Session) -> None:
        self._db = db

    def trigger_sync(self, case: Case, user: User) -> SyncJob:
        job = SyncJob(
            case_id=case.id,
            status=SyncJobStatus.PENDING.value,
            message="Queued for Alfresco sync",
        )
        self._db.add(job)
        self._db.add(
            AuditLog(
                user_id=user.id,
                action="start_sync",
                resource_type="case",
                resource_id=str(case.id),
                details=f"Sync job {job.id} enqueued",
            )
        )
        self._db.commit()
        self._db.refresh(job)

        enqueue_sync_job(case_id=case.id, job_id=job.id)
        return job

    def get_job_for_user(self, job_id: str, user: User) -> SyncJob | None:
        return (
            self._db.query(SyncJob)
            .join(Case)
            .filter(SyncJob.id == job_id, Case.owner_id == user.id)
            .first()
        )
