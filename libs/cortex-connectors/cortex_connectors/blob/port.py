"""Port ka object/blob storage — implementacija u sync-worker adapteru."""

from abc import ABC, abstractmethod


class BlobPort(ABC):
    """Interfejs prema blob storage-u (S3, Azure Blob, lokalni disk)."""

    @abstractmethod
    async def put(self, key: str, content: bytes) -> str:
        """Sačuvaj sadržaj i vrati storage path."""

    @abstractmethod
    async def get(self, path: str) -> bytes:
        """Učitaj sadržaj sa storage path-a."""

    @abstractmethod
    async def delete(self, path: str) -> None:
        """Obriši objekat sa datog path-a."""
