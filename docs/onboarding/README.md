# Onboarding — Cortex modularni monolit

Dobrodošli u `arhitektura-monolit/`. Ovo je **početna tačka** za development tim: gde pišemo kod, kako moduli komuniciraju i šta proveriti pre PR-a.

## Obavezno čitanje (redosled)

1. [ARCHITECTURE_OVERVIEW.md](../../ARCHITECTURE_OVERVIEW.md) — šta sistem radi, integracije, tech stack
2. [MODULE-BOUNDARIES.md](../../MODULE-BOUNDARIES.md) — granice modula i facade API
3. [gde-sta-ide.md](gde-sta-ide.md) — **gde implementirati** novi feature (decision table)
4. [hexagonal-layout.md](hexagonal-layout.md) — ports/adapters, layering unutar modula
5. [struktura-repozitorijuma.md](struktura-repozitorijuma.md) — folderi, layering, imenovanje
6. [auth.md](auth.md) — AD/SSO tok (produkcija) vs mock (MVP)
7. [lokalni-razvoj.md](lokalni-razvoj.md) — pokretanje, portovi, Makefile/scripts
8. [checklist-prvi-pr.md](checklist-prvi-pr.md) — pre merge-a
9. [ARCHITECTURE-READY.md](../ARCHITECTURE-READY.md) — kada je arhitektura spremna za tim
10. [prvi-feature.md](prvi-feature.md) — walkthrough za prvi PR

## Referenca za AI asistente

- Repo root: [AGENTS.md](../../AGENTS.md)
- Cursor rules: `.cursor/rules/` u workspace root-u (`Architecture/.cursor/rules/`)

## Uporedba sa drugim primerom

Ideje skupljamo iz `arhitektura-monolit-projekat-2/`, menjamo samo monolit:

- [UPOREDBA-PROJEKAT-2.md](../UPOREDBA-PROJEKAT-2.md)

## Brzi start

```bash
cd arhitektura-monolit
make infra-up
make install
make lint-imports
make dev
```

- App: http://localhost:5174
- API: http://localhost:8000
- Flower: http://localhost:5555
- MVP login: `hmueller` / `mock` (zamenjuje se AD SSO)

## Repo mapa (gde šta živi)

```
arhitektura-monolit/
├── apps/
│   ├── cortex-server/      # FastAPI composition root (bez domenske logike)
│   ├── sync-worker/        # Celery -Q sync
│   ├── ingestion-worker/   # Celery -Q ingestion
│   └── web-client/         # React frontend (Vite)
├── packages/               # domen moduli (module-*)
├── libs/                   # shared: core, models, connectors, observability
├── infra/                  # docker-compose, k8s, postgres init
├── scripts/                # dev pomoćne skripte
└── docs/                   # tim dokumentacija
```

## Zlatna pravila (kratko)

1. **Jedan modul = jedna domena** — ne mešaj documents u platform.
2. **Cross-module samo preko `api.py`** — nikad `module_ai.agents` iz drugog modula.
3. **`Document.status` samo u `module-documents`** — workeri zovu `DocumentsModule.mark_*`.
4. **Celery** — konstante iz `cortex_core.messaging.tasks`, lanac preko queue-a ne importa.
5. **`make lint-imports`** posle svake promene granica modula.

## Kontakt sa arhitekturom

Veći refactor ili nova granica modula → ažuriraj `MODULE-BOUNDARIES.md`, `pyproject.toml` (import-linter) i `REFACTOR-PLAN.md`.
