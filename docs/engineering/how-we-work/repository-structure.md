# Repository Structure and Layering

## Apps (composition roots)

| App | Role | Allowed contents |
|-----|------|------------------|
| `cortex-server` | FastAPI | `main.py`, middleware, `include_router`, `app.state` |
| `sync-worker` | Celery `-Q sync` | only `tasks/__init__.py` → celery app |
| `ingestion-worker` | Celery `-Q ingestion` | same |
| `web-client` | React UI | `src/pages`, `src/api`, `src/components` |

**Apps must not** contain business logic, SQL, Alfresco calls, or agents.

## Typical domain module (hexagonal)

See [hexagonal-layout.md](hexagonal-layout.md).

```
packages/module-{name}/
├── pyproject.toml
└── module_{name}/
    ├── api.py           # application facade (public module contract)
    ├── register.py      # DI — register_services(registry)
    ├── deps.py          # FastAPI Depends → app.state / registry
    ├── routes/          # driving adapter (thin HTTP)
    ├── schemas/         # Pydantic DTO
    ├── domain/          # entities, domain rules (optional)
    ├── ports/           # Protocol interfaces
    ├── services/        # use-case logic (depends on ports)
    ├── adapters/        # port implementations (Postgres, Redis, ...)
    └── tasks.py         # Celery driving adapter (worker modules)
```

### Layering

```
routes/ | tasks.py  →  api.py  →  services/  →  ports/  ←  adapters/  →  cortex-connectors
```

- **routes/** — HTTP, Depends, `response_model`, no SQL
- **api.py** — use-case boundaries, module-level auth, DTO mapping
- **services/** — must not import FastAPI
- **adapters/** — Postgres, Redis, thin wrapper over `cortex-connectors`

## Shared libs

| Lib | Contents |
|-----|----------|
| `cortex-models` | SQLAlchemy: User, Case, Document, SyncJob, AuditLog |
| `cortex-core` | ports, enums, settings, Celery factory, messaging task names, SearchPort |
| `cortex-connectors` | Alfresco, Blob, OCR implementations |
| `cortex-observability` | metrics/tracing hooks |

## Frontend (`apps/web-client`)

```
apps/web-client/
├── src/
│   ├── api/           # HTTP client, types
│   ├── pages/         # screens (Cases, Chat, Documents, ...)
│   ├── components/    # layout, sidebar
│   └── context/       # AuthContext (token, user)
├── package.json
└── vite.config.ts
```

New screen → `src/pages/`, route in `App.tsx`, API call in `src/api/client.ts`.

## Scripts (`scripts/`)

Operational scripts **outside** runtime:

- `dev.sh` — run local stack
- `seed-neo4j.sh` — seed law graph
- future: migrations, backup, CI helpers

## Infra

- `infra/docker-compose.yml` — local Postgres, Redis, RabbitMQ, Weaviate, Neo4j
- `infra/k8s/` — manifests per service
- `infra/postgres/init.sql` — initial schema (Alembic baseline from project 2)

## Naming

- Package: `module-documents` → import `module_documents`
- Facade: `{Domain}Module`
- Service: `{Domain}Service`, `{Action}Orchestrator`
- Celery: `sync_case_from_dms`, `ingest_document`
