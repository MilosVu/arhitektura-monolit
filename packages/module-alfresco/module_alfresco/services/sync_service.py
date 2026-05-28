"""Domain servis — Alfresco delta sync (I/O bound)."""

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from cortex_core.base.service import BaseService
from cortex_core.enums import DocumentStatus, SyncJobStatus
from cortex_core.infrastructure.redis.sync_progress import SyncProgressPublisher
from module_alfresco.models import Case, Document, SyncJob
from module_alfresco.adapters.alfresco_client import StubAlfrescoClient


class SyncService(BaseService):
    """
    Koraci:
      1. učitaj case.last_synced_at
      2. AlfrescoPort.list_changed_since(delta)
      3. upiši Document redove u PostgreSQL
      4. enqueue ingestion taskove
      5. SyncProgressPublisher.publish(progress)
    """

    def __init__(
        self,
        session: Session,
        alfresco: StubAlfrescoClient | None = None,
        progress: SyncProgressPublisher | None = None,
    ) -> None:
        self._session = session
        self._alfresco = alfresco or StubAlfrescoClient()
        self._progress = progress or SyncProgressPublisher()

    async def fetch_delta_documents(self, case: Case) -> list[Document]:
        refs = await self._alfresco.list_changed_since(
            case_folder_id=case.case_number,
            since=case.last_synced_at,
        )
        docs: list[Document] = []
        for ref in refs:
            doc = Document(
                case_id=case.id,
                filename=ref.filename,
                mime_type=ref.mime_type,
                status=DocumentStatus.SYNCING.value,
                alfresco_node_id=ref.node_id,
            )
            self._session.add(doc)
            docs.append(doc)
        self._session.commit()
        return docs

    def update_job_status(self, job: SyncJob, *, progress: int, message: str, status: str | None = None) -> None:
        job.progress = progress
        job.message = message
        if status:
            job.status = status
        job.updated_at = datetime.now(UTC)
        self._session.commit()
        self._progress.publish(job.id, progress=progress, message=message, status=job.status)
