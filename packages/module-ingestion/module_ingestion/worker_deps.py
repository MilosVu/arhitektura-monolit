"""Worker composition root — deljene zavisnosti za Celery taskove."""

from __future__ import annotations

from dataclasses import dataclass

from cortex_connectors import get_ocr_adapter
from cortex_core.ports.ocr import OCRPort
from module_documents.api import DocumentsModule
from module_documents.factory import create_documents_module

from module_ingestion.adapters.weaviate_store import WeaviateSearchAdapter


@dataclass(frozen=True)
class IngestionWorkerDeps:
    documents: DocumentsModule
    ocr: OCRPort
    search: WeaviateSearchAdapter


def register_worker_dependencies() -> IngestionWorkerDeps:
    return IngestionWorkerDeps(
        documents=create_documents_module(),
        ocr=get_ocr_adapter(),
        search=WeaviateSearchAdapter(),
    )
