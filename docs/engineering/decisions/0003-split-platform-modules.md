# ADR 0003: Split platform into chat, sync, and documents modules

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

`module-platform` originally contained auth, cases, documents, chat, sync, audit, and AI delegation. The module grew too broad and violated single-responsibility for import boundaries and team ownership.

## Options

### Option A — Split by domain

Extract `module-documents`, `module-chat`, and `module-sync`; platform keeps auth, cases, audit, system.

- **Pros:** Clear ownership, smaller facades, independent evolution.
- **Cons:** More packages and router wiring in cortex-server.

### Option B — Keep monolithic platform module

Leave all HTTP features in one module with internal folders.

- **Pros:** Fewer packages.
- **Cons:** Continued coupling; hard to enforce boundaries.

## Decision

Split platform into **four HTTP modules**: `module-platform` (auth, cases, audit, system), `module-documents`, `module-chat`, `module-sync`. Each exposes its own `api.py` and routes.

## Consequences

- `cortex-server/main.py` mounts separate routers per module.
- Platform may call other modules only via their facades (e.g. list cases, delegate to AI).
- Chat persists in Redis via `module-chat`; AI generates streams via `module-ai`.

## References

- [architecture/module-boundaries.md](../architecture/module-boundaries.md)
