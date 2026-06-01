---
name: update-documentation
description: >-
  Refresh docs from git changes since the last documentation commit — analyze code/config
  diffs, update stale engineering docs, verify and fix links, add ADRs. Invoke via /update-docs.
disable-model-invocation: true
---

# Update Documentation (Cortex monolith)

Sync **engineering documentation** with what changed in the repo since docs were last updated — then **verify all links**. One workflow: refresh content + link hygiene.

## Scope

**Update (when stale):**

- `docs/engineering/**`
- `docs/README.md`
- `README.md`, `AGENTS.md`
- `.cursor/rules/README.md`, `.cursor/skills/README.md` (indexes only — not rule bodies unless conventions changed)
- `apps/web-client/ONBOARDING.md` (frontend-facing dev doc)

**Do not fill with implementation detail:**

- `docs/product/` — PM/user-facing only; update only if user-visible behavior changed

**Do not auto-edit without noting:**

- `docs/engineering/decisions/*.md` — add **new ADR** for architectural changes; do not rewrite accepted ADRs

## Phase 1 — Find the baseline

Determine **since when** to analyze. Use the first method that works:

### A. Last documentation commit (default)

```bash
git log -1 --format="%H %ci %s" -- docs/ README.md AGENTS.md .cursor/rules/ .cursor/skills/README.md apps/web-client/ONBOARDING.md
```

Record `BASE_SHA` = that commit hash. If no commits touch these paths, use repo root or ask the user for a baseline.

### B. User override

User may say: "since commit X", "since last week", "since tag v0.2", "this branch vs main":

```bash
git log --oneline main..HEAD
git diff main...HEAD --stat
```

### C. Uncommitted work

Include working tree if user wants docs for **current session**:

```bash
git status --short
git diff --stat
git diff --cached --stat
```

### D. Links only (no content refresh)

User may say `/update-docs links only` — skip phases 2–4; run **Phase 5** on full doc scope.

User may say `/update-docs plan only` — run phases 1–3 only; post plan, no edits.

## Phase 2 — Analyze changes (read-only first)

List everything since `BASE_SHA` that is **not** already doc-only churn:

```bash
git log --oneline ${BASE_SHA}..HEAD
git diff ${BASE_SHA}..HEAD --stat -- . ':(exclude)docs/product'
git diff ${BASE_SHA}..HEAD --name-only -- packages/ apps/ libs/ infra/ Makefile pyproject.toml alembic/ .github/ .cursor/
```

Classify each changed path:

| Change pattern | Likely doc impact |
|----------------|-------------------|
| New/moved `packages/module-*`, routes, `api.py` | [feature-placement.md](../../../docs/engineering/how-we-work/feature-placement.md), [first-feature.md](../../../docs/engineering/how-we-work/first-feature.md), [module-boundaries.md](../../../docs/engineering/architecture/module-boundaries.md) |
| `pyproject.toml` import-linter contracts | [module-boundaries.md](../../../docs/engineering/architecture/module-boundaries.md) |
| `Document.status` / lifecycle / worker tasks | [documents-lifecycle](../../rules/documents-lifecycle.mdc), ADR 0002, [architecture-ready.md](../../../docs/engineering/architecture/architecture-ready.md) checklist |
| Celery tasks, new worker, queue names | [celery-workers](../../rules/celery-workers.mdc), ADR 0004/0006, [overview.md](../../../docs/engineering/architecture/overview.md) |
| `apps/cortex-server/main.py` routers | [overview.md](../../../docs/engineering/architecture/overview.md), [repository-structure.md](../../../docs/engineering/how-we-work/repository-structure.md) |
| Makefile, `scripts/`, ports | [local-development.md](../../../docs/engineering/how-we-work/local-development.md), root [README.md](../../../README.md) |
| Auth / SSO routes | [auth.md](../../../docs/engineering/how-we-work/auth.md) |
| `apps/web-client/**` | [ONBOARDING.md](../../../apps/web-client/ONBOARDING.md), [frontend-dev-starter](../frontend-dev-starter/SKILL.md) |
| `.cursor/rules/**` new/changed | [cursor-for-the-team.md](../../../docs/engineering/how-we-work/cursor-for-the-team.md) |
| `.cursor/skills/**` or `commands/**` | [cursor-for-the-team.md](../../../docs/engineering/how-we-work/cursor-for-the-team.md), [skills/README.md](../README.md) |
| `infra/k8s/`, Docker | root README K8s section, [overview.md](../../../docs/engineering/architecture/overview.md) |
| Alembic migrations | [local-development.md](../../../docs/engineering/how-we-work/local-development.md) (`make db-setup`) |
| New lib in `libs/` | [repository-structure.md](../../../docs/engineering/how-we-work/repository-structure.md), [overview.md](../../../docs/engineering/architecture/overview.md) |

