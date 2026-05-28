from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_platform.api import PlatformModule
from module_platform.deps import get_current_user, get_platform_module
from module_platform.models import User, get_db
from module_platform.schemas import DocumentDetail, DocumentSummary

router = APIRouter(tags=["documents"])


@router.get("/cases/{case_id}/documents", response_model=list[DocumentSummary])
def list_documents(
    case_id: int,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return platform.list_documents(case_id, current_user, db)


@router.get("/documents/{document_id}", response_model=DocumentDetail)
def get_document(
    document_id: int,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return platform.get_document(document_id, current_user, db)
