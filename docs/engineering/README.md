# Engineering — Internal Documentation

Starting point for the **development team**: architecture, onboarding, decisions, and how we work.

## Required reading (in order)

1. [architecture/overview.md](architecture/overview.md) — what the system does, integrations, tech stack
2. [architecture/module-boundaries.md](architecture/module-boundaries.md) — module boundaries and facade API
3. [how-we-work/feature-placement.md](how-we-work/feature-placement.md) — **where to implement** a new feature
4. [how-we-work/hexagonal-layout.md](how-we-work/hexagonal-layout.md) — ports/adapters, layering
5. [how-we-work/repository-structure.md](how-we-work/repository-structure.md) — folders, naming
6. [how-we-work/auth.md](how-we-work/auth.md) — AD/SSO flow vs mock MVP
7. [how-we-work/local-development.md](how-we-work/local-development.md) — running locally, ports, Makefile
8. [how-we-work/cursor-for-the-team.md](how-we-work/cursor-for-the-team.md) — **Cursor rules, skills, slash commands**
9. [how-we-work/first-pr-checklist.md](how-we-work/first-pr-checklist.md) — before merge
10. [architecture/architecture-ready.md](architecture/architecture-ready.md) — architecture ready for the team
11. [how-we-work/first-feature.md](how-we-work/first-feature.md) — first PR walkthrough

## Architectural decisions (ADR)

Why something was built a certain way → [decisions/README.md](decisions/README.md)

Implementation plans (multi-phase features) → [plans/](plans/)

## Reference

- [reference/comparison-project-2.md](reference/comparison-project-2.md) — what we take from reference project 2
- [decisions/history/refactor-plan.md](decisions/history/refactor-plan.md) — full refactor plan (history)

## AI assistants

Human-readable guide: [how-we-work/cursor-for-the-team.md](how-we-work/cursor-for-the-team.md)

- Entry point: [AGENTS.md](../../AGENTS.md)
- Cursor rules: [.cursor/rules/README.md](../../.cursor/rules/README.md)
- Cursor skills: [.cursor/skills/README.md](../../.cursor/skills/README.md) — `/onboard`, `/flct`, etc.

## Quick start

```bash
make infra-up
make install
make lint-imports
make dev
```

- App: http://localhost:5174
- API: http://localhost:8000
- Flower: http://localhost:5555
- MVP login: `hmueller` / `mock`

## Golden rules

1. **One module = one domain**
2. **Cross-module only via `api.py`**
3. **`Document.status` only in `module-documents`**
4. **Celery** — constants from `cortex_core.messaging.tasks`
5. **`make lint-imports`** after boundary changes

## New decision or open question?

1. Open [decisions/template.md](decisions/template.md)
2. Create `NNNN-short-title.md` in `decisions/`
3. Add a row to the index in [decisions/README.md](decisions/README.md)
4. If module boundaries change → update [architecture/module-boundaries.md](architecture/module-boundaries.md)
