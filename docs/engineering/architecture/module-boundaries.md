# Modular Monolith — Module Boundaries

This repository is a **modular monolith**: `cortex-server` + `sync-worker` + `ingestion-worker`, eight domain modules above shared libs.

> Architectural decisions: [decisions/README.md](../decisions/README.md)  
> Law corpus: [0009-law-corpus-sync.md](../decisions/0009-law-corpus-sync.md), [plans/law-corpus-sync.md](../plans/law-corpus-sync.md)

## Diagram

```mermaid
flowchart TB
  subgraph apps [Deploy shell]
    Server[cortex-server]
    SyncWorker[sync-worker]
    IngestWorker[ingestion-worker]
  end

  subgraph modules [Domain modules]
    Platform[module-platform]
    Documents[module-documents]
    Chat[module-chat]
    SyncMod[module-sync]
    DmsSync[module-dms-sync]
    Ingestion[module-ingestion]
    LawSync[module-law-sync]
    AI[module-ai]
  end

  subgraph libs [Shared libs]
    Core[cortex-core]
    Models[cortex-models]
    Connectors[cortex-connectors]
  end

  Server --> Platform
  Server --> Documents
  Server --> Chat
  Server --> SyncMod
  Server --> LawSync
  Server --> AI
  SyncWorker --> DmsSync
  SyncWorker --> LawSync
  IngestWorker --> Ingestion

  SyncMod --> DmsSync
  DmsSync --> Documents
  Ingestion --> Documents
  Chat --> AI
  LawSync -.-> AI

  modules --> Core
  modules --> Models
  DmsSync --> Connectors
  Ingestion --> Connectors
  LawSync --> Connectors
```

Dashed line `LawSync -.-> AI`: AI reads Neo4j / Weaviate law index written by law-sync — **no Python import** across modules.

## Repo structure

```
.
├── libs/
│   ├── cortex-core/
│   ├── cortex-models/
│   ├── cortex-connectors/
│   └── cortex-observability/
├── packages/
│   ├── module-platform/      # auth, cases, audit, system
│   ├── module-documents/     # Document CRUD + lifecycle
│   ├── module-chat/          # chat threads, Redis
│   ├── module-sync/          # SyncOrchestrator, job API
│   ├── module-dms-sync/      # DMS delta sync (formerly alfresco)
│   ├── module-ingestion/     # OCR, chunk, embed, Weaviate (case docs)
│   ├── module-law-sync/      # Swiss law corpus sync (planned — ADR 0009)
│   └── module-ai/            # LangGraph agents, law lookup read path
├── apps/
│   ├── cortex-server/
│   ├── sync-worker/
│   └── ingestion-worker/
```

## Public API (`api.py`)

| Module | Facade | DTO |
|--------|--------|-----|
| `module-platform` | `PlatformModule` | `module_platform/schemas/` |
| `module-documents` | `DocumentsModule` | `module_documents/schemas/` |
| `module-chat` | `ChatModule` | `module_chat/schemas/` |
| `module-sync` | `SyncModule` | `module_sync/schemas/` |
| `module-ai` | `AiModule` | `module_ai/schemas/` |
| `module-law-sync` | `LawSyncModule` | `module_law_sync/schemas/` |
| `module-dms-sync` | `tasks.py` | Celery: `sync_case_from_dms`, `finalize_sync_job` |
| `module-ingestion` | `tasks.py` | Celery: `ingest_document` |

## Dependency rules

| Module | May depend on |
|--------|---------------|
| `module-platform` | `cortex-core`, `cortex-models`, `module-ai.api` |
| `module-documents` | `cortex-core`, `cortex-models` |
| `module-chat` | `cortex-core`, `module-ai.api` |
| `module-sync` | `cortex-core`, `cortex-models` |
| `module-dms-sync` | `cortex-core`, `cortex-models`, `cortex-connectors`, `module-documents.api` |
| `module-ingestion` | `cortex-core`, `cortex-models`, `cortex-connectors`, `module-documents.api` |
| `module-law-sync` | `cortex-core`, `cortex-models`, `cortex-connectors` |
| `module-ai` | `cortex-core` (`SearchPort` read, `LawSearchPort` read) |
| `cortex-server` | all modules via `api.py` + routes |
| `sync-worker` | `module-dms-sync`, `module-law-sync`, `cortex-core` |
| `ingestion-worker` | `module-ingestion`, `cortex-core` |

**Forbidden:**

- any module → another module's internal code (only `.api`)
- worker modules → direct ORM write on `Document.status` (only `DocumentsModule`)
- `module-dms-sync` → `module-ingestion` (chain via Celery task names)
- `module-ai` → `module-law-sync` (read law data via Neo4j / `LawSearchPort` only)
- `module-law-sync` → `module-ai`, `module-documents`, `module-ingestion`
- law sync → `DocumentChunk` or `Document.status`

Enforcement: `make lint-imports`

## Celery task names

| Constant | Task name |
|----------|-----------|
| `TASK_SYNC_CASE` | `module_dms_sync.tasks.sync_case_from_dms` |
| `TASK_INGEST_DOCUMENT` | `module_ingestion.tasks.ingest_document` |
| `TASK_FINALIZE_SYNC` | `module_dms_sync.tasks.finalize_sync_job` |
| `TASK_SYNC_LAW_CORPUS` | `module_law_sync.tasks.sync_law_corpus` (planned) |
| `TASK_SYNC_LAW_PROVISION` | `module_law_sync.tasks.sync_law_provision` (planned) |
| `TASK_REINDEX_LAW_VERSION` | `module_law_sync.tasks.reindex_law_version` (planned) |

Law-sync tasks use queue **`sync`** (same worker as DMS sync until load requires a split).

## Document lifecycle

Only `module-documents` changes `Document.status`. Worker modules call `DocumentsModule.mark_syncing()`, `mark_ingesting()`, `mark_ready()`, `mark_failed()`.

Law corpus versioning is owned by **`module-law-sync`** via `LawVersion` rows in PostgreSQL — not `Document.status`.

## Law corpus lifecycle (ADR 0009)

1. **`module-law-sync`** fetches via `LawSourcePort`, normalizes, creates immutable `LawVersion`
2. Writes Markdown to Blob, graph to Neo4j, chunks to Weaviate `LawChunk`
3. **`module-ai`** reads graph + law search port for `LawLinkAgent`, `/laws/{ref}`, law RAG

## Hexagonal layout (P3)

Modules with `ports/` + `adapters/` + `register.py`:

| Module | Hexagonal status |
|--------|------------------|
| `module-documents` | full pilot (`DocumentRepositoryPort`, `DocumentService`) |
| `module-platform` | `IdentityProviderPort`, `AuthService` |
| `module-chat` | `ChatStorePort` → `RedisChatStore` |
| `module-dms-sync` | `register.py`; shared ports in `cortex-connectors` |
| `module-ingestion` | `register.py`; OCR/Search via `cortex-core` ports |
| `module-law-sync` | planned — `LawSourcePort`, Blob/Neo4j/Weaviate adapters |
| `module-sync` | `SyncOrchestrator` in `services/` |
| `module-ai` | agents + `SearchPort` / `LawSearchPort` read |

See [hexagonal-layout.md](../how-we-work/hexagonal-layout.md).

## Extract to microservice

Same pattern as before: copy module to new repo, replace in-proc facade with HTTP client, add K8s deployment.
