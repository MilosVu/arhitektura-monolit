"""Public facade for the AI domain module."""

import asyncio
import json

from fastapi.responses import StreamingResponse

from module_ai.adapters.weaviate_store import search_chunks
from module_ai.schemas import (
    LawNodeResponse,
    RagChunk,
    RagSearchResponse,
    TranslateResponse,
)
from module_ai.services.neo4j_store import (
    get_law_by_ref,
    ping_neo4j,
    seed_laws_if_empty,
)

FALLBACK_RAG_CHUNKS = [
    RagChunk(
        document_id=1,
        filename="Klageerwiderung.pdf",
        content="Parteien vereinbaren hiermit einen Vertrag betreffend Lieferung und Zahlung.",
        score=0.5,
    ),
]


class AiModule:
    """In-process facade — replace with HTTP client when extracting to ai-agents service."""

    def seed_laws_on_startup(self) -> None:
        seed_laws_if_empty()

    def ping_neo4j(self) -> bool:
        return ping_neo4j()

    async def stream_chat(
        self, message: str, thread_id: str, case_id: int
    ) -> StreamingResponse:
        async def stream():
            chunks = [
                "Basierend auf den Dokumenten in diesem Fall ",
                "scheint Klausel 3.2 relevant zu sein. ",
                "Ich empfehle, Art. 41 OR (or-41) zu prüfen.",
            ]
            for chunk in chunks:
                payload = json.dumps({"content": chunk})
                yield f"data: {payload}\n\n"
                await asyncio.sleep(0.3)
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream(), media_type="text/event-stream")

    def translate(
        self,
        document_id: int,
        text: str,
        source_lang: str | None,
        target_lang: str,
    ) -> TranslateResponse:
        translated = (
            f"[MOCK TRANSLATION {source_lang or 'auto'} → {target_lang}]\n\n"
            f"{text}\n\n"
            "— Übersetzt durch Cortex Translation Agent (stub)"
        )
        return TranslateResponse(
            document_id=document_id,
            source_lang=source_lang or "de",
            target_lang=target_lang,
            translated_text=translated,
        )

    def rag_search(self, query: str, case_id: int, limit: int) -> RagSearchResponse:
        hits = search_chunks(query, case_id=case_id, limit=limit)
        chunks = [
            RagChunk(
                document_id=h.document_id,
                filename=h.filename,
                content=h.content,
                score=h.score,
            )
            for h in hits
        ]

        if not chunks:
            chunks = [
                RagChunk(
                    document_id=c.document_id,
                    filename=c.filename,
                    content=f"...fallback match for '{query}' — {c.content}",
                    score=c.score,
                )
                for c in FALLBACK_RAG_CHUNKS
            ]

        return RagSearchResponse(query=query, chunks=chunks[:limit])

    def lookup_law(self, law_ref: str) -> LawNodeResponse:
        law = get_law_by_ref(law_ref)
        if law:
            return law

        return LawNodeResponse(
            ref=law_ref,
            title="Unknown Law Reference",
            article=law_ref,
            content="No graph node found — run make seed-neo4j or restart cortex-server.",
            valid_from="2020-01-01",
        )
