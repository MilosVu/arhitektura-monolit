from typing import Annotated

from cortex_models import User, get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_sync.api import SyncModule
from module_sync.deps import get_current_user, get_sync_module
from module_sync.schemas import SyncJobCreateResponse, SyncJobResponse

router = APIRouter(tags=["sync"])


@router.post("/cases/{case_id}/sync", response_model=SyncJobCreateResponse)
def trigger_sync(
    case_id: int,
    sync: Annotated[SyncModule, Depends(get_sync_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return sync.trigger_sync(case_id, current_user, db)


@router.get("/sync/jobs/{job_id}", response_model=SyncJobResponse)
def get_sync_job(
    job_id: str,
    sync: Annotated[SyncModule, Depends(get_sync_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return sync.get_job(job_id, current_user, db)
