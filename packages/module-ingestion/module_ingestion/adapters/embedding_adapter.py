"""Embedding adapter — delegira StubLLMRouter iz cortex-core."""

from cortex_core.infrastructure.llm.stub_router import StubLLMRouter
from cortex_core.ports.llm import LLMPort


class EmbeddingAdapter:
    def __init__(self, llm: LLMPort | None = None) -> None:
        self._llm = llm or StubLLMRouter()

    async def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        return await self._llm.embed(chunks)
