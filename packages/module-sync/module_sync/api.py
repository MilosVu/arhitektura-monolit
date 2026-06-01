"""Public facade for the sync domain module."""

from cortex_core.errors import ForbiddenError
from cortex_models import Case, User
from fastapi import HTTPException
from sqlalchemy.orm import Session

from module_sync.schemas import SyncJobCreateResponse, SyncJobResponse
from module_sync.services import SyncOrchestrator


class SyncModule:
    """In-process facade for sync job trigger and polling."""

    def _assert_case_access(self, case_id: int, user: User, db: Session) -> Case:
        case = (
            db.query(Case).filter(Case.id == case_id, Case.owner_id == user.id).first()
        )
        if not case:
            raise ForbiddenError(f"Case {case_id} not accessible")
        return case

    def trigger_sync(
        self, case_id: int, user: User, db: Session
    ) -> SyncJobCreateResponse:
        try:
            case = self._assert_case_access(case_id, user, db)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

        job = SyncOrchestrator(db).trigger_sync(case, user)
        return SyncJobCreateResponse(job_id=job.id)

    def get_job(self, job_id: str, user: User, db: Session) -> SyncJobResponse:
        job = SyncOrchestrator(db).get_job_for_user(job_id, user)
        if not job:
            raise HTTPException(status_code=404, detail="Sync job not found")
        return SyncJobResponse.model_validate(job)
