---
name: parallel-exploring
description: >-
  Explore the Cortex modular monolith in parallel with read-only subagents. Use when
  mapping architecture, finding where a feature lives, or investigating cross-module flows
  (sync → ingest → ready, chat → AI, RAG).
---

# Parallel Explore (Cortex monolith)

Launch multiple **explore** subagents in **one message** so they run concurrently. Each agent is read-only.

## When to use

- "Where is X handled?"
- Cross-module flow (sync job → dms-sync → ingestion → document ready)
- Before a large feature — map touch points
- Complement to `/onboard` when the task is specific

For a single known file path, use Grep or Read directly — subagents are for breadth.

## Default parallel layout (5 agents)

**Agent 1 — HTTP modules & routes**

> Explore `apps/cortex-server/cortex_server/main.py` and `packages/module-*/module_*/routes/`.
> List routers, prefixes, and which module owns each. Report facade deps pattern.

**Agent 2 — Document lifecycle & workers**

> Explore `module-documents/api.py`, `module-dms-sync/tasks.py`, `module-ingestion/tasks.py`,
> `apps/sync-worker/`, `apps/ingestion-worker/`. How does status change? Celery task chain?

**Agent 3 — Shared libs & ports**

> Explore `libs/cortex-core/`, `cortex-models/`, `cortex-connectors/`.
> List ports (SearchPort, etc.), ORM entities, settings entry points.

**Agent 4 — Platform & auth**

> Explore `module-platform/` — auth, cases, audit, SSO stubs. JWT flow, deps, routes.

**Agent 5 — Frontend API surface**

> Explore `apps/web-client/src/api/` and `vite.config` proxy. What endpoints does UI call?

Use `subagent_type: "explore"` and `readonly: true`. Set thoroughness to **medium** unless the user asks for exhaustive.

## Synthesize

Combine agent reports into:

1. **Data flow** — user action → HTTP → module → queue → worker → storage
2. **Owning module** for the user's question
3. **Key files** (3–7 paths) to edit
4. **Boundary risks** — forbidden imports, lifecycle rules

## Module quick reference

| Domain | Package |
|--------|---------|
| Auth, cases, audit | `module-platform` |
| Documents, status | `module-documents` |
| Chat, Redis | `module-chat` |
| Sync jobs | `module-sync` |
| DMS delta | `module-dms-sync` |
| OCR, embed | `module-ingestion` |
| RAG, agents | `module-ai` |

See `.cursor/rules/feature-placement.mdc` for full table.
