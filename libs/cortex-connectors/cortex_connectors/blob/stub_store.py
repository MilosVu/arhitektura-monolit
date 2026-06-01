"""Blob storage stub — drži mock path-ove u memoriji."""

from cortex_connectors.blob.port import BlobPort


class StubBlobStore(BlobPort):
    """MVP stub — simulira blob storage bez pravog backend-a."""

    def __init__(self) -> None:
        self._paths: dict[str, bytes] = {}

    async def put(self, key: str, content: bytes) -> str:
        path = f"blob://mock/{key}"
        self._paths[path] = content
        return path

    async def get(self, path: str) -> bytes:
        return self._paths.get(path, b"")

    async def delete(self, path: str) -> None:
        self._paths.pop(path, None)
