"""Alfresco adapter — stub implementacija AlfrescoPort."""

from datetime import UTC, datetime

from cortex_core.ports.alfresco import AlfrescoDocumentRef, AlfrescoPort


class StubAlfrescoClient(AlfrescoPort):
    """MVP stub — simulira delta listu bez pravog Alfresco API-ja."""

    async def list_changed_since(
        self,
        case_folder_id: str,
        since: datetime | None,
    ) -> list[AlfrescoDocumentRef]:
        _ = since
        now = datetime.now(UTC)
        return [
            AlfrescoDocumentRef(
                node_id=f"alfresco-{case_folder_id}-1",
                filename="Sync_Doc_1.pdf",
                mime_type="application/pdf",
                modified_at=now,
                case_folder_id=case_folder_id,
            ),
        ]

    async def download_binary(self, node_id: str) -> bytes:
        return b"%PDF-1.4 mock content for " + node_id.encode()

    async def ping(self) -> bool:
        return True
