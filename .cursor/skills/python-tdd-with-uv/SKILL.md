---
name: python-tdd-with-uv
description: >-
  Test-driven development in this monolith using uv and pytest. Red-green-refactor
  with vertical slicing. Use when adding backend logic, services, facades, or worker
  behavior in packages/ or libs/.
---

# Python TDD with uv (Cortex monolith)

This repo is a **uv workspace**. Tests already use pytest — extend them, do not reinvent setup.

## Commands

```bash
uv sync --all-packages
uv run pytest                          # all tests
uv run pytest apps/cortex-server/tests # server only
uv run pytest packages/module-documents/tests -v
uv run pytest -k "test_health" -x      # one test, stop on fail
make flct                              # format + lint + mypy + import-linter + test
```

Always use `uv run` — never manual venv activation.

## Where tests live

| Code | Test location |
|------|---------------|
| `apps/cortex-server/` | `apps/cortex-server/tests/` |
| `packages/module-*/` | `packages/module-*/tests/` |
| `libs/cortex-*/` | `libs/cortex-*/tests/` |

Place tests next to the package they cover. Do not add a single global `tests/` at repo root unless the team agrees.

## TDD cycle

```
RED    → one failing test for the next behavior
GREEN  → minimum code to pass
REFACTOR → clean up; re-run pytest + mypy
REPEAT
```

**Rules:**

- One failing test at a time
- Assert **observable behavior**, not private implementation
- Mock only at boundaries: DB, Redis, Alfresco, Weaviate, Celery broker, LLM
- For HTTP: use FastAPI `TestClient` fixture pattern from `apps/cortex-server/tests/`
- For facades: prefer fake repositories / stub ports over mocking entire modules
- Never bypass `DocumentsModule.mark_*` in worker tests — test lifecycle via facade

## Module boundary tests

After adding cross-module calls:

```bash
make lint-imports
```

Import-linter is part of `make flct` — run it when tests touch `api.py` or new imports.

## Adding dependencies

```bash
uv add --package module-documents httpx   # example: per-package dep
uv add --dev pytest-mock                  # workspace dev dep
```

Commit `pyproject.toml` and `uv.lock` changes.

## References

- `docs/engineering/how-we-work/first-feature.md` — endpoint walkthrough
- `.cursor/rules/quality-tooling.mdc` — full CI checklist
