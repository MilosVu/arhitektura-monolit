# AGENTS.md — Guide for AI Assistants and the Team

## AI rules

Detailed operative rules: [.cursor/rules/README.md](.cursor/rules/README.md).

## Documentation


| Doc                                                                                        | Purpose                      |
| ------------------------------------------------------------------------------------------ | ---------------------------- |
| [docs/README.md](docs/README.md)                                                           | Product vs engineering split |
| [docs/engineering/README.md](docs/engineering/README.md)                                   | Developer onboarding         |
| [docs/engineering/decisions/README.md](docs/engineering/decisions/README.md)               | ADRs                         |
| [docs/engineering/how-we-work/feature-placement.md](docs/engineering/how-we-work/feature-placement.md) | Feature placement            |


## Commands

```bash
make infra-up && make install && make dev
make lint-imports    # after boundary changes
make flct            # format + lint + mypy + import-linter + test
make db-setup        # alembic upgrade head
```

Scripts: `scripts/dev.sh`, `scripts/seed-neo4j.sh`.

## Invariants

1. Thin app shell — no domain logic in `apps/*/main.py`
2. Facade only — cross-module via `module_*/api.py`
3. `Document.status` — only `DocumentsModule.mark_*()`
4. Celery — constants from `cortex_core.messaging.tasks`
5. After boundary changes — `make lint-imports`
6. ORM — only `cortex-models`

## New architectural decision

Use [docs/engineering/decisions/template.md](docs/engineering/decisions/template.md) and add an ADR under `docs/engineering/decisions/`.

## Do not

- Reintroduce `module-alfresco` or `cortex-worker`
- Import `module_ai.agents` from other modules
- Write `Document.status` directly in workers

Auth target: AD/SSO via frontend → backend validation → local User for RBAC. See [docs/engineering/how-we-work/auth.md](docs/engineering/how-we-work/auth.md).