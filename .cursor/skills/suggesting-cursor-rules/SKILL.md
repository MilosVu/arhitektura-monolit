---
name: suggesting-cursor-rules
description: >-
  When the user corrects the same convention 2+ times, suggest encoding it as a
  .cursor/rules/*.mdc file. Meta-skill for this monolith — check existing rules first.
---

# Suggesting Cursor Rules (Cortex monolith)

Watch for **repeated corrections**. Offer to encode the convention in `.cursor/rules/` so it applies automatically.

## Triggers

Suggest a rule when:

- User corrects the **same pattern 2+ times** in one or across chats
- User says "always", "never", "every time you…"
- Agent repeats a mistake that **existing rules already forbid** → remind about existing rule first, don't duplicate
- Team hits the same code review comment repeatedly

**Do not suggest** on the first correction — wait for a pattern.

## Before creating — check existing rules

Read [.cursor/rules/README.md](../../rules/README.md). Common topics **already covered**:

| Topic | Existing rule |
|-------|---------------|
| Module placement | `feature-placement.mdc` |
| Import boundaries | `module-boundaries.mdc` |
| Document.status | `documents-lifecycle.mdc` |
| Celery tasks | `celery-workers.mdc` |
| English | `english-only.mdc` |
| FastAPI routes | `fastapi-routes-facades.mdc` |
| Frontend | `frontend-web-client.mdc` |

If the convention fits an existing file → **propose an edit** to that `.mdc`, not a new file.

## How to offer

```
I notice you've corrected [pattern] a couple of times. Want me to add this to
.cursor/rules/ (or extend [existing-rule].mdc) so it's always applied?
```

Wait for yes before writing.

## New rule template

Path: `.cursor/rules/<short-name>.mdc`

```markdown
---
description: <one line — when this applies>
globs: packages/**/*.py    # omit alwaysApply; use globs OR alwaysApply: true
alwaysApply: false
---

# <Title>

## Invariant

<One clear rule>

## STOP list

- <anti-pattern> → **STOP** → <correct approach>

## Deep dive

`docs/engineering/...`
```

**Guidelines:**

- One concern per file
- Keep under ~60 lines — link to `docs/engineering/` for detail
- Use `globs` for file-specific rules; `alwaysApply: true` only for universal invariants (rare — tier 1 is already crowded)
- Update [.cursor/rules/README.md](../../rules/README.md) index
- If module boundaries change → also update `docs/engineering/architecture/module-boundaries.md` and `pyproject.toml` import-linter

## Cortex-specific examples

**User keeps saying "don't import agents directly":**

→ Extend `module-boundaries.mdc` or `ai-agents.mdc`, not a duplicate.

**User wants a new frontend convention (e.g. loading states on every fetch):**

→ New `frontend-components.mdc` with `globs: apps/web-client/src/**/*.tsx`

**User wants "always run lint-imports after api.py change":**

→ Already in `quality-tooling.mdc` — remind team, don't duplicate.

## After creating

1. Mention in [cursor-for-the-team.md](../../../docs/engineering/how-we-work/cursor-for-the-team.md) only if tier-1/2 behavior changed materially
2. Optional ADR if the rule reflects an architectural decision
3. `make flct` if any Python tooling config changed (unlikely for `.mdc` only)

## Rules

- Frame as helpful offer, not lecture
- Never weaken lifecycle or import-linter rules to match bad habits
- Prefer editing docs + existing rules over proliferating many small `.mdc` files
