---
name: systematic-debugging
description: >-
  Structured debug workflow for Cortex — reproduce, isolate by module/layer, hypothesize,
  verify. Celery sync chain, document lifecycle, Flower, API vs worker. Use when sync,
  ingestion, or status stuck/wrong.
---

# Systematic Debugging (Cortex monolith)

Debug methodically — especially **async pipelines** (sync → dms-sync → ingestion → `ready`).

## 1. Reproduce

Before changing code:

- Exact steps (UI, API curl, or Celery trigger)
- Expected vs actual (`Document.status`, `SyncJob` state, HTTP code)
- Environment: `make dev` running? Both workers up? Flower at :5555?
- Consistent or intermittent?

If intermittent → suspect race, queue backlog, or missing `await`/commit.

**Quick health:**

```bash
curl -s http://localhost:8000/health
# Flower: http://localhost:5555
# docker compose / make infra-up — postgres, redis, rabbitmq up?
```

## 2. Isolate by layer

Use binary search — don't guess across the whole monolith.

```
User / web-client
    → cortex-server (HTTP)
        → module-sync (SyncOrchestrator, job create)
            → RabbitMQ queue sync
                → module-dms-sync (TASK_SYNC_CASE)
                    → DocumentsModule.mark_syncing
                    → Blob download
                    → TASK_INGEST_DOCUMENT
                        → module-ingestion
                            → DocumentsModule.mark_ingesting → mark_ready
```

**Which layer?**

| Check | How |
|-------|-----|
| HTTP / auth | curl with JWT; server logs |
| Sync job created? | DB `SyncJob`, API `GET /sync/{job_id}` |
| Celery task sent? | Flower — task received? queue `sync` / `ingestion` |
| Worker running? | terminals: `sync-worker`, `ingestion-worker` |
| Document status | DB or API — only changed via `DocumentsModule`? |
| DMS / Blob | dms-sync logs, connector stubs |
| Weaviate / ingestion | ingestion worker logs, SearchPort write |

**Git bisect** (regression):

```bash
git bisect start
git bisect bad
git bisect good <last-known-good-sha>
# test reproduction at each step
git bisect reset
```

## 3. Hypothesize

State a **testable** hypothesis:

- Good: "Status stays `syncing` because `TASK_INGEST_DOCUMENT` never enqueued — check `module_dms_sync/tasks.py` send_task call."
- Bad: "Sync is broken."

Common Cortex-specific causes:

- Worker sets `doc.status` directly → **forbidden** — must use `DocumentsModule.mark_*`
- Hardcoded Celery task string → use `cortex_core.messaging.tasks` constants
- Cross-module import instead of facade → import-linter or runtime import error
- Wrong queue — sync task on `ingestion` queue or vice versa
- `create_documents_module()` / worker DI not wired in worker shell
- Only one worker running (ingestion never picks up task)

## 4. Verify hypothesis

Minimal evidence:

- Add temporary logging at **one** boundary (route → facade → task enqueue)
- Flower: task name, args, state
- pytest for the isolated unit (preferred over prod logging)
- Read terminal output from failing worker — full stack trace

If wrong → new hypothesis. Document what you ruled out.

## 5. Fix and verify

- **Minimal fix** at root cause
- Re-run reproduction end-to-end
- `make flct` before commit
- Add a test that would catch regression (see `python-tdd-with-uv` skill)

## Debugging tools

| Scenario | Tool |
|----------|------|
| Celery task flow | Flower :5555, worker terminal logs |
| HTTP surface | curl + `/api-smoke`, server uvicorn logs |
| Module map | `parallel-exploring` skill |
| Import violation | `make lint-imports` |
| Local full stack | `make dev`, `scripts/dev.sh` |
| DB state | psql / API document + sync job endpoints |

## Rules

- Never bypass `DocumentsModule` lifecycle to "unstick" status
- Never fix symptoms (retry in UI only) without finding enqueue/status bug
- After 15 min stuck → re-isolate layer; use `parallel-exploring` for map
- Do not import `module_ai.agents` or other modules' internals across boundaries

## Related

- [ADR 0002](../../../docs/engineering/decisions/0002-documents-module-status-ownership.md) — status ownership
- [ADR 0006](../../../docs/engineering/decisions/0006-celery-without-domain-events.md) — Celery chain
- `.cursor/rules/celery-workers.mdc`, `.cursor/rules/documents-lifecycle.mdc`
