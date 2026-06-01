"""Factory za spoljne connectore — stub (default) ili prod (kasnije)."""

from __future__ import annotations

import os

from cortex_core.ports.alfresco import AlfrescoPort
from cortex_core.ports.ocr import OCRPort

from cortex_connectors.alfresco.stub_client import StubAlfrescoClient
from cortex_connectors.blob.port import BlobPort
from cortex_connectors.blob.stub_store import StubBlobStore
from cortex_connectors.ocr.stub_adapter import StubOCRAdapter

_CONNECTORS_MODE = os.getenv("CORTEX_CONNECTORS_MODE", "stub").lower()


def get_alfresco_client() -> AlfrescoPort:
    if _CONNECTORS_MODE != "stub":
        raise NotImplementedError(
            f"Prod Alfresco adapter not implemented (mode={_CONNECTORS_MODE})"
        )
    return StubAlfrescoClient()


def get_blob_store() -> BlobPort:
    if _CONNECTORS_MODE != "stub":
        raise NotImplementedError(
            f"Prod Blob adapter not implemented (mode={_CONNECTORS_MODE})"
        )
    return StubBlobStore()


def get_ocr_adapter() -> OCRPort:
    if _CONNECTORS_MODE != "stub":
        raise NotImplementedError(
            f"Prod OCR adapter not implemented (mode={_CONNECTORS_MODE})"
        )
    return StubOCRAdapter()
