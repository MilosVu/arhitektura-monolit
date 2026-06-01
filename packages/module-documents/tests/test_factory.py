"""Unit testovi za DocumentsModule factory."""

from module_documents.api import DocumentsModule
from module_documents.factory import create_documents_module
from module_documents.services.document_service import DocumentService


def test_create_documents_module_returns_facade() -> None:
    module = create_documents_module()
    assert isinstance(module, DocumentsModule)


def test_create_documents_module_has_document_service() -> None:
    module = create_documents_module()
    assert isinstance(module._service, DocumentService)
