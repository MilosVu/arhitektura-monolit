---
name: babysitting-pr
description: >-
  Keep a GitHub PR merge-ready — triage CI failures, review comments, merge conflicts.
  Fix with make flct. Use when a PR is open and needs attention.
disable-model-invocation: true
---

# Babysitting a PR (Cortex monolith)

Loop until the PR is merge-ready or human input is required.

## 1. PR status

```bash
gh pr view --json number,title,state,mergeable,mergeStateStatus,statusCheckRollup,reviewDecision
gh pr checks
```

## 2. CI failures

This repo's CI runs (from `.github/workflows/ci.yaml`):

- `uv run poe ci:format`
- `uv run poe ci:lint`
- `uv run poe check` (mypy)
- `uv run poe lint-imports`
- `uv run poe test`

**Reproduce locally:**

```bash
make flct
```

Get failed job logs:

```bash
gh run view <run-id> --log-failed
```

Fix **minimal** scope — do not change CI config to make failures pass.

## 3. Review comments

- Address clear fixes (naming, null checks, boundary violations)
- Skip comments needing design decisions — report to user
- Never weaken import-linter or document lifecycle rules to appease review

## 4. Merge conflicts

```bash
git fetch origin main
git merge origin/main
```

Resolve preserving module boundaries and facade patterns. Ask user on ambiguous conflicts.

## 5. Push and re-check

```bash
git push
gh pr checks --watch
```

**Max 3 fix cycles** — then report blockers.

If many independent CI steps failed, you may launch parallel subagents per slice (format, lint, mypy, import-linter, test) — then merge and run `make flct`.

## 6. Report

- CI: what failed, what was fixed
- Comments: addressed vs deferred
- Merge state: ready or blocking items

## Rules

- No force-push to shared branches
- Do not delete tests to go green
- After boundary changes in PR → confirm `make lint-imports` passes
