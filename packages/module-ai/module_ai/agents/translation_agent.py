"""Translation agent — split-screen prevod."""

from cortex_core.agents.state import AgentState
from cortex_core.ports.llm import LLMMessage

from module_ai.agents.base import BaseLangGraphAgent
from module_ai.services.llm_router import LiteLLMRouter


class TranslationAgent(BaseLangGraphAgent):
    name = "translation-agent"

    def __init__(self, llm: LiteLLMRouter | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._llm = llm or LiteLLMRouter()

    def build_graph(self) -> dict:
        return {"nodes": ["extract_text", "translate", "format_output"], "edges": []}

    async def invoke(self, state: AgentState) -> AgentState:
        text = state.get("user_message", "")
        result = await self._llm.complete(
            [
                LLMMessage(role="system", content="Du bist ein juristischer Übersetzer."),
                LLMMessage(role="user", content=text),
            ]
        )
        return {**state, "assistant_reply": result.text}
