"""LawLink agent — Neo4j graph lookup + citation."""

from cortex_core.agents.state import AgentState

from module_ai.agents.base import BaseLangGraphAgent
from module_ai.services.neo4j_store import get_law_by_ref


class LawLinkAgent(BaseLangGraphAgent):
    name = "law-link-agent"

    def build_graph(self) -> dict:
        return {
            "nodes": ["parse_citations", "neo4j_lookup", "validate_temporal"],
            "edges": [],
        }

    async def invoke(self, state: AgentState) -> AgentState:
        refs = state.get("law_refs", ["or-41"])
        laws = []
        for ref in refs:
            law = get_law_by_ref(ref)
            if law:
                laws.append(law.model_dump())
        return {**state, "retrieved_laws": laws}
