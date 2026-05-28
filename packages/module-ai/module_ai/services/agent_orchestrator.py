"""Orkestrator — bira agenta po tipu zahteva."""

from collections.abc import AsyncIterator

from cortex_core.agents.state import AgentState

from module_ai.agents.chat_agent import ChatAgent
from module_ai.agents.law_link_agent import LawLinkAgent
from module_ai.agents.rag_agent import RagAgent
from module_ai.agents.translation_agent import TranslationAgent


class AgentOrchestrator:
    """
    Jedinstvena ulazna tačka za ai-agents servis.

    Gateway zove orchestrator preko HTTP; orchestrator delegira agentu.
    """

    def __init__(self) -> None:
        self._chat = ChatAgent()
        self._translation = TranslationAgent()
        self._rag = RagAgent()
        self._law_link = LawLinkAgent()

    async def run_chat(self, *, thread_id: str, case_id: int, user_id: int, message: str) -> AgentState:
        state: AgentState = {
            "thread_id": thread_id,
            "case_id": case_id,
            "user_id": user_id,
            "user_message": message,
        }
        return await self._chat.invoke(state)

    async def stream_chat(
        self, *, thread_id: str, case_id: int, user_id: int, message: str
    ) -> AsyncIterator[str]:
        state: AgentState = {
            "thread_id": thread_id,
            "case_id": case_id,
            "user_id": user_id,
            "user_message": message,
        }
        async for token in self._chat.stream(state):
            yield token

    async def run_translation(self, text: str, target_lang: str) -> str:
        state: AgentState = {"user_message": text, "target_lang": target_lang}
        result = await self._translation.invoke(state)
        return result.get("assistant_reply", "")

    async def run_rag_search(self, query: str, case_id: int) -> AgentState:
        return await self._rag.invoke({"user_message": query, "case_id": case_id})

    async def run_law_lookup(self, law_ref: str) -> AgentState:
        return await self._law_link.invoke({"law_refs": [law_ref]})
