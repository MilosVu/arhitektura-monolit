"""Chat agent — RAG + law citation (LangGraph stub)."""

from cortex_core.agents.state import AgentState

from module_ai.agents.base import BaseLangGraphAgent
from module_ai.services.llm_router import LiteLLMRouter


class ChatAgent(BaseLangGraphAgent):
    name = "chat-agent"

    def __init__(self, llm: LiteLLMRouter | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._llm = llm or LiteLLMRouter()

    def build_graph(self) -> dict:
        return {
            "nodes": ["load_checkpoint", "retrieve_rag", "retrieve_laws", "call_llm", "save_checkpoint"],
            "edges": [
                ("load_checkpoint", "retrieve_rag"),
                ("retrieve_rag", "retrieve_laws"),
                ("retrieve_laws", "call_llm"),
                ("call_llm", "save_checkpoint"),
            ],
        }

    async def invoke(self, state: AgentState) -> AgentState:
        # Stub tok — u produkciji svaki korak je LangGraph node
        _graph = self.build_graph()
        _ = _graph

        prior = self.load_checkpoint(state["thread_id"]) or {}
        messages = prior.get("messages", [])

        # TODO: RagAgent.retrieve + LawLinkAgent.resolve
        reply = (
            "Basierend auf den Dokumenten in diesem Fall scheint Klausel 3.2 relevant. "
            "Art. 41 OR (or-41) prüfen."
        )

        new_state: AgentState = {
            **state,
            "messages": messages + [{"role": "assistant", "content": reply}],
            "assistant_reply": reply,
            "law_refs": ["or-41"],
        }
        self.save_checkpoint(state["thread_id"], new_state)
        return new_state
