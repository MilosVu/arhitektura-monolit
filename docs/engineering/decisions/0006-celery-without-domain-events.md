# ADR 0006: Celery task queue without domain events

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

After sync completes, ingestion must run; after ingestion, documents become ready. We needed async orchestration without adding an event bus or saga framework in the first refactor.

## Options

### Option A — Celery task chain with named constants

`module-sync` enqueues sync; `module-dms-sync` enqueues ingest via `TASK_INGEST_DOCUMENT`; lifecycle via `DocumentsModule`.

- **Pros:** Simple, already in stack, easy to debug with Flower.
- **Cons:** Implicit workflow in task code; no event replay.

### Option B — Domain events + outbox

Publish `DocumentSynced`, `DocumentReady` events; consumers react.

- **Pros:** Loose coupling, audit trail of events.
- **Cons:** Extra infra, complexity not justified yet.

## Decision

Keep **Celery task queue** as the integration mechanism. Use **`cortex_core.messaging.tasks`** constants for task names. No domain event bus for now.

## Consequences

- Task names must not be hardcoded in feature code.
- `module-dms-sync` must not import `module-ingestion` — only send Celery tasks.
- `SyncOrchestrator` in `module-sync` coordinates job creation and polling.

## References

- [history/refactor-plan.md](history/refactor-plan.md) — section 14 (what we do NOT do)
