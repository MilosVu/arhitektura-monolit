# ADR 0004: Two Celery worker deployables

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

Sync (DMS I/O, network-bound) and ingestion (OCR, embedding, CPU/GPU) have different resource profiles. A single `cortex-worker` forced one scaling and deploy model for both.

## Options

### Option A — Split workers

`apps/sync-worker` (-Q sync) and `apps/ingestion-worker` (-Q ingestion).

- **Pros:** Independent scaling, queue isolation, clearer failure domains.
- **Cons:** Two K8s deployments and images to maintain.

### Option B — Single worker, multiple queues

One Celery worker consumes both queues.

- **Pros:** One deployable.
- **Cons:** Ingestion load can starve sync; cannot scale profiles independently.

## Decision

Replace `cortex-worker` with **`sync-worker`** and **`ingestion-worker`**. Domain logic stays in `module-dms-sync` and `module-ingestion`; app folders are thin Celery shells.

## Consequences

- K8s: two worker deployments instead of one.
- Makefile targets: `dev-sync-worker`, `dev-ingestion-worker`.
- Cross-step chaining via Celery task constants, not direct module imports.

## References

- [history/refactor-plan.md](history/refactor-plan.md) — sections 11–12
