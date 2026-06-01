"""
Bazni LangGraph agent — imitacija grafa bez stvarne langgraph zavisnosti.

U produkciji:
  from langgraph.graph import StateGraph
  graph = StateGraph(AgentState)
  graph.add_node("retrieve", self.retrieve_context)
  graph.add_edge(...)
  return graph.compile(checkpointer=RedisSaver(...))
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from cortex_core.agents.state import AgentState
from cortex_core.infrastructure.redis.agent_checkpoint import LangGraphCheckpointStore


class BaseLangGraphAgent(ABC):
    name: str = "base-agent"

    def __init__(
        self, checkpoint_store: LangGraphCheckpointStore | None = None
    ) -> None:
        self._checkpoints = checkpoint_store or LangGraphCheckpointStore()

    @abstractmethod
    def build_graph(self) -> object:
        """Vraća kompajlirani LangGraph — ovde stub dict sa node imenima."""

    @abstractmethod
    async def invoke(self, state: AgentState) -> AgentState:
        """Sinhroni prolaz kroz graf (prevod, RAG lookup)."""

    async def stream(self, state: AgentState) -> AsyncIterator[str]:
        """Streaming varijanta za chat SSE."""
        result = await self.invoke(state)
        text = result.get("assistant_reply", "")
        for token in text.split():
            yield token + " "

    def load_checkpoint(self, thread_id: str) -> AgentState | None:
        return self._checkpoints.load(thread_id)

    def save_checkpoint(self, thread_id: str, state: AgentState) -> None:
        self._checkpoints.save(thread_id, dict(state))
