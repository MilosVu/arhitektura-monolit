"""Weaviate read path — AI module owns RAG search via SearchPort."""

import logging

import weaviate.classes.query as wq
from cortex_core.infrastructure.weaviate.client import get_weaviate_client
from cortex_core.infrastructure.weaviate.collection import (
    COLLECTION_NAME,
    ensure_collection,
)
from cortex_core.ports.search import ChunkHit, SearchPort

logger = logging.getLogger(__name__)


class WeaviateSearchStore(SearchPort):
    """SearchPort read side — BM25 retrieval for RAG."""

    def search_chunks(
        self,
        query: str,
        case_id: int | None = None,
        limit: int = 5,
    ) -> list[ChunkHit]:
        try:
            ensure_collection()
            collection = get_weaviate_client().collections.get(COLLECTION_NAME)

            filters = None
            if case_id is not None:
                filters = wq.Filter.by_property("case_id").equal(case_id)

            response = collection.query.bm25(
                query=query,
                limit=limit,
                filters=filters,
                return_metadata=wq.MetadataQuery(score=True),
            )

            results: list[ChunkHit] = []
            for obj in response.objects:
                props = obj.properties
                score = (
                    obj.metadata.score if obj.metadata and obj.metadata.score else 0.0
                )
                results.append(
                    ChunkHit(
                        document_id=int(props.get("document_id", 0)),
                        filename=str(props.get("filename", "")),
                        content=str(props.get("content", "")),
                        score=float(score),
                    )
                )
            return results
        except Exception as exc:
            logger.warning("Weaviate search failed: %s", exc)
            return []

    def upsert_document_chunks(
        self,
        document_id: int,
        case_id: int,
        filename: str,
        chunks: list[str],
    ) -> int:
        raise NotImplementedError("Write path is owned by module-ingestion")


_default_store = WeaviateSearchStore()


def search_chunks(
    query: str, case_id: int | None = None, limit: int = 5
) -> list[ChunkHit]:
    return _default_store.search_chunks(query, case_id=case_id, limit=limit)
