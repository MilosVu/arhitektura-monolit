# ADR 0001: Modular monolith as primary architecture

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

Cortex AI needs a backend that supports document sync, ingestion, RAG, and chat with clear domain boundaries, but without the operational cost of many microservices at the current team size.

## Options

### Option A — Modular monolith

Single deployable with strict module boundaries enforced by import-linter; optional future extract of hot paths.

- **Pros:** Simple ops, shared DB transactions, fast refactors across modules via facades.
- **Cons:** All modules deploy together; requires discipline to avoid coupling.

### Option B — Microservices from day one

Separate services for platform, sync, ingestion, AI, etc.

- **Pros:** Independent scaling and deploy per service.
- **Cons:** High infra and coordination overhead; premature for current scale.

## Decision

Adopt a **modular monolith**: one repo, seven domain modules, thin app shells, facade-only cross-module calls. Microservice extract is a future option when metrics justify it.

## Consequences

- `apps/cortex-server`, `sync-worker`, and `ingestion-worker` are composition roots only.
- Module boundaries documented in [architecture/module-boundaries.md](../architecture/module-boundaries.md).
- Import-linter contracts in root `pyproject.toml`.

## References

- [architecture/overview.md](../architecture/overview.md)
- [history/refactor-plan.md](history/refactor-plan.md)
