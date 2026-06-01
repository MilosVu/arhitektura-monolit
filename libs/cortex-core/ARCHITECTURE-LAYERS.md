# Cortex Core — slojevi arhitekture

Deljeni paket (`libs/cortex-core`) je **jedini** dozvoljen cross-import između modula.

## Struktura

```
cortex_core/
├── base/                    # BaseRepository, BaseService
├── errors.py                # Domen greške (CortexError, ForbiddenError, ...)
├── ports/                   # Protokoli (Alfresco, LLM, OCR, Cache, Search)
├── infrastructure/
│   ├── redis/               # RedisCacheAdapter, AdSessionCache, SyncProgressPublisher, ...
│   ├── llm/                 # StubLLMRouter (MaaS stub)
│   └── weaviate/            # client + collection bootstrap (connection only)
├── agents/                  # AgentState, ToolDefinition (LangGraph tipovi)
├── messaging/               # Celery queue/task konvencije
├── db.py                    # Base, engine, session factory
├── sync_worker_celery.py    # Celery app za sync queue
└── ingestion_worker_celery.py  # Celery app za ingestion queue
```

ORM entiteti žive u **`cortex-models`**, ne u `cortex-core`.

## Redis — use-case adapteri

| Adapter | Ključ / kanal | Ko piše | Ko čita |
|---------|---------------|---------|---------|
| `AdSessionCache` | `cortex:ad:session:{user_id}` | module-platform | module-platform |
| `RedisChatStore` (module-chat) | `cortex:thread:{id}:messages` | module-chat | module-chat, module-ai |
| `LangGraphCheckpointStore` | `cortex:agent:checkpoint:{thread_id}` | module-ai | module-ai |
| `SyncProgressPublisher` | `cortex:sync:progress:{job_id}` | module-dms-sync | module-sync (WS, future) |

Chat persistence je u **`module-chat/adapters/redis_chat_store.py`** — ne u `cortex-core`.

## Ports & Adapters (hexagonal)

```
                    ┌─────────────────┐
   sync-worker ────►│  AlfrescoPort   │◄──── cortex-connectors
                    └─────────────────┘
                    ┌─────────────────┐
 ingestion-worker ─►│    OCRPort      │◄──── cortex-connectors
                    └─────────────────┘
                    ┌─────────────────┐
   module-ai ───────►│    LLMPort      │◄──── StubLLMRouter
                    └─────────────────┘
                    ┌─────────────────┐
   svi moduli ─────►│   CachePort     │◄──── RedisCacheAdapter
                    └─────────────────┘
```

## Gde živi poslovna logika

| Sloj | Lokacija | Primer |
|------|----------|--------|
| HTTP router | `module_*/routes/` | FastAPI endpoint |
| Application facade | `module_*/api.py` | `DocumentsModule`, `PlatformModule` |
| Use-case service | `module_*/services/` | `CaseService`, `DmsSyncService` |
| Port (interface) | `cortex_core/ports/` ili `module_*/ports/` | `SearchPort`, `DocumentRepositoryPort` |
| Adapter | `module_*/adapters/`, `cortex-connectors/` | `PostgresDocumentRepository`, `RedisChatStore` |
| Agent (LangGraph) | `module-ai/agents/` | `RagAgent`, `LawLinkAgent` |

## Modularni monolit

Monolit repozitorijum koristi **7 domenskih paketa** u `packages/` iznad shared libs u `libs/`:

| Paket | Uloga |
|-------|--------|
| `module-platform` | Auth, cases, audit, system health |
| `module-documents` | Document CRUD + lifecycle (jedini menja status) |
| `module-chat` | Chat thread, poruke (Redis) |
| `module-sync` | Sync job trigger, polling, orchestrator |
| `module-dms-sync` | DMS delta sync + Celery sync tasks |
| `module-ingestion` | OCR, chunk, embed, Weaviate write |
| `module-ai` | Agenti, RAG, laws/Neo4j, prevod |

Deploy shell-ovi (`apps/cortex-server`, `apps/sync-worker`, `apps/ingestion-worker`) su **tanki** — samo FastAPI/Celery wiring, bez poslovne logike.

Detalji granica: [docs/engineering/architecture/module-boundaries.md](../../docs/engineering/architecture/module-boundaries.md).
