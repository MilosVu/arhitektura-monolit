"""Stub LLM — deljen između ai-agents i ingestion-worker (bez cross-importa)."""

from collections.abc import AsyncIterator

from cortex_core.ports.llm import LLMCompletionResult, LLMMessage, LLMPort


class StubLLMRouter(LLMPort):
    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        model: str = "local/cortex-llm",
        temperature: float = 0.2,
    ) -> LLMCompletionResult:
        _ = temperature
        user_text = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return LLMCompletionResult(
            text=f"[MOCK {model}] {user_text[:200]}",
            model=model,
            prompt_tokens=len(user_text.split()),
            completion_tokens=42,
        )

    async def stream(
        self,
        messages: list[LLMMessage],
        *,
        model: str = "local/cortex-llm",
    ) -> AsyncIterator[str]:
        result = await self.complete(messages, model=model)
        for word in result.text.split():
            yield word + " "

    async def embed(self, texts: list[str], *, model: str = "local/cortex-embed") -> list[list[float]]:
        _ = model
        return [[float(len(t) % 10) / 10.0] * 8 for t in texts]
