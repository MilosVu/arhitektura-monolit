"""Worker composition root — deljene zavisnosti za Celery taskove."""

from __future__ import annotations

from dataclasses import dataclass

from cortex_connectors import get_alfresco_client, get_blob_store
from cortex_connectors.blob.port import BlobPort
from cortex_core.ports.alfresco import AlfrescoPort
from module_documents.api import DocumentsModule
from module_documents.factory import create_documents_module


@dataclass(frozen=True)
class DmsSyncWorkerDeps:
    documents: DocumentsModule
    alfresco: AlfrescoPort
    blob: BlobPort


def register_worker_dependencies() -> DmsSyncWorkerDeps:
    return DmsSyncWorkerDeps(
        documents=create_documents_module(),
        alfresco=get_alfresco_client(),
        blob=get_blob_store(),
    )
