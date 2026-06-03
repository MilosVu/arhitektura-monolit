from typing import Annotated

from cortex_models import User, get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_law_sync.api import LawSyncModule
from module_law_sync.deps import get_current_user, get_law_sync_module
from module_law_sync.schemas import (
    LawSyncJobCreateRequest,
    LawSyncJobCreateResponse,
    LawSyncJobResponse,
)

router = APIRouter(prefix="/law-sync", tags=["law-sync"])


@router.post("/jobs", response_model=LawSyncJobCreateResponse)
def trigger_law_sync(
    body: LawSyncJobCreateRequest,
    law_sync: Annotated[LawSyncModule, Depends(get_law_sync_module)],
    _current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return law_sync.trigger_sync(body, db)


@router.get("/jobs/{job_id}", response_model=LawSyncJobResponse)
def get_law_sync_job(
    job_id: str,
    law_sync: Annotated[LawSyncModule, Depends(get_law_sync_module)],
    _current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return law_sync.get_job(job_id, db)
