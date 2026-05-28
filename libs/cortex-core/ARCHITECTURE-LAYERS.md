# Cortex Core — slojevi arhitekture

Deljeni paket (`libs/cortex-core`) je **jedini** dozvoljen cross-import između servisa.

## Struktura

```
cortex_core/
├── base/                    # BaseRepository, BaseService
├── domain/                  # Domen greške
├── ports/                   # Protokoli (Alfresco, LLM, OCR, Cache)
├── infrastructure/
│   ├── redis/               # Redis adapteri po use-case-u
│   └── llm/                 # StubLLMRouter (MaaS stub)
├── agents/                  # AgentState, ToolDefinition (LangGraph tipovi)
├── messaging/               # Celery queue/task konvencije
├── db.py                    # Base, engine, session factory
├── models.py                # deprecated re-exports → module_platform.models
├── infrastructure/
│   ├── redis/               # RedisCacheAdapter, ChatRepository (legacy)
│   └── weaviate/            # client + collection bootstrap (connection only)
```

## Redis — tri odvojena use-case-a

| Modul | Ključ / kanal | Ko piše | Ko čita |
|-------|---------------|---------|---------|
| `AdSessionCache` | `cortex:ad:session:{user_id}` | api-gateway | api-gateway |
| `ChatRepository` | `cortex:thread:{id}:messages` | api-gateway | api-gateway, ai-agents |
| `LangGraphCheckpointStore` | `cortex:agent:checkpoint:{thread_id}` | ai-agents | ai-agents |
| `SyncProgressPublisher` | `cortex:sync:progress:{job_id}` | workeri | gateway (WS, future) |

## Ports & Adapters (hexagonal)

```
                    ┌─────────────────┐
   sync-worker ────►│  AlfrescoPort   │◄──── StubAlfrescoClient
                    └─────────────────┘
                    ┌─────────────────┐
 ingestion-worker ─►│    OCRPort      │◄──── StubOCRAdapter
                    └─────────────────┘
                    ┌─────────────────┐
   ai-agents ──────►│    LLMPort      │◄──── LiteLLMRouter / StubLLMRouter
                    └─────────────────┘
                    ┌─────────────────┐
   svi servisi ────►│   CachePort     │◄──── RedisCacheAdapter
                    └─────────────────┘
```

## Gde živi poslovna logika

| Sloj | Lokacija | Primer |
|------|----------|--------|
| HTTP router | `*/main.py` | FastAPI endpoint |
| Application service | `*/services/` | `CaseService`, `AlfrescoSyncService` |
| Repository | `*/repositories/` | `CaseRepository` |
| Domain port | `cortex_core/ports/` | `AlfrescoPort` |
| Infrastructure | `*/adapters/`, `cortex_core/infrastructure/` | `StubAlfrescoClient` |
| Agent (LangGraph) | `ai-agents/agents/` | `ChatAgent`, `LawLinkAgent` |

## Mikroservisi vs monolit

| Mikroservisi | Monolit (modularni) |
|--------------|---------------------|
| `api-gateway/services/` | `module-platform/services/` |
| `ai-agents/agents/` | `module-ai/agents/` |
| `sync-worker/services/` | `module-alfresco/services/` |
| `ingestion-worker/services/` | `module-ingestion/services/` |
| HTTP između servisa | `PlatformModule` → `AiModule` (in-process facade) |

`cortex-core` ostaje **identičan** u oba projekta.

## Modularni monolit

Monolit repozitorijum koristi **4 domenska paketa** u `packages/` iznad `cortex-core` u `libs/`:

| Paket | Uloga | DTO |
|-------|--------|-----|
| `module-platform` | Auth, cases, audit, sync trigger | `module_platform/schemas.py` |
| `module-ai` | Agenti, RAG, chat, laws/Neo4j | `module_ai/schemas.py` |
| `module-alfresco` | Alfresco delta sync + Celery sync tasks |
| `module-ingestion` | OCR, chunk, embed, Weaviate + Celery ingestion tasks |

Deploy shell-ovi (`apps/cortex-server`, `apps/cortex-worker`) su **tanki** — samo FastAPI/Celery wiring, bez poslovne logike.

Detalji granica: [MODULE-BOUNDARIES.md](../../MODULE-BOUNDARIES.md) u root-u monolit repoa.
