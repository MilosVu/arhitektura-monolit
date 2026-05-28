"""Weaviate write path — ingestion module owns chunk upsert."""

import logging
import uuid

import weaviate.classes.query as wq

from cortex_core.infrastructure.weaviate.client import get_weaviate_client
from cortex_core.infrastructure.weaviate.collection import COLLECTION_NAME, ensure_collection

logger = logging.getLogger(__name__)


def upsert_document_chunks(
    document_id: int,
    case_id: int,
    filename: str,
    chunks: list[str],
) -> int:
    ensure_collection()
    collection = get_weaviate_client().collections.get(COLLECTION_NAME)

    collection.data.delete_many(
        where=wq.Filter.by_property("document_id").equal(document_id),
    )

    count = 0
    for i, chunk_text in enumerate(chunks):
        collection.data.insert(
            properties={
                "document_id": document_id,
                "case_id": case_id,
                "filename": filename,
                "content": chunk_text,
            },
            uuid=str(uuid.uuid5(uuid.NAMESPACE_DNS, f"doc-{document_id}-chunk-{i}")),
        )
        count += 1
    return count


def ping_weaviate() -> bool:
    from cortex_core.infrastructure.weaviate.client import ping_weaviate as _ping

    return _ping()
