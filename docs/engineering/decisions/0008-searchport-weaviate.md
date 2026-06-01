# ADR 0008: `SearchPort` — ingestion write, AI read

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

Weaviate access was duplicated: ingestion wrote chunks/embeddings; AI read for RAG. Without a shared contract, schema changes and client config diverged.

## Options

### Option A — `SearchPort` in `cortex-core`

Port interface in core; write adapter in ingestion, read adapter in AI.

- **Pros:** Single contract, modules stay decoupled, testable fakes.
- **Cons:** Two adapter implementations to maintain.

### Option B — Shared Weaviate module imported everywhere

- **Pros:** One client wrapper file.
- **Cons:** Violates module boundaries (ingestion ↔ ai coupling).

## Decision

Define **`SearchPort`** in **`cortex-core`**. **`module-ingestion`** implements write (upsert chunks). **`module-ai`** implements read (hybrid search for RAG). No direct Weaviate imports across modules.

## Consequences

- Weaviate client details live in module adapters or `cortex-connectors`.
- `module-ai` must not depend on `module-ingestion` — only on SearchPort read side.
- Integration tests can stub SearchPort without Weaviate.

## References

- [architecture/module-boundaries.md](../architecture/module-boundaries.md)
