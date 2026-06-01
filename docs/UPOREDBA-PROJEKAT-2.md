# Uporedba: `arhitektura-monolit` vs `arhitektura-monolit-projekat-2`

Referentni primer **2** služi samo kao izvor ideja. **Menjamo isključivo** `arhitektura-monolit/`.

## Sažetak

| Oblast | `arhitektura-monolit` (cilj) | `arhitektura-monolit-projekat-2` |
|--------|------------------------------|----------------------------------|
| Domen moduli | 7: platform, documents, chat, sync, dms-sync, ingestion, ai | 4: platform, ai, alfresco, ingestion |
| Workeri | `sync-worker` + `ingestion-worker` (2 queue profila) | jedan `cortex-worker` |
| ORM | `libs/cortex-models` (jedan izvor) | modeli u `module-platform` |
| DMS modul | `module-dms-sync` (DMS-agnostic ime) | `module-alfresco` |
| Document lifecycle | samo `module-documents` | rasuto po platform/alfresco/ingestion |
| Shared libs | core, models, connectors, observability | uglavnom `cortex-core` |
| Dev orkestracija | `Makefile` | Poe (`scripts/app.toml`) + `scripts/dev.sh` |
| Kvalitet koda | `import-linter` | + ruff, mypy strict, pre-commit, pytest |
| Migracije DB | nema Alembic u monolitu | Alembic baseline |
| DI pattern | `app.state` + facade instance u `main.py` | `ServiceRegistry` + `register.py` po modulu |
| HTTP middleware | CORS | + correlation ID, centralni error JSON |
| Dokumentacija tima | REFACTOR-PLAN, MODULE-BOUNDARIES | `docs/inzenjerstvo/*` (13 fajlova) |
| Frontend | `apps/web-client` (React, pun MVP) | `apps/web-client` (isto) |
| Auth (dokumentovano) | mock JWT u kodu | mock + putanja ka AD u docs |

## Šta je monolit već bolje (zadržati)

1. **Jasne granice modula** — documents/chat/sync izdvojeni iz platforme.
2. **Split worker deploy** — sync (I/O) vs ingestion (CPU/GPU) nezavisno skaliranje.
3. **`cortex-connectors`** — spoljni sistemi odvojeni od domena.
4. **Import-linter** — već pokriva 7 modula + 2 worker shell-a.
5. **Celery task konstante** — `cortex_core.messaging.tasks` (bez hardcoded stringova).

## Šta preuzeti iz projekta 2 (prioritet)

### P0 — odmah (dokumentacija + onboarding)

- [x] Struktura `docs/onboarding/` (ovaj repozitorijum)
- [x] `AGENTS.md` + Cursor rules u workspace-u
- [x] `scripts/` za lokalni dev
- [x] `hexagonal-layout.md` + Cursor rule `hexagonal-modules.mdc`
- [x] AD/SSO tehnički contract u `docs/onboarding/auth.md` (implementacija u P3)
- [x] Orphan platform routes uklonjeni; `cortex_models` import u ingestion/core
- [x] `checklist-prvi-pr.md`

### P1 — developer experience

- [x] `scripts/dev.sh` + Makefile aliasi (`flc`, `flct`, `test`, `db-setup`)
- [x] Poe taskovi (`scripts/app.toml`)
- [x] pre-commit + ruff + mypy u root `pyproject.toml`
- [x] `.github/workflows/ci.yaml` (sync-worker + ingestion-worker build)
- [x] pytest baseline (`test_health`, `test_errors`)

### P2 — runtime kvalitet

| Iz projekta 2 | Akcija u monolitu |
|---------------|-------------------|
| `CortexError` hijerarhija + middleware | uvesti u `cortex-core` + `cortex-server` |
| `correlation.py` middleware | observability + request tracing |
| `ServiceRegistry` + `register.py` | postepena migracija sa `app.state` |
| Alembic | baseline migracija iz `infra/postgres/init.sql` |

### P2 — runtime kvalitet

- [x] `CortexError` hijerarhija + `ErrorResponse` + middleware
- [x] `ServiceRegistry` + `register.py` po HTTP modulima
- [x] Alembic baseline (`alembic/versions/001_baseline_schema.py`)

### P3 — hexagonal layout + AD SSO

- [x] `module-documents` hexagonal pilot
- [x] `module-platform` AD SSO stub (`/auth/sso/url`, `/auth/sso/callback`)
- [x] `module-chat` `ChatStorePort`
- [x] `register.py` za dms-sync / ingestion

Projekat 2 dokumentuje (referenca):

```
module_*/
  domain/
  ports/
  services/
  adapters/
  register.py
```

Monolit danas koristi `services/`, `repositories/`, `routes/` — **ne big-bang** prebacivanje, već novi kod u novim feature-ima prati hexagonal gde ima smisla.

## Mapiranje modula (projekat 2 → monolit)

| Projekat 2 | Monolit |
|------------|---------|
| `module-platform` (auth, cases, documents, chat, sync) | `module-platform` + `module-documents` + `module-chat` + `module-sync` |
| `module-alfresco` | `module-dms-sync` |
| `module-ingestion` | `module-ingestion` (isto, ali lifecycle preko documents) |
| `module-ai` | `module-ai` (+ `agents/rag`, `legal`, `nlp`) |
| `cortex-worker` | `sync-worker` + `ingestion-worker` |

## Šta namerno NE preuzimamo iz projekta 2

- Povratak na jedan `cortex-worker` i `module-alfresco` ime.
- ORM duplikati u worker modulima.
- Direktan cross-module import servisa (samo facade ostaje).
- Mikroservisni extract kao default — monolit ostaje primarna arhitektura.

## Post-P3 hardening (arhitektura za tim)

- [x] `create_documents_module()` + `worker_deps.py` za Celery
- [x] Cleanup: mrtvi ORM u platform, legacy schema re-export, ingestion models shim
- [x] CI zelen (`make flct`)
- [x] [ARCHITECTURE-READY.md](ARCHITECTURE-READY.md) + [prvi-feature.md](onboarding/prvi-feature.md)
- [x] `cortex_connectors/factory.py` (stub selection)
- [ ] Produkt E2E (sync → ready, RAG, AD) — tim feature PR-ovi

## Sledeći koraci (redosled za tim)

1. Pročitati [onboarding/README.md](onboarding/README.md) i [ARCHITECTURE-READY.md](ARCHITECTURE-READY.md).
2. Pokrenuti `make install && make dev` (ili `scripts/dev.sh`).
3. Pre svakog PR-a: `make flct`.
4. Implementirati feature prema [onboarding/gde-sta-ide.md](onboarding/gde-sta-ide.md) i [prvi-feature.md](onboarding/prvi-feature.md).
