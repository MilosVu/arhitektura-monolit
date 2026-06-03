# ADR 0009: `module-law-sync` — Swiss law corpus ingestion

- **Status:** accepted
- **Date:** 2026-06-01
- **Author(s):** architecture team

## Context

Cortex needs a **Swiss legal corpus** from day one: federal and cantonal laws, **versioned** over time, fetched from official APIs and (where needed) web scraping. The corpus must support:

- **Structured lookup** — citations, relationships (`AMENDS`, `CITES`, temporal validity)
- **Semantic search** — chunked embeddings for law RAG (separate from case-document RAG)
- **Audit / re-index** — canonical text stored as Markdown per version

Today, `module-ai` only **reads** a small Neo4j seed (`LawLinkAgent`, `GET /laws/{ref}`). There is no ingestion pipeline, no versioning model, and no separation between case `DocumentChunk` and law chunks in Weaviate.

Requirements from the start:

- Immutable **version records** (`valid_from` / `valid_to`)
- **Federal vs cantonal** jurisdiction
- **Four storage roles**: PostgreSQL (catalog), Blob (MD archive), Neo4j (graph), Weaviate (`LawChunk` collection)
- Async sync via Celery (I/O-bound, like DMS sync)

## Options

### Option A — Extend `module-ai` with sync services and Celery tasks

Add `law_corpus_sync`, scrapers, and write adapters inside `module-ai`.

- **Pros:** Neo4j and law agents already live there; fewer packages.
- **Cons:** Mixes read (agents, HTTP) with heavy write/sync lifecycle; violates single-responsibility; harder to extract later; `module-ai` must not grow into a second ingestion worker.

### Option B — Reuse `module-ingestion` for law embed pipeline

Treat laws like documents: OCR/chunk/embed via existing ingestion tasks.

- **Pros:** Reuses Weaviate write path and embedding flow.
- **Cons:** Wrong domain — laws are not `Document` entities, no `Document.status`, different metadata (jurisdiction, version, provision ref); would pollute `SearchPort` and document lifecycle.

### Option C — New domain module `module-law-sync` (recommended)

Dedicated module owns fetch → normalize → version → Blob MD → Neo4j graph → Weaviate `LawChunk`. `module-ai` remains read-only consumer. External sources via `LawSourcePort` in `cortex-core`, adapters in `cortex-connectors`.

- **Pros:** Clear boundary (mirrors `module-dms-sync` + `module-ingestion` split for a different domain); versioning and sync jobs isolated; independent extract to microservice; separate Weaviate collection and port from case documents.
- **Cons:** Eighth domain module; import-linter contract and worker wiring must be updated.

## Decision

Adopt **Option C**: create **`module-law-sync`** as the owning domain for Swiss law corpus ingestion, versioning, and index writes.

Storage split:

| Store | Role |
|-------|------|
| **PostgreSQL** (`cortex-models`) | Source of truth for provisions, immutable versions, sync jobs |
| **Blob** (S3/MinIO via `BlobPort`) | Canonical Markdown per version (not git) |
| **Neo4j** | Graph structure, relationships, temporal nodes |
| **Weaviate** (`LawChunk` collection) | Chunk + vector index for law semantic search |

Ports in `cortex-core`:

- **`LawSourcePort`** — fetch from Fedlex API / scraper (adapters in `cortex-connectors`)
- **`LawSearchPort`** — law chunk search (read: `module-ai`, write: `module-law-sync`) — **separate from `SearchPort`** (ADR 0008 case documents)
- **`LawGraphPort`** (optional phase 1 stub) — graph read/write contract; write in law-sync, read in AI

Celery tasks run on the **`sync`** queue initially (same worker deployable as DMS sync — I/O profile). Task constants in `cortex_core.messaging.tasks`.

`module-ai` **must not** import `module-law-sync` internals — only read Neo4j / `LawSearchPort` and optionally call `LawSyncModule` facade for admin triggers.

## Consequences

### Positive

- Versioning and federal/cantonal scope are first-class from phase 1
- Case document RAG and law RAG stay isolated (`DocumentChunk` vs `LawChunk`)
- Same extract pattern as other modules (facade + Celery + connectors)

### Trade-offs

- Repo grows from 7 to **8 domain modules**; import-linter contracts must be extended
- Some text duplication (Blob MD + Neo4j content + Weaviate chunks) — acceptable for audit and re-index
- Scraping adapters need rate limiting and legal/ToS review per source

### Code and docs to change

| Area | Change |
|------|--------|
| `packages/module-law-sync/` | New package (skeleton in phase 1) |
| `libs/cortex-models/` | `LawCode`, `LawProvision`, `LawVersion`, `LawSyncJob` |
| `libs/cortex-core/` | `LawSourcePort`, `LawSearchPort`; task constants |
| `libs/cortex-connectors/` | Swiss law API / scraper stubs |
| `apps/sync-worker/` | Register law-sync Celery tasks |
| `apps/cortex-server/` | Wire `LawSyncModule` routes (sync trigger, job status) |
| `module-ai` | Read adapters; extend `LawLinkAgent`; optional law RAG |
| Docs | `module-boundaries.md`, `feature-placement.md`, `architecture.mmd` |
| Import-linter | New module contract in root `pyproject.toml` |

### Out of scope for this ADR

- Production Fedlex/scraper credentials and legal review of scraping
- Cantonal source catalog (implemented per source in connectors)
- Replacing Neo4j seed script — superseded gradually by law-sync pipeline

## References

- [plans/law-corpus-sync.md](../plans/law-corpus-sync.md) — phased implementation plan
- [0008-searchport-weaviate.md](0008-searchport-weaviate.md) — document `SearchPort` remains unchanged
- [architecture/module-boundaries.md](../architecture/module-boundaries.md)
