# Cursor Skills — Cortex Modular Monolith

Project skills in `.cursor/skills/`. Discovered automatically by the agent; slash commands in `.cursor/commands/` for explicit invocation.

**Rules vs skills:** `.cursor/rules/` = always-on or glob invariants. Skills = on-demand workflows.

## All skills

| Skill | Slash command | When to use |
|-------|---------------|-------------|
| [cortex-onboard](cortex-onboard/SKILL.md) | `/onboard` | **Start of a new chat** or before a cross-module feature |
| [python-tdd-with-uv](python-tdd-with-uv/SKILL.md) | — | New backend logic, services, tests |
| [grinding-until-pass](grinding-until-pass/SKILL.md) | `/flct` | After refactor — loop until `make flct` passes |
| [parallel-exploring](parallel-exploring/SKILL.md) | — | "Where is X?" across modules |
| [api-smoke-testing](api-smoke-testing/SKILL.md) | `/api-smoke` | After HTTP route changes |
| [verifying-in-browser](verifying-in-browser/SKILL.md) | — | After UI or API-proxy changes |
| [babysitting-pr](babysitting-pr/SKILL.md) | `/babysit-pr` | Open PR needs CI / review fixes |
| [code-review](code-review/SKILL.md) | `/code-review` | **Before commit** — architecture + security + tests |
| [systematic-debugging](systematic-debugging/SKILL.md) | — | Sync/ingestion/Celery chain stuck or wrong |
| [update-documentation](update-documentation/SKILL.md) | `/update-docs` | Refresh docs from git + verify/fix links |
| [suggesting-cursor-rules](suggesting-cursor-rules/SKILL.md) | — | Agent suggests new `.mdc` after repeated corrections |
| [frontend-dev-starter](frontend-dev-starter/SKILL.md) | — | Before or during `apps/web-client/` work |

## Recommended chat flow

```
New chat, big feature  →  /onboard  →  describe task
Backend feature        →  python-tdd-with-uv + make flct
Before commit          →  /code-review  →  fix blockers  →  /flct
Before merge           →  /flct
Open PR                →  /babysit-pr
Sync stuck / wrong status →  systematic-debugging
Docs refresh              →  /update-docs
UI change                →  frontend-dev-starter + verifying-in-browser
```

## Adding skills

1. Create `.cursor/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Add `disable-model-invocation: true` for slash-command-only skills
3. Update this README
4. Optional: add `.cursor/commands/<name>.md` for `/` menu

Adapted from [awesome-cursor-skills](https://github.com/...) — customized for this monolith.

## Related

- [Rules README](../rules/README.md)
- [AGENTS.md](../../AGENTS.md)
