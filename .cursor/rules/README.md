# Cursor Rules — Cortex Modular Monolith

Operative rules for AI assistants (Cursor) working in **this repository**.

**Location:** `.cursor/rules/` at the repo root. Open Cursor with this folder as the workspace root — otherwise these rules will not load.

Long-form documentation lives in [`docs/engineering/`](../docs/engineering/README.md). Rules are short, actionable invariants; docs explain the why.

## How rules are tiered

| Tier | When it applies | Purpose |
|------|-----------------|---------|
| **1 — Always on** | Every chat session | Language, repo map, feature placement |
| **2 — Cross-cutting** | Matching Python/config globs | Boundaries, structure, FastAPI, Celery, tooling |
| **3 — Domain** | Module-specific globs | Documents lifecycle, AI agents, frontend |

Tier 1 rules have `alwaysApply: true`. Tier 2 and 3 activate when you edit files matching their `globs` pattern.

## Rule index

| File | Scope |
|------|-------|
| [english-only.mdc](english-only.mdc) | English for new code, comments, rules, commits, PR text |
| [monolith-overview.mdc](monolith-overview.mdc) | Repo map, golden rules, doc links |
| [feature-placement.mdc](feature-placement.mdc) | Which module owns a feature — read before coding |
| [module-boundaries.mdc](module-boundaries.mdc) | Import-linter contracts, allowed dependencies |
| [python-package-structure.mdc](python-package-structure.mdc) | Folder layout, naming conventions |
| [hexagonal-modules.mdc](hexagonal-modules.mdc) | Ports / adapters / services layering |
| [ports-adapters.mdc](ports-adapters.mdc) | `cortex-core` ports, `cortex-connectors` adapters |
| [fastapi-routes-facades.mdc](fastapi-routes-facades.mdc) | Thin routes, facades, FastAPI deps |
| [celery-workers.mdc](celery-workers.mdc) | Sync / ingestion workers, task chains |
| [quality-tooling.mdc](quality-tooling.mdc) | Makefile, uv workspace, import-linter, `make flct` |
| [documents-lifecycle.mdc](documents-lifecycle.mdc) | `Document.status` — only `DocumentsModule.mark_*` |
| [ai-agents.mdc](ai-agents.mdc) | LangGraph agents, RAG, facade-only access |
| [frontend-web-client.mdc](frontend-web-client.mdc) | React / Vite conventions |

## Quick start for AI assistants

1. Read [monolith-overview.mdc](monolith-overview.mdc) and [feature-placement.mdc](feature-placement.mdc).
2. Before a cross-module change → [module-boundaries.mdc](module-boundaries.mdc).
3. After changing import boundaries → run `make lint-imports`.
4. Before merge → `make flct` (or `/flct` in chat)

## Skills and slash commands

Project skills: [skills/README.md](../skills/README.md)

| Command | When |
|---------|------|
| `/onboard` | Start of new chat or cross-module work |
| `/flct` | Loop until quality gate passes |
| `/api-smoke` | After HTTP route changes |
| `/babysit-pr` | Open PR needs attention |

## Adding or changing a rule

1. Edit or add a `.mdc` file in this folder.
2. Use YAML frontmatter: `description`, `alwaysApply` or `globs`.
3. Keep rules short — link to `docs/engineering/` for detail.
4. Update this index if you add a new file.

## Related

| Doc | Purpose |
|-----|---------|
| [AGENTS.md](../AGENTS.md) | Agent entry point (commands, invariants) |
| [docs/engineering/README.md](../docs/engineering/README.md) | Developer onboarding |
| [docs/engineering/decisions/README.md](../docs/engineering/decisions/README.md) | ADRs — architectural decisions |
