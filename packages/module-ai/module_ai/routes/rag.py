from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_platform.models import User, get_db
from module_ai.routes.deps import get_current_user, get_platform_module
from module_ai.schemas import RagSearchRequest, RagSearchResponse

router = APIRouter(tags=["rag"])


@router.post("/cases/{case_id}/search", response_model=RagSearchResponse)
def search_case_documents(
    case_id: int,
    body: RagSearchRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    platform: Annotated[object, Depends(get_platform_module)],
):
    return platform.search_case_documents(case_id, body, current_user, db)
