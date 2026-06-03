# Architecture Decision Records (ADR)

We record **architectural decisions**, trade-offs, and open questions here. Each decision has its own file — easy to track history and rationale.

## How to use

1. Copy [template.md](template.md)
2. Name the file: `NNNN-short-title.md` (e.g. `0009-redis-cluster-mode.md`)
3. Fill sections: context → options → decision → consequences
4. Add a row to the index below
5. Status:
   - **proposed** — open question, no decision yet
   - **accepted** — decision in effect
   - **deprecated** — replaced by a newer decision (link new ADR)
   - **superseded** — explicitly replaced

## Decision index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-modular-monolith.md) | Modular monolith as primary architecture | accepted | 2025 |
| [0002](0002-documents-module-status-ownership.md) | `module-documents` owns `Document.status` | accepted | 2025 |
| [0003](0003-split-platform-modules.md) | Split platform: chat, sync, documents | accepted | 2025 |
| [0004](0004-split-sync-ingestion-workers.md) | Two Celery worker deployables | accepted | 2025 |
| [0005](0005-cortex-models-single-orm-source.md) | `cortex-models` as single ORM source | accepted | 2025 |
| [0006](0006-celery-without-domain-events.md) | Celery task queue without domain events | accepted | 2025 |
| [0007](0007-module-dms-sync-naming.md) | DMS-agnostic name (`module-dms-sync`) | accepted | 2025 |
| [0008](0008-searchport-weaviate.md) | `SearchPort` — ingestion write, AI read | accepted | 2025 |
| [0009](0009-law-corpus-sync.md) | `module-law-sync` — Swiss law corpus ingestion | accepted | 2026-06-01 |

## History

Full big-bang refactor plan (checklist, file mapping): [history/refactor-plan.md](history/refactor-plan.md)

## Related

- [architecture/module-boundaries.md](../architecture/module-boundaries.md) — current module boundaries
- [reference/comparison-project-2.md](../reference/comparison-project-2.md) — comparison with reference project