**Architectural decision?** If changes alter module boundaries, lifecycle, deploy topology, or auth model → draft new ADR from [template.md](../../../docs/engineering/decisions/template.md) and index in [decisions/README.md](../../../docs/engineering/decisions/README.md).

## Phase 3 — Report before large edits

Post a short plan **before** editing many files:

```markdown
## Doc refresh plan

**Baseline:** <SHA> (<date>) — "<message>"
**Commits since:** N
**Code areas touched:** …

| Doc file | Action | Reason |
|----------|--------|--------|
| docs/engineering/... | UPDATE | new module-x routes |
| decisions/ | NEW ADR 0009 | … |

Proceed? (Agent continues unless user objects.)
```

For `/update-docs` invocation, **proceed automatically** unless the user said **`/update-docs plan only`**.

## Phase 4 — Update docs

Rules while editing:

1. **English only** in engineering docs
2. **Match existing tone** — read the file first; minimal diff
3. **No duplicate** — link to ADR or existing page instead of copying architecture essays
4. **Product vs engineering** — API task names and module paths stay in `engineering/` only
5. Update **indexes** when adding pages (engineering README, docs README)
6. Do **not** delete history from [refactor-plan.md](../../../docs/engineering/decisions/history/refactor-plan.md) — append checklist notes if needed
7. Keep `.mdc` rules short; put long prose in `docs/engineering/`
8. When moving/renaming doc files, fix **incoming links** in the same pass (Phase 5 catches stragglers)

## Phase 5 — Verify and fix links (always)

Run after Phase 4, or alone with `links only`. Focus on **repo-local paths**; external URLs are optional.

### Scope

Default scan:

```
docs/**/*.md
.cursor/**/*.md
.cursor/**/*.mdc
README.md
AGENTS.md
apps/web-client/ONBOARDING.md
libs/cortex-core/ARCHITECTURE-LAYERS.md
```

After a content refresh, **at minimum** scan all files touched in Phase 4 plus the default scope.

### Extract links

From each file: `[text](path)`, reference-style `[id]: path`. Ignore `http://localhost:*`, `#anchors`, and illustrative code-only paths.

### Test local paths

Resolve relative to the **source file's directory**; confirm file or directory exists.

Also grep for stale patterns:

```bash
grep -rE 'gde-sta-ide|prvi-feature|uporedba|docs/onboarding/|MODULE-BOUNDARIES|0001-modularni' docs/ .cursor/ README.md AGENTS.md || true
```

Watch for wrong relative depth from `.cursor/rules/` (`../../docs/` not `../docs/`).

### Test external URLs (optional)

```bash
curl -sL -o /dev/null -w "%{http_code}" --max-time 10 "<url>"
```

403/429 → note as "blocked to curl", not necessarily broken.

### Fix

| Problem | Action |
|---------|--------|
| Renamed/moved file | Update link target |
| Dead onboarding / Serbian filenames | Point to current English paths |
| Wrong `../` depth | Fix relative path |
| Missing `.mdc` / doc file | Create file or retarget link |
| External URL 404 | Update URL, remove link, or note for human review |

Do not delete product doc content without approval.

### Link report (include in Phase 6 summary)

```markdown
### Links
| File | Link | Action |
|------|------|--------|
| … | … | fixed → … |

Checked: N | Broken: X | Fixed: Y | Needs review: Z
```

## Phase 6 — Summary for the user

```markdown
## Documentation refresh complete

**Since:** <BASE_SHA> (<date>)
**Commits analyzed:** N

### Updated files
- …

### Links
- Checked N, fixed Y, …

### New ADRs
- … (or "none")

### Intentionally not changed
- docs/product/ — no user-visible change

### Suggested follow-ups
- Team review ADR 0009
- Run `/onboard` in next chat if boundaries changed
```

## When to run

- End of sprint / before release
- After a large PR merged (multi-module)
- When docs feel stale or after doc moves/renames
- After adding skills, rules, or Makefile targets

## When not to run

- Typo-only code fix with no behavioral change — skip full refresh; `links only` is still OK if you edited docs

## Related

- [suggesting-cursor-rules](../suggesting-cursor-rules/SKILL.md) — if gaps repeat, add a rule
- New ADR: [decisions/template.md](../../../docs/engineering/decisions/template.md)
