# Comparison: `arhitektura-monolit` vs `arhitektura-monolit-projekat-2`

Reference project **2** is an external read-only source of ideas (not part of this repo). All changes happen in **this repository**.

## Summary

| Area | `arhitektura-monolit` (target) | `arhitektura-monolit-projekat-2` |
|------|--------------------------------|----------------------------------|
| Domain modules | 7: platform, documents, chat, sync, dms-sync, ingestion, ai | 4: platform, ai, alfresco, ingestion |
| Workers | `sync-worker` + `ingestion-worker` (2 queue profiles) | single `cortex-worker` |
| ORM | `libs/cortex-models` (single source) | models in `module-platform` |
| DMS module | `module-dms-sync` (DMS-agnostic name) | `module-alfresco` |
| Document lifecycle | only `module-documents` | scattered across platform/alfresco/ingestion |
| Shared libs | core, models, connectors, observability | mostly `cortex-core` |
| Dev orchestration | `Makefile` | Poe (`scripts/app.toml`) + `scripts/dev.sh` |
| Code quality | `import-linter` | + ruff, mypy strict, pre-commit, pytest |
| DB migrations | Alembic baseline in monolith | Alembic baseline |
| DI pattern | `app.state` + facade instances in `main.py` | `ServiceRegistry` + `register.py` per module |
| HTTP middleware | CORS | + correlation ID, central error JSON |
| Team documentation | `docs/engineering/` + ADR | `docs/inzenjerstvo/*` (13 files) |
| Frontend | `apps/web-client` (React, full MVP) | `apps/web-client` (same) |
| Auth (documented) | mock JWT in code | mock + AD path in docs |

## What the monolith already does better (keep)

1. **Clear module boundaries** — documents/chat/sync extracted from platform.
2. **Split worker deploy** — sync (I/O) vs ingestion (CPU/GPU) scale independently.
3. **`cortex-connectors`** — external systems separated from domain.
4. **Import-linter** — already covers 7 modules + 2 worker shells.
5. **Celery task constants** — `cortex_core.messaging.tasks` (no hardcoded strings).

## What to take from project 2 (priority)

### P0 — immediate (documentation + onboarding)

- [x] `docs/engineering/` structure (product + engineering split)
- [x] `AGENTS.md` + Cursor rules in workspace
- [x] `scripts/` for local dev
- [x] `hexagonal-layout.md` + Cursor rule `hexagonal-modules.mdc`
- [x] AD/SSO technical contract in `docs/engineering/how-we-work/auth.md` (implementation in P3)
- [x] Orphan platform routes removed; `cortex_models` import in ingestion/core
- [x] `first-pr-checklist.md`

### P1 — developer experience

- [x] `scripts/dev.sh` + Makefile aliases (`flc`, `flct`, `test`, `db-setup`)
- [x] Poe tasks (`scripts/app.toml`)
- [x] pre-commit + ruff + mypy in root `pyproject.toml`
- [x] `.github/workflows/ci.yaml` (sync-worker + ingestion-worker build)
- [x] pytest baseline (`test_health`, `test_errors`)

### P2 — runtime quality

| From project 2 | Action in monolith |
|----------------|-------------------|
| `CortexError` hierarchy + middleware | add to `cortex-core` + `cortex-server` |
| `correlation.py` middleware | observability + request tracing |
| `ServiceRegistry` + `register.py` | gradual migration from `app.state` |
| Alembic | baseline migration from `infra/postgres/init.sql` |

### P2 — runtime quality (done)

- [x] `CortexError` hierarchy + `ErrorResponse` + middleware
- [x] `ServiceRegistry` + `register.py` per HTTP module
- [x] Alembic baseline (`alembic/versions/001_baseline_schema.py`)

### P3 — hexagonal layout + AD SSO

- [x] `module-documents` hexagonal pilot
- [x] `module-platform` AD SSO stub (`/auth/sso/url`, `/auth/sso/callback`)
- [x] `module-chat` `ChatStorePort`
- [x] `register.py` for dms-sync / ingestion

Project 2 documents (reference):

```
module_*/
  domain/
  ports/
  services/
  adapters/
  register.py
```

The monolith today uses `services/`, `repositories/`, `routes/` — **no big-bang** migration; new code in new features follows hexagonal layout where it makes sense.

## Module mapping (project 2 → monolith)

| Project 2 | Monolith |
|-----------|----------|
| `module-platform` (auth, cases, documents, chat, sync) | `module-platform` + `module-documents` + `module-chat` + `module-sync` |
| `module-alfresco` | `module-dms-sync` |
| `module-ingestion` | `module-ingestion` (same, but lifecycle via documents) |
| `module-ai` | `module-ai` (+ `agents/rag`, `legal`, `nlp`) |
| `cortex-worker` | `sync-worker` + `ingestion-worker` |

## What we deliberately do NOT take from project 2

- Reverting to one `cortex-worker` and `module-alfresco` name.
- ORM duplicates in worker modules.
- Direct cross-module service imports (facade only).
- Microservice extract as default — monolith remains primary architecture.

## Post-P3 hardening (architecture ready for team)

- [x] `create_documents_module()` + `worker_deps.py` for Celery
- [x] Cleanup: dead ORM in platform, legacy schema re-export, ingestion models shim
- [x] CI green (`make flct`)
- [x] [architecture-ready.md](../architecture/architecture-ready.md) + [first-feature.md](../how-we-work/first-feature.md)
- [x] `cortex_connectors/factory.py` (stub selection)
- [ ] Product E2E (sync → ready, RAG, AD) — team feature PRs

## Next steps (order for the team)

1. Read [engineering/README.md](../README.md) and [architecture-ready.md](../architecture/architecture-ready.md).
2. Run `make install && make dev` (or `scripts/dev.sh`).
3. Before every PR: `make flct`.
4. Implement features per [feature-placement.md](../how-we-work/feature-placement.md) and [first-feature.md](../how-we-work/first-feature.md).
