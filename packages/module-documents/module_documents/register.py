"""DI registracija za module-documents."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry

from module_documents.api import DocumentsModule
from module_documents.factory import create_documents_module
from module_documents.services.document_service import DocumentService


def register_services(
    registry: ServiceRegistry,
    *,
    documents_module: DocumentsModule | None = None,
) -> DocumentsModule:
    module = documents_module or create_documents_module()
    registry.register(DocumentsModule, module)
    registry.register(DocumentService, module._service)
    return module
