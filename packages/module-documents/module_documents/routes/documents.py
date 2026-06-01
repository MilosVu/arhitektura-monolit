from typing import Annotated

from cortex_models import User, get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from module_documents.api import DocumentsModule
from module_documents.deps import get_current_user, get_documents_module
from module_documents.schemas import DocumentDetail, DocumentSummary, ReingestResponse

router = APIRouter(tags=["documents"])


@router.get("/cases/{case_id}/documents", response_model=list[DocumentSummary])
def list_documents(
    case_id: int,
    documents: Annotated[DocumentsModule, Depends(get_documents_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return documents.list_by_case(case_id, current_user, db)


@router.get("/documents/{document_id}", response_model=DocumentDetail)
def get_document(
    document_id: int,
    documents: Annotated[DocumentsModule, Depends(get_documents_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return documents.get(document_id, current_user, db)


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    documents: Annotated[DocumentsModule, Depends(get_documents_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    documents.delete(document_id, current_user, db)


@router.post("/documents/{document_id}/reingest", response_model=ReingestResponse)
def reingest_document(
    document_id: int,
    documents: Annotated[DocumentsModule, Depends(get_documents_module)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return documents.trigger_reingest(document_id, current_user, db)
