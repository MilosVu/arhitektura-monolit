"""RAG agent — Weaviate BM25 retrieval."""

from dataclasses import asdict

from cortex_core.agents.state import AgentState

from module_ai.adapters.weaviate_store import WeaviateSearchStore
from module_ai.agents.base import BaseLangGraphAgent


class RagAgent(BaseLangGraphAgent):
    name = "rag-agent"

    def __init__(self, search: WeaviateSearchStore | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._search = search or WeaviateSearchStore()

    def build_graph(self) -> dict:
        return {"nodes": ["embed_query", "bm25_search", "rerank"], "edges": []}

    async def invoke(self, state: AgentState) -> AgentState:
        query = state.get("user_message", "")
        case_id = state.get("case_id", 0)
        chunks = self._search.search_chunks(query, case_id=case_id, limit=5)
        return {
            **state,
            "retrieved_chunks": [asdict(c) for c in chunks],
        }
