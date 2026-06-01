# ADR 0002: `module-documents` owns `Document.status`

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

Before refactor, `Document.status` was updated from platform, alfresco, and ingestion code paths. That caused inconsistent lifecycle, duplicate ORM logic, and unclear ownership.

## Options

### Option A — Central lifecycle in `module-documents`

Only `DocumentsModule.mark_*()` methods change status; workers call the facade.

- **Pros:** Single source of truth, auditable transitions, import-linter enforceable.
- **Cons:** Extra facade calls from workers.

### Option B — Distributed status updates

Each module updates status when it finishes its step.

- **Pros:** Fewer cross-module calls.
- **Cons:** Race conditions, duplicated rules, hard to reason about state.

## Decision

**`module-documents` is the sole owner** of `Document.status`. Workers and other modules call `DocumentsModule.mark_syncing`, `mark_ingesting`, `mark_ready`, `mark_failed` — never direct ORM writes.

## Consequences

- Lifecycle methods live in `module_documents/api.py`.
- Import-linter forbids worker modules from importing document ORM for status writes.
- Document CRUD HTTP routes live in `module-documents`, not platform.

## References

- [history/refactor-plan.md](history/refactor-plan.md) — section 7 (DocumentsModule API)
