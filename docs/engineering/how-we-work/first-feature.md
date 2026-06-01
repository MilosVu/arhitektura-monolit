# First Feature — Walkthrough

Three typical scenarios for a first PR. Copy the pattern from existing code in the same module.

## Walkthrough A — new HTTP endpoint (module-documents)

**Example:** add a `notes` field on a document or a new GET filter.

### Steps

1. **ORM** (if column needed): `libs/cortex-models/cortex_models/document.py` + Alembic migration.
2. **Port** (if persistence changes): `module_documents/ports/document_repository_port.py`.
3. **Adapter:** `module_documents/adapters/postgres_document_repository.py`.
4. **Service:** `module_documents/services/document_service.py`.
5. **Facade:** `module_documents/api.py` — new method.
6. **DTO:** `module_documents/schemas/documents.py`.
7. **Route:** `module_documents/routes/documents.py` — thin handler.
8. **Deps:** `get_documents_module` from `app.state` (already exists).
9. **Server:** router already mounted in `cortex-server/main.py` — usually no change.

### Route handler template

```python
@router.get("/documents/{document_id}/notes")
def get_notes(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    module: DocumentsModule = Depends(get_documents_module),
):
    return module.get_notes(document_id, user, db)
```

### Verify

```bash
make lint-imports
make flct
```

---

## Walkthrough B — new Celery step

**Example:** extra step after OCR in the ingestion pipeline.

### Rules

- CPU/GPU → `module-ingestion`; I/O (DMS download) → `module-dms-sync`.
- Chain: `celery_app.send_task(TASK_..., queue=QUEUE_...)`.
- Do **not** import `module_ingestion` from `module_dms_sync`.

### Steps

1. Constant in `libs/cortex-core/cortex_core/messaging/tasks.py` (if new task name).
2. Task function in `module_ingestion/tasks.py` or `module_dms_sync/tasks.py`.
3. Lifecycle: `_documents.mark_ingesting()` / `mark_ready()` / `mark_failed()` — deps from `worker_deps.py`.
4. Enqueue next step via `TASK_*` constant.

### Worker deps (required)

```python
from module_ingestion.worker_deps import register_worker_dependencies

_worker_deps = register_worker_dependencies()
_documents = _worker_deps.documents
```

### Verify

```bash
make lint-imports
# manual: make dev + trigger sync from UI
```

---

## Walkthrough C — new shared port (external system)

**Example:** new `NotificationPort` for email.

### Steps

1. **Port:** `libs/cortex-core/cortex_core/ports/notification.py` — `Protocol` or `ABC`.
2. **Stub:** `libs/cortex-connectors/cortex_connectors/notification/stub.py`.
3. **Factory:** `cortex_connectors/factory.py` — `get_notification_client()`.
4. **Service** in the module that uses the port — receives port in `__init__`.
5. **Wire:** `register.py` or `worker_deps.py` calls factory.

### Factory pattern

```python
from cortex_connectors.factory import get_notification_client

client = get_notification_client()  # stub while CORTEX_CONNECTORS_MODE=stub
```

### Unit test without Docker

See `packages/module-documents/tests/test_document_service_fake_repo.py` — in-memory port implementation.

---

## Red flags (STOP)

| Problem | Correct approach |
|---------|------------------|
| `doc.status = "ready"` in worker | `documents.mark_ready(id, session)` |
| `from module_ai.agents...` from platform | `from module_ai.api import AiModule` |
| `DocumentsModule()` without factory | `create_documents_module()` |
| Business logic in `main.py` | module `services/` + `api.py` |
| New ORM in `module_platform/models/` | `cortex_models` |

## Next

- [architecture/architecture-ready.md](../architecture/architecture-ready.md)
- [first-pr-checklist.md](first-pr-checklist.md)
- [hexagonal-layout.md](hexagonal-layout.md)
