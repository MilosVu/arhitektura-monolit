"""Public facade for the documents domain module."""

from __future__ import annotations

from typing import Any

from cortex_core.errors import DocumentNotFoundError, ForbiddenError
from cortex_models import User
from fastapi import HTTPException
from sqlalchemy.orm import Session

from module_documents.schemas import DocumentDetail, DocumentSummary, ReingestResponse
from module_documents.services.document_service import DocumentService


class DocumentsModule:
    """In-process facade — delegira na DocumentService."""

    def __init__(self, service: DocumentService) -> None:
        self._service = service

    def list_by_case(
        self, case_id: int, user: User, db: Session
    ) -> list[DocumentSummary]:
        try:
            return self._service.list_by_case(case_id, user, db)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

    def get(self, document_id: int, user: User, db: Session) -> DocumentDetail:
        try:
            return self._service.get(document_id, user, db)
        except DocumentNotFoundError:
            raise HTTPException(status_code=404, detail="Document not found") from None

    def create(
        self, case_id: int, metadata: dict[str, Any], db: Session
    ) -> DocumentDetail:
        return self._service.create(case_id, metadata, db)

    def delete(self, document_id: int, user: User, db: Session) -> None:
        try:
            self._service.delete(document_id, user, db)
        except DocumentNotFoundError:
            raise HTTPException(status_code=404, detail="Document not found") from None

    def trigger_reingest(
        self, document_id: int, user: User, db: Session
    ) -> ReingestResponse:
        try:
            return self._service.trigger_reingest(document_id, user, db)
        except DocumentNotFoundError:
            raise HTTPException(status_code=404, detail="Document not found") from None

    def mark_syncing(self, document_id: int, db: Session) -> None:
        self._service.mark_syncing(document_id, db)

    def mark_ingesting(self, document_id: int, db: Session) -> None:
        self._service.mark_ingesting(document_id, db)

    def mark_ready(
        self, document_id: int, db: Session, *, page_count: int | None = None
    ) -> None:
        self._service.mark_ready(document_id, db, page_count=page_count)

    def mark_failed(self, document_id: int, reason: str, db: Session) -> None:
        self._service.mark_failed(document_id, reason, db)
