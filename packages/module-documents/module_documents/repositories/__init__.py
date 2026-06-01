"""Legacy — koristi module_documents.adapters."""

from module_documents.adapters.postgres_document_repository import (
    PostgresDocumentRepository as DocumentRepository,
)

__all__ = ["DocumentRepository"]
