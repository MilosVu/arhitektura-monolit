# ADR 0005: `cortex-models` as single ORM source

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

Worker packages and platform duplicated ORM definitions (`Document`, `Case`, `SyncJob`). Schema drift and migration confusion followed.

## Options

### Option A — Shared `libs/cortex-models`

All SQLAlchemy models in one package; modules import from there.

- **Pros:** One migration source, no drift, clear ownership of schema.
- **Cons:** All modules depend on shared models lib (acceptable for monolith).

### Option B — Per-module ORM copies

Each module owns its slice of models.

- **Pros:** Theoretical module isolation.
- **Cons:** Duplication, inconsistent schema, broken joins.

## Decision

Create **`libs/cortex-models`** as the **only** ORM source. Move models from `module-platform`; remove duplicates from worker packages.

## Consequences

- Alembic migrations target `cortex-models` metadata.
- Modules use repositories/services against shared models; no local model copies.
- `cortex-core` does not contain ORM entities.

## References

- [history/refactor-plan.md](history/refactor-plan.md) — file mapping section
