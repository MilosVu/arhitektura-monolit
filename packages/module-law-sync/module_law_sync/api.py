"""Public facade for the law corpus sync domain module."""

from cortex_core.enums import LawSyncJobStatus
from cortex_models import LawSyncJob
from fastapi import HTTPException
from sqlalchemy.orm import Session

from module_law_sync.schemas import (
    LawSyncJobCreateRequest,
    LawSyncJobCreateResponse,
    LawSyncJobResponse,
)
from module_law_sync.sync_trigger import enqueue_law_sync_job


class LawSyncModule:
    """In-process facade for law sync job trigger and polling."""

    def trigger_sync(
        self, body: LawSyncJobCreateRequest, db: Session
    ) -> LawSyncJobCreateResponse:
        job = LawSyncJob(
            scope=body.scope,
            status=LawSyncJobStatus.PENDING.value,
            message="Queued for law corpus sync",
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        enqueue_law_sync_job(job_id=job.id, scope=body.scope)
        return LawSyncJobCreateResponse(job_id=job.id)

    def get_job(self, job_id: str, db: Session) -> LawSyncJobResponse:
        job = db.query(LawSyncJob).filter(LawSyncJob.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Law sync job not found")
        return LawSyncJobResponse.model_validate(job)
