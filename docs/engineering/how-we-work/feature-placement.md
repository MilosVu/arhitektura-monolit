# Feature Placement — Implementation Guide

Before writing code, answer: **which domain owns this feature**. If unsure, use the table below.

## Decision table

| Question / feature | Package | Typical files |
|--------------------|---------|---------------|
| Login, JWT/session, user, role mapping | `module-platform` | `services/auth_service.py`, `routes/auth.py` |
| Case list, detail, access control | `module-platform` | `services/case_service.py`, `routes/cases.py` |
| Audit log | `module-platform` | `routes/audit.py`, `cortex_models.AuditLog` |
| System/health status aggregate | `module-platform` | `system.py`, `routes/system.py` |
| Document CRUD, view, re-ingest API | `module-documents` | `api.py`, `routes/documents.py` |
| **Changing `Document.status`** | `module-documents` | `api.py` → `mark_syncing`, `mark_ready`, ... |
| Chat thread, messages, Redis | `module-chat` | `adapters/redis_chat_store.py`, `routes/chat.py` |
| Sync job creation, polling, orchestrator | `module-sync` | `services/sync_orchestrator.py`, `routes/sync.py` |
| DMS download, delta sync, blob | `module-dms-sync` | `tasks.py`, `services/`, `cortex-connectors` |
| OCR, chunk, embed, Weaviate write | `module-ingestion` | `tasks.py`, `services/pipeline.py` |
| RAG search, law lookup, translate, agents | `module-ai` | `agents/`, `routes/rag.py`, ... |
| New ORM entity / column | `cortex-models` | `cortex_models/*.py` — **never** new ORM in `module_*` |
| HTTP DTO (request/response) | owning module | `module_*/schemas/` — not in `module-platform` for documents/chat/sync |
| New port (interface) | `cortex-core` | `cortex_core/ports/` |
| Alfresco/Blob/OCR adapter | `cortex-connectors` | `cortex_connectors/*` |
| Metrics, trace span helpers | `cortex-observability` | no business logic |
| New HTTP endpoint | module `routes/` + `api.py` + `schemas/` | see checklist below |
| Router mounting, CORS, lifespan | `apps/cortex-server` | `main.py` wiring only |
| Celery task registration | worker module `tasks.py` | shell bootstrap only |

## HTTP routes by module

| Prefix / area | Module |
|---------------|--------|
| `/auth`, `/cases`, `/audit`, `/system` | `module-platform` |
| `/cases/{id}/documents`, `/documents/{id}` | `module-documents` |
| `/chat/*` | `module-chat` |
| `/cases/{id}/sync`, `/sync/{job_id}` | `module-sync` |
| RAG, laws, translate | `module-ai` |

Do **not** move documents/chat/sync back into the `module-platform` router.

## New HTTP endpoint — checklist

1. Pick the module (table above).
2. Request/response DTO in `module_*/schemas/`.
3. Use-case method in `module_*/api.py` (facade).
4. Thin handler in `module_*/routes/*.py`.
5. `deps.py`: `get_*_module` reads `request.app.state`.
6. In `cortex-server/main.py`: module instance in `app.state` + `include_router`.

## New Celery step — checklist

1. Sync (I/O) → `module-dms-sync`; CPU/GPU pipeline → `module-ingestion`.
2. Task function in `tasks.py`; name from `cortex_core.messaging.tasks`.
3. Document status: `DocumentsModule.mark_*()` — no direct ORM write.
4. Enqueue next step: `celery_app.send_task(TASK_..., queue=...)`.
5. `make lint-imports`.

## Red flags (STOP)

- `doc.status = ...` in a worker outside `module-documents`
- `from module_ai.agents...` from platform/chat
- `from module_ingestion.services...` from dms-sync (use Celery task)
- Business logic in `cortex-server/main.py`
- Duplicated ORM model in a worker package

## Example: add re-ingest document endpoint

```
module-documents/
  schemas/documents.py     # ReingestRequest if needed
  api.py                   # DocumentsModule.trigger_reingest(...)
  routes/documents.py      # POST handler
  deps.py                  # get_documents_module
```

`module-sync` or `module-ingestion` only enqueue — no HTTP in worker modules.
