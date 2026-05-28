from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_platform.api import PlatformModule
from module_platform.deps import get_current_user, get_platform_module
from module_platform.models import User, get_db
from module_platform.schemas import SyncJobCreateResponse, SyncJobResponse

router = APIRouter(tags=["sync"])


@router.post("/cases/{case_id}/sync", response_model=SyncJobCreateResponse)
def trigger_sync(
    case_id: int,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return platform.trigger_sync(case_id, current_user, db)


@router.get("/sync/jobs/{job_id}", response_model=SyncJobResponse)
def get_sync_job(
    job_id: str,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return platform.get_sync_job(job_id, current_user, db)
