---
name: cortex-onboard
description: >-
  Warm-start for Cortex modular monolith — read AGENTS.md, engineering docs, and
  relevant rules before implementing. Use at the start of a new chat, when onboarding
  a developer, or before a cross-module feature. Invoke via /onboard.
disable-model-invocation: true
---

# Cortex Onboard

Load project context before writing code. **Do not implement anything until step 4 is complete.**

## 1. Read core docs (in order)

Use the Read tool on each file — do not skip or summarize from memory:

1. `AGENTS.md`
2. `docs/engineering/README.md`
3. `docs/engineering/how-we-work/feature-placement.md`
4. `docs/engineering/architecture/module-boundaries.md`

If the user mentions a specific area, also read:

| Area | Additional doc |
|------|----------------|
| HTTP endpoint | `docs/engineering/how-we-work/first-feature.md` |
| Celery / worker | `.cursor/rules/celery-workers.mdc`, `.cursor/rules/documents-lifecycle.mdc` |
| AI / RAG | `.cursor/rules/ai-agents.mdc`, `docs/engineering/decisions/0008-searchport-weaviate.md` |
| Frontend | `.cursor/skills/frontend-dev-starter/SKILL.md`, `apps/web-client/ONBOARDING.md` |
| Architecture history | `docs/engineering/decisions/README.md` |

## 2. Confirm invariants (must remember)

1. Thin app shell — no domain logic in `apps/*/main.py`
2. Cross-module only via `module_*/api.py` facades
3. `Document.status` only via `DocumentsModule.mark_*()` — never direct ORM in workers
4. Celery task names from `cortex_core.messaging.tasks` constants
5. ORM only in `libs/cortex-models`
6. After boundary changes → `make lint-imports`
7. Before merge → `make flct`

## 3. Optional deep explore

If the task spans multiple modules or the codebase is unfamiliar, launch **parallel explore subagents** (see `parallel-exploring` skill):

- Agent A: owning module + routes (`packages/module-*/`)
- Agent B: shared libs + ports (`libs/cortex-core/`, `cortex-connectors/`)
- Agent C: app wiring (`apps/cortex-server/main.py`, worker shells)

## 4. Reply with onboarding summary

Post a short summary (no code yet):

- **Repo map** — 7 modules + 2 workers in one sentence each
- **Where this task belongs** — module + typical files
- **Risks** — boundary violations, lifecycle, Celery chain
- **Ask** — what the user wants to build or fix

Wait for the user's task before editing files.
