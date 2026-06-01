# Cursor Skills — Cortex Modular Monolith

Project skills in `.cursor/skills/`. Discovered automatically by the agent; slash commands in `.cursor/commands/` for explicit invocation.

**Rules vs skills:** `.cursor/rules/` = always-on or glob invariants. Skills = on-demand workflows.

## Starter pack (installed)

| Skill | Slash command | When to use |
|-------|---------------|-------------|
| [cortex-onboard](cortex-onboard/SKILL.md) | `/onboard` | **Start of a new chat** or before a cross-module feature |
| [python-tdd-with-uv](python-tdd-with-uv/SKILL.md) | — | New backend logic, services, tests |
| [grinding-until-pass](grinding-until-pass/SKILL.md) | `/flct` | After refactor — loop until `make flct` passes |
| [parallel-exploring](parallel-exploring/SKILL.md) | — | "Where is X?" across modules |
| [api-smoke-testing](api-smoke-testing/SKILL.md) | `/api-smoke` | After HTTP route changes |
| [verifying-in-browser](verifying-in-browser/SKILL.md) | — | After UI or API-proxy changes |
| [babysitting-pr](babysitting-pr/SKILL.md) | `/babysit-pr` | Open PR needs CI / review fixes |
| [frontend-dev-starter](frontend-dev-starter/SKILL.md) | — | Before or during `apps/web-client/` work |

## Recommended chat flow

```
New chat, big feature  →  /onboard  →  describe task
Backend feature        →  python-tdd-with-uv + make flct
Before merge           →  /flct
Open PR                →  /babysit-pr
UI change              →  frontend-dev-starter + verifying-in-browser
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
