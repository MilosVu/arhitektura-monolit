# AGENTS.md — vodič za AI asistente i tim

Radimo u **`arhitektura-monolit/`** (modularni monolit). Referentni primer **`arhitektura-monolit-projekat-2/`** — samo čitanje ideja, **ne menjati** taj folder.

## Obavezna dokumentacija

| Dokument | Svrha |
|----------|-------|
| [docs/onboarding/README.md](docs/onboarding/README.md) | Onboarding tima |
| [docs/onboarding/gde-sta-ide.md](docs/onboarding/gde-sta-ide.md) | Gde implementirati feature |
| [MODULE-BOUNDARIES.md](MODULE-BOUNDARIES.md) | Granice modula, import-linter |
| [REFACTOR-PLAN.md](REFACTOR-PLAN.md) | Refactor istorija i odluke |
| [docs/UPOREDBA-PROJEKAT-2.md](docs/UPOREDBA-PROJEKAT-2.md) | Šta preuzeti iz projekta 2 |
| [docs/ARCHITECTURE-READY.md](docs/ARCHITECTURE-READY.md) | Arhitektura spremna za tim |
| [docs/onboarding/prvi-feature.md](docs/onboarding/prvi-feature.md) | Walkthrough prvog feature-a |

Cursor rules: `../.cursor/rules/` (workspace `Architecture/.cursor/rules/`).

## Komande

```bash
make infra-up
make install
make dev
make lint-imports
make flct          # format + lint + mypy + import-linter + test
make db-setup      # alembic upgrade head
```

Skripte: `scripts/dev.sh`, `scripts/seed-neo4j.sh`.

## Repo mapa

```
apps/cortex-server, sync-worker, ingestion-worker, web-client
packages/module-platform, module-documents, module-chat, module-sync,
         module-dms-sync, module-ingestion, module-ai
libs/cortex-core, cortex-models, cortex-connectors, cortex-observability
```

## Kritična pravila

1. **Tanak app shell** — bez domenske logike u `apps/*/main.py`.
2. **Facade only** — cross-module preko `module_*/api.py`.
3. **`Document.status`** — samo `DocumentsModule.mark_*()`.
4. **Celery** — `cortex_core.messaging.tasks` konstante.
5. **Posle promene granica** — `make lint-imports`.
6. **ORM** — samo `cortex-models`.

## Auth (cilj)

AD/SSO preko frontenda → backend validacija → lokalni User za RBAC → Alfresco po korisničkom ACL. Detalji: [docs/onboarding/auth.md](docs/onboarding/auth.md).

## Šta NE raditi

- Vraćati `module-alfresco` ili jedan `cortex-worker`.
- Importovati `module_ai.agents` iz drugih modula.
- Direktan ORM write statusa u workerima.
- Menjati `arhitektura-monolit-projekat-2/`.
