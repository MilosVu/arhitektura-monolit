"""Port ka Alfresco ECM — implementacija u sync-worker adapteru."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AlfrescoDocumentRef:
    node_id: str
    filename: str
    mime_type: str
    modified_at: datetime
    case_folder_id: str


class AlfrescoPort(ABC):
    """Interfejs prema klijentskom Alfresco (on-prem)."""

    @abstractmethod
    async def list_changed_since(
        self,
        case_folder_id: str,
        since: datetime | None,
    ) -> list[AlfrescoDocumentRef]:
        """Delta sync — samo novi/izmenjeni nodovi od last_synced_at."""

    @abstractmethod
    async def download_binary(self, node_id: str) -> bytes:
        """Preuzmi sirovi fajl za ingestion pipeline."""

    @abstractmethod
    async def ping(self) -> bool:
        """Health check Alfresco veze."""
