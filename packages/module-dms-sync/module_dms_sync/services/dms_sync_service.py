"""Domain servis — DMS delta sync (I/O bound)."""

from datetime import UTC, datetime

from cortex_connectors import get_alfresco_client, get_blob_store
from cortex_connectors.blob.port import BlobPort
from cortex_core.base.service import BaseService
from cortex_core.infrastructure.redis.sync_progress import SyncProgressPublisher
from cortex_core.ports.alfresco import AlfrescoPort
from cortex_models import Case, SyncJob
from module_documents.api import DocumentsModule
from module_documents.factory import create_documents_module
from sqlalchemy.orm import Session


class DmsSyncService(BaseService):
    """
    Koraci:
      1. učitaj case.last_synced_at
      2. AlfrescoPort.list_changed_since(delta)
      3. upiši Document redove preko DocumentsModule.create()
      4. download u BlobPort
      5. mark_syncing() preko DocumentsModule
      6. SyncProgressPublisher.publish(progress)
    """

    def __init__(
        self,
        session: Session,
        documents: DocumentsModule | None = None,
        alfresco: AlfrescoPort | None = None,
        blob: BlobPort | None = None,
        progress: SyncProgressPublisher | None = None,
    ) -> None:
        self._session = session
        self._documents = documents or create_documents_module()
        self._alfresco = alfresco or get_alfresco_client()
        self._blob = blob or get_blob_store()
        self._progress = progress or SyncProgressPublisher()

    async def fetch_delta_documents(self, case: Case) -> list[int]:
        refs = await self._alfresco.list_changed_since(
            case_folder_id=case.case_number,
            since=case.last_synced_at,
        )
        doc_ids: list[int] = []
        for ref in refs:
            detail = self._documents.create(
                case_id=case.id,
                metadata={
                    "filename": ref.filename,
                    "mime_type": ref.mime_type,
                    "alfresco_node_id": ref.node_id,
                },
                db=self._session,
            )
            content = await self._alfresco.download_binary(ref.node_id)
            await self._blob.put(f"{case.id}/{ref.node_id}", content)
            self._documents.mark_syncing(detail.id, self._session)
            doc_ids.append(detail.id)
        return doc_ids

    def update_job_status(
        self, job: SyncJob, *, progress: int, message: str, status: str | None = None
    ) -> None:
        job.progress = progress
        job.message = message
        if status:
            job.status = status
        job.updated_at = datetime.now(UTC)
        self._session.commit()
        self._progress.publish(
            job.id, progress=progress, message=message, status=job.status
        )
