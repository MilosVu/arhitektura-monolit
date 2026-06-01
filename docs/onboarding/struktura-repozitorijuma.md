# Struktura repozitorijuma i layering

## Apps (composition roots)

| App | Uloga | Šta sme unutra |
|-----|-------|----------------|
| `cortex-server` | FastAPI | `main.py`, middleware, `include_router`, `app.state` |
| `sync-worker` | Celery `-Q sync` | samo `tasks/__init__.py` → celery app |
| `ingestion-worker` | Celery `-Q ingestion` | isto |
| `web-client` | React UI | `src/pages`, `src/api`, `src/components` |

**Apps ne sadrže** poslovnu logiku, SQL, Alfresco pozive, agente.

## Tipičan domen modul (hexagonal)

Vidi [hexagonal-layout.md](hexagonal-layout.md).

```
packages/module-{name}/
├── pyproject.toml
└── module_{name}/
    ├── api.py           # application facade (javni ugovor modula)
    ├── register.py      # DI — register_services(registry)
    ├── deps.py          # FastAPI Depends → app.state / registry
    ├── routes/          # driving adapter (tanak HTTP)
    ├── schemas/         # Pydantic DTO
    ├── domain/          # entiteti, domenska pravila (opciono)
    ├── ports/           # Protocol interfejsi
    ├── services/        # use-case logika (zavisi od portova)
    ├── adapters/        # implementacije portova (Postgres, Redis, ...)
    ├── repositories/    # legacy — migrira se u adapters/
    ├── infrastructure/  # legacy — migrira se u adapters/
    └── tasks.py         # Celery driving adapter
```

### Layering

```
routes/ | tasks.py  →  api.py  →  services/  →  ports/  ←  adapters/  →  cortex-connectors
```

- **routes/** — HTTP, Depends, `response_model`, bez SQL
- **api.py** — use-case granice, auth na nivou modula, mapiranje u DTO
- **services/** — ne importuju FastAPI
- **repositories/** — koriste `cortex_models`

## Shared libs

| Lib | Sadržaj |
|-----|---------|
| `cortex-models` | SQLAlchemy: User, Case, Document, SyncJob, AuditLog |
| `cortex-core` | ports, enums, settings, Celery factory, messaging task names, SearchPort |
| `cortex-connectors` | Alfresco, Blob, OCR implementacije |
| `cortex-observability` | metrics/tracing hooks |

## Frontend (`apps/web-client`)

```
apps/web-client/
├── src/
│   ├── api/           # HTTP klijent, tipovi
│   ├── pages/         # ekrani (Cases, Chat, Documents, ...)
│   ├── components/    # layout, sidebar
│   └── context/       # AuthContext (token, user)
├── package.json
└── vite.config.ts
```

Novi ekran → `src/pages/`, ruta u `App.tsx`, API poziv u `src/api/client.ts`.

## Skripte (`scripts/`)

Operativne skripte koje **nisu** deo runtime aplikacije:

- `dev.sh` — lokalno pokretanje stack-a
- `seed-neo4j.sh` — seed pravnog grafa
- buduće: migracije, backup, CI helperi

## Infra

- `infra/docker-compose.yml` — lokalni Postgres, Redis, RabbitMQ, Weaviate, Neo4j
- `infra/k8s/` — manifesti po servisu
- `infra/postgres/init.sql` — početna šema (Alembic planiran iz projekta 2)

## Imenovanje

- Paket: `module-documents` → import `module_documents`
- Facade: `{Domain}Module`
- Servis: `{Domain}Service`, `{Action}Orchestrator`
- Celery: `sync_case_from_dms`, `ingest_document`
