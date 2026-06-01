from typing import Annotated

from cortex_models import User, get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_platform.api import PlatformModule
from module_platform.deps import get_current_user, get_platform_module
from module_platform.schemas import AuditLogResponse

router = APIRouter(tags=["audit"])


@router.get("/audit-logs", response_model=list[AuditLogResponse])
def list_audit_logs(
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    limit: int = 50,
):
    return platform.list_audit_logs(current_user, db, limit)
