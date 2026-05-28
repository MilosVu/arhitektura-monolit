from cortex_core.infrastructure.llm.stub_router import StubLLMRouter
from cortex_core.ports.llm import LLMCompletionResult, LLMMessage, LLMPort


class LiteLLMRouter(StubLLMRouter):
    """
    Produkcija:
      import litellm
      litellm.completion(model="openai/local-llm", api_base="http://maas:8080/v1", ...)

    MVP: nasleđuje StubLLMRouter iz cortex-core.
    """

    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        model: str = "local/cortex-llm",
        temperature: float = 0.2,
    ) -> LLMCompletionResult:
        return await super().complete(messages, model=model, temperature=temperature)
