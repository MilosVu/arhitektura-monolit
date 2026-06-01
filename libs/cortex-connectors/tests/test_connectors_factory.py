"""Factory vraća stub implementacije u default modu."""

from cortex_connectors import (
    StubAlfrescoClient,
    StubBlobStore,
    StubOCRAdapter,
    get_alfresco_client,
    get_blob_store,
    get_ocr_adapter,
)


def test_factory_returns_stubs_by_default(monkeypatch) -> None:
    monkeypatch.delenv("CORTEX_CONNECTORS_MODE", raising=False)
    assert isinstance(get_alfresco_client(), StubAlfrescoClient)
    assert isinstance(get_blob_store(), StubBlobStore)
    assert isinstance(get_ocr_adapter(), StubOCRAdapter)


def test_factory_stub_mode_explicit(monkeypatch) -> None:
    monkeypatch.setenv("CORTEX_CONNECTORS_MODE", "stub")
    assert isinstance(get_alfresco_client(), StubAlfrescoClient)
