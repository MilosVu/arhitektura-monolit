---
name: grinding-until-pass
description: >-
  Iterate fix → run → check until make flct passes (format, lint, mypy, import-linter,
  tests). Use after refactors, dependency upgrades, or when the user says "make it green".
---

# Grind Until Pass (Cortex monolith)

Autonomously loop until the quality gate passes.

## Goal command

**Primary (full gate):**

```bash
make flct
```

Equivalent step-by-step if you need faster iteration:

```bash
uv run poe ci:format    # ruff format
uv run poe ci:lint      # ruff check
uv run poe check        # mypy
uv run poe lint-imports # module boundaries — CRITICAL after api.py / import changes
uv run poe test         # pytest
```

For import-only changes, run `make lint-imports` first — it fails fast.

## Loop

1. Run `make flct` (or the failing sub-command)
2. Read the **first** error in output
3. Apply the **minimal** fix — no drive-by refactors
4. Re-run from step 1
5. Stop when exit code 0

## Rules

- **Max 10 iterations** — then stop and report blockers for human input
- **Fix one error at a time** — first failure often cascades
- **Do not delete tests** to go green — fix code or fix wrong test expectations
- **Do not suppress** — no `# type: ignore`, `noqa`, or weakening import-linter contracts without reason
- **Document.status** — if tests touch workers, use `DocumentsModule` facade mocks, not direct ORM status writes
- If errors **increase** after a fix, revert approach and reassess

## Common failures in this repo

| Failure | Likely fix |
|---------|------------|
| import-linter | cross-module import → use `module_*/api.py` facade |
| mypy strict | add types, fix Optional, use Pydantic models |
| ruff I001 | run formatter or fix import order |
| pytest | read assertion; check TestClient fixtures |

## When done

Report: iterations count, what was fixed, confirm `make flct` exit 0.
