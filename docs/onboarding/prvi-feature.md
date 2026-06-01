# Prvi feature — walkthrough

Tri tipična scenarija za prvi PR. Kopiraj obrazac iz postojećeg koda u istom modulu.

## Walkthrough A — novi HTTP endpoint (module-documents)

**Primer:** dodati polje `notes` na dokument ili novi GET filter.

### Koraci

1. **ORM** (ako treba kolona): `libs/cortex-models/cortex_models/document.py` + Alembic migracija.
2. **Port** (ako menja persistence): `module_documents/ports/document_repository_port.py`.
3. **Adapter:** `module_documents/adapters/postgres_document_repository.py`.
4. **Service:** `module_documents/services/document_service.py`.
5. **Facade:** `module_documents/api.py` — nova metoda.
6. **DTO:** `module_documents/schemas/documents.py`.
7. **Route:** `module_documents/routes/documents.py` — tanak handler.
8. **Deps:** `get_documents_module` iz `app.state` (već postoji).
9. **Server:** router već montiran u `cortex-server/main.py` — obično bez izmene.

### Šablon route handlera

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

### Provera

```bash
make lint-imports
make flct
```

---

## Walkthrough B — novi Celery korak

**Primer:** dodatni korak posle OCR-a u ingestion pipeline-u.

### Pravila

- CPU/GPU → `module-ingestion`; I/O (DMS download) → `module-dms-sync`.
- Lanac: `celery_app.send_task(TASK_..., queue=QUEUE_...)`.
- **Ne** importuj `module_ingestion` iz `module_dms_sync`.

### Koraci

1. Konstanta u `libs/cortex-core/cortex_core/messaging/tasks.py` (ako novo ime taska).
2. Task funkcija u `module_ingestion/tasks.py` ili `module_dms_sync/tasks.py`.
3. Lifecycle: `_documents.mark_ingesting()` / `mark_ready()` / `mark_failed()` — deps iz `worker_deps.py`.
4. Enqueue sledećeg koraka preko `TASK_*` konstante.

### Worker deps (obavezno)

```python
from module_ingestion.worker_deps import register_worker_dependencies

_worker_deps = register_worker_dependencies()
_documents = _worker_deps.documents
```

### Provera

```bash
make lint-imports
# ručno: make dev + trigger sync sa UI
```

---

## Walkthrough C — novi shared port (spoljni sistem)

**Primer:** novi `NotificationPort` za email.

### Koraci

1. **Port:** `libs/cortex-core/cortex_core/ports/notification.py` — `Protocol` ili `ABC`.
2. **Stub:** `libs/cortex-connectors/cortex_connectors/notification/stub.py`.
3. **Factory:** `cortex_connectors/factory.py` — `get_notification_client()`.
4. **Service** u modulu koji koristi port — prima port kroz `__init__`.
5. **Wire:** `register.py` ili `worker_deps.py` poziva factory.

### Factory obrazac

```python
from cortex_connectors.factory import get_notification_client

client = get_notification_client()  # stub dok CORTEX_CONNECTORS_MODE=stub
```

### Unit test bez Docker-a

Vidi `packages/module-documents/tests/test_document_service_fake_repo.py` — in-memory implementacija porta.

---

## Red flags (STOP)

| Problem | Ispravno |
|---------|----------|
| `doc.status = "ready"` u workeru | `documents.mark_ready(id, session)` |
| `from module_ai.agents...` iz platform | `from module_ai.api import AiModule` |
| `DocumentsModule()` bez factory | `create_documents_module()` |
| Business logika u `main.py` | modul `services/` + `api.py` |
| Novi ORM u `module_platform/models/` | `cortex_models` |

## Dalje

- [ARCHITECTURE-READY.md](../ARCHITECTURE-READY.md)
- [hexagonal-layout.md](hexagonal-layout.md)
- [checklist-prvi-pr.md](checklist-prvi-pr.md)
