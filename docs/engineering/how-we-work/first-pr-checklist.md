# Checklist — First PR / Every PR

## Before opening a PR

- [ ] Feature is in the **correct module** ([feature-placement.md](feature-placement.md))
- [ ] New code follows [hexagonal-layout.md](hexagonal-layout.md) where applicable
- [ ] Cross-module only via `module_*/api.py`
- [ ] `Document.status` only via `DocumentsModule.mark_*` (if touching documents)
- [ ] Celery task names from `cortex_core.messaging.tasks`

## Commands (repo root)

```bash
make lint-imports
make flct    # format + lint + mypy + import-linter + test (same as CI)
```

## Include in the PR description

- Which module / use-case
- Whether module boundaries changed (import-linter)
- Whether API changed (breaking change)
- How to test manually (step 1–2–3)

## Red flags for review

- Business logic in `apps/cortex-server/main.py`
- Import `module_*.services` or `module_*.agents` from another module
- Direct ORM write on `Document.status` in a worker
- New hardcoded Celery task string
