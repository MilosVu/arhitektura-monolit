"""Shared Weaviate collection bootstrap (connection stays in client.py)."""

import logging

import weaviate.classes.config as wc

from cortex_core.infrastructure.weaviate.client import get_weaviate_client

logger = logging.getLogger(__name__)

COLLECTION_NAME = "DocumentChunk"


def ensure_collection() -> None:
    client = get_weaviate_client()
    if client.collections.exists(COLLECTION_NAME):
        return
    client.collections.create(
        name=COLLECTION_NAME,
        vectorizer_config=wc.Configure.Vectorizer.none(),
        properties=[
            wc.Property(name="document_id", data_type=wc.DataType.INT),
            wc.Property(name="case_id", data_type=wc.DataType.INT),
            wc.Property(name="filename", data_type=wc.DataType.TEXT),
            wc.Property(name="content", data_type=wc.DataType.TEXT),
        ],
    )
    logger.info("Created Weaviate collection %s", COLLECTION_NAME)
