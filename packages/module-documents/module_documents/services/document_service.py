"""Use-case logika za dokumente."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from cortex_core.celery_app import create_celery_app
from cortex_core.enums import DocumentStatus
from cortex_core.errors import DocumentNotFoundError, ForbiddenError
from cortex_core.messaging.tasks import QUEUE_INGESTION, TASK_INGEST_DOCUMENT
from cortex_models import Document, User
from sqlalchemy.orm import Session

from module_documents.ports.document_repository_port import DocumentRepositoryPort
from module_documents.schemas import DocumentDetail, DocumentSummary, ReingestResponse

_producer_app = create_celery_app("cortex_server")


class DocumentService:
    """Document CRUD i lifecycle — zavisi od DocumentRepositoryPort."""

    def __init__(
        self,
        repo_factory: Callable[[Session], DocumentRepositoryPort],
    ) -> None:
        self._repo_factory = repo_factory

    def list_by_case(
        self, case_id: int, user: User, db: Session
    ) -> list[DocumentSummary]:
        repo = self._repo_factory(db)
        if not repo.get_case_for_owner(case_id, user.id):
            raise ForbiddenError(f"Case {case_id} not accessible")
        docs = repo.list_by_case(case_id)
        return [DocumentSummary.model_validate(d) for d in docs]

    def get(self, document_id: int, user: User, db: Session) -> DocumentDetail:
        doc = self._repo_factory(db).get_owned_document(document_id, user.id)
        if not doc:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        return DocumentDetail.model_validate(doc)

    def create(
        self, case_id: int, metadata: dict[str, Any], db: Session
    ) -> DocumentDetail:
        doc = Document(
            case_id=case_id,
            filename=metadata.get("filename", "unknown"),
            mime_type=metadata.get("mime_type", "application/pdf"),
            alfresco_node_id=metadata.get("alfresco_node_id"),
            status=DocumentStatus.PENDING.value,
        )
        saved = self._repo_factory(db).save(doc)
        return DocumentDetail.model_validate(saved)

    def delete(self, document_id: int, user: User, db: Session) -> None:
        repo = self._repo_factory(db)
        doc = repo.get_owned_document(document_id, user.id)
        if not doc:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        repo.delete(doc)

    def trigger_reingest(
        self, document_id: int, user: User, db: Session
    ) -> ReingestResponse:
        doc = self._repo_factory(db).get_owned_document(document_id, user.id)
        if not doc:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        _producer_app.send_task(
            TASK_INGEST_DOCUMENT,
            args=[doc.id, ""],
            queue=QUEUE_INGESTION,
        )
        return ReingestResponse(document_id=doc.id)

    def mark_syncing(self, document_id: int, db: Session) -> None:
        self._update_status(document_id, DocumentStatus.SYNCING, db)

    def mark_ingesting(self, document_id: int, db: Session) -> None:
        self._update_status(document_id, DocumentStatus.INGESTING, db)

    def mark_ready(
        self, document_id: int, db: Session, *, page_count: int | None = None
    ) -> None:
        repo = self._repo_factory(db)
        doc = repo.get_by_id(document_id)
        if not doc:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        doc.status = DocumentStatus.READY.value
        if page_count is not None:
            doc.page_count = page_count
        doc.updated_at = datetime.now(UTC)
        repo.save(doc)

    def mark_failed(self, document_id: int, _reason: str, db: Session) -> None:
        repo = self._repo_factory(db)
        doc = repo.get_by_id(document_id)
        if not doc:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        doc.status = DocumentStatus.FAILED.value
        doc.updated_at = datetime.now(UTC)
        repo.save(doc)

    def _update_status(
        self, document_id: int, status: DocumentStatus, db: Session
    ) -> None:
        repo = self._repo_factory(db)
        doc = repo.get_by_id(document_id)
        if not doc:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        doc.status = status.value
        doc.updated_at = datetime.now(UTC)
        repo.save(doc)
