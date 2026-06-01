---
name: code-review
description: >-
  Pre-commit review of local changes — architecture alignment (module boundaries,
  lifecycle, facades), security, correctness, tests, and quality. Read-only analysis
  with prioritized findings. Invoke via /code-review before git commit.
disable-model-invocation: true
---

# Pre-Commit Code Review (Cortex monolith)

**Read-only review** of your changes before `git commit`. Produces a structured report — does **not** edit code unless you explicitly ask to fix findings afterward.

Goal: catch architecture violations, missing tests, and risky patterns **before** CI and human PR review.

## Phase 0 — Scope the diff

Determine what to review (default: **all local changes** vs last commit):

```bash
git status --short
git diff --stat
git diff --name-only
git diff --cached --name-only   # staged only
```

**Variants:**

| User says | Scope |
|-----------|--------|
| `/code-review` | Unstaged + staged vs `HEAD` |
| `/code-review staged` | Staged only (`--cached`) |
| `/code-review vs main` | `git diff main...HEAD` (+ working tree if asked) |

If no changes: report "nothing to review" and stop.

Build a **file list** grouped by area:

- `packages/module-*`
- `apps/*`
- `libs/*`
- `apps/web-client/*`
- config (Makefile, pyproject.toml, .github/, .cursor/)

Skip reviewing unrelated files the user did not touch unless they affect boundaries (e.g. `pyproject.toml` import-linter).

## Phase 1 — Automated checks (run, do not skip)

Run what applies to the diff:

```bash
make lint-imports    # if any packages/libs/apps Python or pyproject import-linter changed
make flct              # full gate — preferred before commit; if too slow, run at least affected tests
```

If `make flct` fails, include failures in the report as **BLOCKER** findings before semantic review.

For partial scope:

```bash
uv run poe lint-imports
uv run pytest <relevant test paths> -v
```

**Do not commit** with BLOCKER items unresolved.

## Phase 2 — Parallel read-only review (4 lenses)

Launch **four** Task subagents in **one message**: `subagent_type: "explore"`, `readonly: true`.

Pass each agent: the file list, `git diff` summary (or key hunks), and its lens prompt.

### Agent A — Architecture (highest priority for this repo)

```
Read-only review: ARCHITECTURE — Cortex modular monolith

Changed files: <list>

Check against invariants:
1. Feature in correct module (platform / documents / chat / sync / dms-sync / ingestion / ai)
2. Cross-module calls ONLY via module_*/api.py facades — no internal imports
3. Document.status changed ONLY via DocumentsModule.mark_* — never direct ORM in workers
4. Celery: task names from cortex_core.messaging.tasks — no hardcoded strings; no dms-sync → ingestion import (queue only)
5. Thin app shell — no domain logic in apps/*/main.py
6. Routes call facades only — no SQL/ORM in routes
7. ORM only in libs/cortex-models — no duplicated models
8. New port in cortex-core vs adapter in cortex-connectors — correct layer?
9. import-linter: would new imports violate module-boundaries.md?

Output format:
- BLOCKER / SHOULD FIX / SUGGESTION
- file:line — issue — recommended fix
- "No architecture issues" if clean
```

### Agent B — Security & auth

```
Read-only review: SECURITY

Changed files: <list>

Focus: SQL injection, shell injection, secrets in code, auth bypass, missing JWT checks,
IDOR on case/document resources, unsafe user input in LLM prompts, logging secrets,
SSO stub mistakes, CORS misconfig.

Output: BLOCKER / SHOULD FIX / SUGGESTION + file:line + fix
```

### Agent C — Correctness & async

```
Read-only review: CORRECTNESS

Changed files: <list>

Focus: logic bugs, edge cases (empty, None), error handling, transaction/session boundaries,
Celery idempotency, race conditions in sync→ingest chain, wrong status transitions,
breaking API contracts, Pydantic schema drift vs routes.

Output: BLOCKER / SHOULD FIX / SUGGESTION + file:line + fix
```

### Agent D — Tests & maintainability

```
Read-only review: TESTS & MAINTAINABILITY

Changed files: <list>

Focus: missing tests for new behavior, weak assertions, untested error paths,
function size, naming, duplication, type hints (mypy), English comments/docstrings.

Output: BLOCKER / SHOULD FIX / SUGGESTION + file:line + fix
```

If diff is **small** (<5 files, one module), a single agent pass is OK — still cover all four lenses in one report.

If diff is **large** (>30 files), split by directory and run a second wave.

## Phase 3 — Synthesize report

Merge subagent output. De-duplicate. Produce this structure:

```markdown
# Pre-commit review

**Scope:** N files | `<branch>` | staged/unstaged
**Automated:** lint-imports ✅/❌ | flct ✅/❌

## Verdict

🟢 **OK to commit** — no blockers (minor suggestions optional)
🟡 **Fix should-fix items first** — no blockers but important gaps
🔴 **Do not commit** — blockers present

## Executive summary (max 5 bullets)

- …

## Blockers (must fix)

| # | Area | Location | Issue | Fix |
|---|------|----------|-------|-----|

## Should fix

| # | Area | Location | Issue | Fix |
|---|------|----------|-------|-----|

## Suggestions (optional)

- …

## Architecture checklist

- [ ] Correct owning module
- [ ] Facade-only cross-module
- [ ] Document lifecycle via DocumentsModule (if touched)
- [ ] Celery task constants (if touched)
- [ ] make lint-imports passed (if boundaries touched)
- [ ] Tests added/updated for behavior change

## What looks good

- … (always include — at least one positive note if earned)

## Recommended next steps

1. Fix blockers → re-run `/code-review`
2. Run `/flct` if not already green
3. Commit with conventional message
4. `/update-docs` if module boundaries or public API changed
```

## Phase 4 — After review

- **Do not** auto-fix unless user says "fix blockers" or "apply review fixes"
- If user wants fixes → address BLOCKER first, then SHOULD FIX, then re-run `/code-review` or `/flct`
- Suggest new `.cursor/rules/` entry if the same violation appears (see `suggesting-cursor-rules` skill)

## Severity guide

| Level | Meaning |
|-------|---------|
| **BLOCKER** | Architecture invariant broken, security hole, flct failure, data/lifecycle corruption risk |
| **SHOULD FIX** | Missing tests, weak error handling, maintainability that will hurt PR review |
| **SUGGESTION** | Nice-to-have, style, minor naming |

## When to run

- **Before every commit** on non-trivial changes
- After completing a feature branch locally, before push
- After AI-generated code — especially cross-module changes

## When not enough

- Does not replace `/flct` — run both: `/code-review` then `/flct`
- Does not replace human PR review or security sign-off for production
- UI visual bugs → also `verifying-in-browser` for web-client changes

## Related

- [feature-placement.md](../../../docs/engineering/how-we-work/feature-placement.md)
- [module-boundaries.md](../../../docs/engineering/architecture/module-boundaries.md)
- [first-pr-checklist.md](../../../docs/engineering/how-we-work/first-pr-checklist.md)
- `/flct` — quality gate after fixing findings
