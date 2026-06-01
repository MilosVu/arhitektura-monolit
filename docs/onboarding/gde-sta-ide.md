# Gde šta ide — vodič za implementaciju

Pre pisanja koda odgovori na pitanje **koji domen poseduje feature**. Ako nisi siguran, pogledaj tabelu ispod.

## Decision table

| Pitanje / feature | Paket | Tipični fajlovi |
|-------------------|-------|-----------------|
| Login, JWT/session, korisnik, role mapiranje | `module-platform` | `services/auth_service.py`, `routes/auth.py` |
| Lista predmeta, detalj, pristup | `module-platform` | `services/case_service.py`, `routes/cases.py` |
| Audit log | `module-platform` | `routes/audit.py`, `cortex_models.AuditLog` |
| System/health status agregat | `module-platform` | `system.py`, `routes/system.py` |
| Document CRUD, pregled, re-ingest API | `module-documents` | `api.py`, `routes/documents.py` |
| **Promena `Document.status`** | `module-documents` | `api.py` → `mark_syncing`, `mark_ready`, ... |
| Chat thread, poruke, Redis | `module-chat` | `infrastructure/`, `routes/chat.py` |
| Sync job kreiranje, polling, orchestrator | `module-sync` | `services/sync_orchestrator.py`, `routes/sync.py` |
| Preuzimanje iz DMS, delta sync, blob | `module-dms-sync` | `tasks.py`, `services/`, `cortex-connectors` |
| OCR, chunk, embed, Weaviate write | `module-ingestion` | `tasks.py`, `services/pipeline.py` |
| RAG search, law lookup, prevod, agenti | `module-ai` | `agents/`, `routes/rag.py`, ... |
| Novi ORM entitet / kolona | `cortex-models` | `cortex_models/*.py` — **nikad** novi ORM u `module_*` |
| HTTP DTO (request/response) | modul koji poseduje domen | `module_*/schemas/` — ne u `module-platform` za documents/chat/sync |
| Novi port (interface) | `cortex-core` | `cortex_core/ports/` |
| Konkretan Alfresco/Blob/OCR adapter | `cortex-connectors` | `cortex_connectors/*` |
| Metrike, trace span helper | `cortex-observability` | bez business logike |
| Novi HTTP endpoint | modul `routes/` + `api.py` + `schemas/` | vidi checklist ispod |
| Montiranje routera, CORS, lifespan | `apps/cortex-server` | `main.py` samo wiring |
| Registracija Celery taskova | worker modul `tasks.py` | shell samo bootstrap |

## HTTP rute po modulu

| Prefix / oblast | Modul |
|-----------------|-------|
| `/auth`, `/cases`, `/audit`, `/system` | `module-platform` |
| `/cases/{id}/documents`, `/documents/{id}` | `module-documents` |
| `/chat/*` | `module-chat` |
| `/cases/{id}/sync`, `/sync/{job_id}` | `module-sync` |
| RAG, laws, translate | `module-ai` |

**Ne** vraćaj documents/chat/sync u `module-platform` router.

## Novi HTTP endpoint — checklist

1. Odredi modul (tabela gore).
2. Request/response DTO u `module_*/schemas/`.
3. Use-case metoda u `module_*/api.py` (facade).
4. Tanak handler u `module_*/routes/*.py`.
5. `deps.py`: `get_*_module` čita `request.app.state`.
6. U `cortex-server/main.py`: instanca modula u `app.state` + `include_router`.

## Novi Celery korak — checklist

1. Sync (I/O) → `module-dms-sync`; CPU/GPU pipeline → `module-ingestion`.
2. Task funkcija u `tasks.py`, ime iz `cortex_core.messaging.tasks`.
3. Status dokumenta: `DocumentsModule.mark_*()` — ne direktan ORM write.
4. Enqueue sledećeg koraka: `celery_app.send_task(TASK_..., queue=...)`.
5. `make lint-imports`.

## Red flags (STOP)

- `doc.status = ...` u workeru van `module-documents`
- `from module_ai.agents...` iz platform/chat
- `from module_ingestion.services...` iz dms-sync (koristi Celery task)
- Business logika u `cortex-server/main.py`
- Dupliran ORM model u worker paketu

## Primer: “dodaj endpoint za re-ingest dokumenta”

```
module-documents/
  schemas/documents.py     # ReingestRequest ako treba
  api.py                   # DocumentsModule.trigger_reingest(...)
  routes/documents.py      # POST handler
  deps.py                  # get_documents_module
```

`module-sync` ili `module-ingestion` samo enqueue — ne HTTP u worker modulu.
