"""Port ka lokalnom LLM-u (LiteLLM / MaaS) — implementacija u ai-agents."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass


@dataclass
class LLMMessage:
    role: str  # system | user | assistant
    content: str


@dataclass
class LLMCompletionResult:
    text: str
    model: str
    prompt_tokens: int
    completion_tokens: int


class LLMPort(ABC):
    """Univerzalni LLM ruter — nikad direktan poziv ka cloud API-ju."""

    @abstractmethod
    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        model: str = "local/cortex-llm",
        temperature: float = 0.2,
    ) -> LLMCompletionResult:
        """Sinhroni completion (prevod, kratak odgovor)."""

    @abstractmethod
    async def stream(
        self,
        messages: list[LLMMessage],
        *,
        model: str = "local/cortex-llm",
    ) -> AsyncGenerator[str, None]:
        """Streaming tokeni za chat UI (SSE)."""

    @abstractmethod
    async def embed(
        self, texts: list[str], *, model: str = "local/cortex-embed"
    ) -> list[list[float]]:
        """Embedding vektori za ingestion-worker."""
