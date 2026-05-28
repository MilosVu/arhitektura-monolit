"""Deljeni tipovi za LangGraph agente (state, tools)."""

from typing import Annotated, Any, TypedDict


class AgentState(TypedDict, total=False):
    """
    LangGraph state — prolazi kroz čvorove grafa.

    Primer toka ChatAgent-a:
      retrieve_context → call_llm → format_citations → END
    """

    thread_id: str
    case_id: int
    user_id: int
    user_message: str
    messages: list[dict[str, str]]
    retrieved_chunks: list[dict[str, Any]]
    law_refs: list[str]
    assistant_reply: str
    tool_calls: list[dict[str, Any]]


class ToolDefinition(TypedDict):
    name: str
    description: str
    parameters: dict[str, Any]


# Registrovani alati za agente (RAG, Neo4j, prevod)
REGISTERED_TOOLS: list[ToolDefinition] = [
    {
        "name": "search_case_documents",
        "description": "BM25 pretraga chunkova u Weaviate za dati case_id",
        "parameters": {"case_id": "int", "query": "str", "limit": "int"},
    },
    {
        "name": "lookup_law_article",
        "description": "Pronađi član zakona u Neo4j grafu",
        "parameters": {"law_ref": "str"},
    },
    {
        "name": "translate_text",
        "description": "Prevod dokumenta preko LiteLLM",
        "parameters": {"text": "str", "target_lang": "str"},
    },
]

AgentContext = Annotated[dict[str, Any], "Runtime kontekst prosleđen agentu"]
