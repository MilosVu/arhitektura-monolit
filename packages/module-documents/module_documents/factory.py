"""Factory za DocumentsModule — HTTP i Celery composition root."""

from __future__ import annotations

from module_documents.adapters.postgres_document_repository import (
    PostgresDocumentRepository,
)
from module_documents.api import DocumentsModule
from module_documents.services.document_service import DocumentService


def create_documents_module() -> DocumentsModule:
    """Kreira facade sa podrazumevanim Postgres adapterom."""
    service = DocumentService(repo_factory=PostgresDocumentRepository)
    return DocumentsModule(service=service)
