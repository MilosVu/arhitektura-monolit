# Cursor — guide for the team

How we use **Cursor** (AI-assisted coding) in this repository. You do not need to memorize everything — this page is the cheat sheet.

## One-time setup

1. **Clone this repo** and open **`arhitektura-monolit/`** as the **workspace root** in Cursor.  
   If you open a parent folder, `.cursor/rules/` will not load correctly.

2. **Pull latest** — `.cursor/` is in git. Everyone gets the same rules and skills.

3. **Install the stack** (once per machine):

   ```bash
   make infra-up && make install
   ```

That is it. No extra Cursor plugins required for day-to-day work.

---

## What lives in `.cursor/`

| Folder | What it is | Who reads it |
|--------|------------|--------------|
| [`.cursor/rules/`](../../../.cursor/rules/README.md) | Short **always-on or file-specific conventions** | Cursor injects automatically |
| [`.cursor/skills/`](../../../.cursor/skills/README.md) | **Step-by-step workflows** (TDD, PR babysit, browser check) | Agent when relevant, or you trigger via chat |
| [`.cursor/commands/`](../../../.cursor/commands/) | **Slash commands** you type in chat (`/onboard`, …) | You |

**Rules** = laws (module boundaries, English-only, document lifecycle).  
**Skills** = playbooks (how to run tests, explore the repo, fix CI).  
**Commands** = shortcuts to start a playbook.

Long explanations stay in [`docs/engineering/`](../README.md) and [ADRs](../decisions/README.md). Rules stay short on purpose.

---

## Three layers (mental model)

```
┌─────────────────────────────────────────┐
│  Rules (.cursor/rules/)                 │  ← automatic, every chat / matching files
├─────────────────────────────────────────┤
│  Skills + commands (.cursor/skills/)    │  ← on demand (/onboard, TDD, …)
├─────────────────────────────────────────┤
│  Docs (docs/engineering/) + AGENTS.md   │  ← deep context, architecture, ADRs
└─────────────────────────────────────────┘
```

You write normal code. Cursor follows the rules. You invoke commands when you want extra context or a workflow.

---

## Slash commands (type in chat)

| Command | When to use |
|---------|-------------|
| **`/onboard`** | **Start of a new chat** or before a cross-module feature. Agent reads core docs and summarizes the repo — no coding until you describe the task. |
| **`/flct`** | After changes — agent loops until `make flct` passes (format, lint, mypy, import-linter, tests). |
| **`/api-smoke`** | After adding or changing HTTP routes — hit endpoints, report 404/500. |
| **`/babysit-pr`** | Open PR with failing CI or review comments — agent tries to fix and re-check. |

### Typical flows

**Small fix** (typo, one file):

→ Describe the task. Rules already apply. Run `make flct` before push.

**New backend feature**:

1. `/onboard`
2. Describe the feature (“add endpoint X in module-documents”)
3. Agent should check [feature-placement.md](feature-placement.md)
4. Before PR: `make flct` or `/flct`

**New frontend screen**:

1. `/onboard` (optional)
2. Read [frontend-dev-starter](../../../.cursor/skills/frontend-dev-starter/SKILL.md)
3. Edit under `apps/web-client/`
4. Ask agent to verify in browser (port **5174**)

**Open PR not green**:

→ `/babysit-pr`

---

## Rules that always apply (Tier 1)

You do not enable these — they are always on:

| Rule | Meaning |
|------|---------|
| `english-only` | New code, comments, commits in English |
| `monolith-overview` | Repo map, golden rules, doc links |
| `feature-placement` | Which module owns a feature — **read before coding** |

---

## Rules that apply when you edit matching files (Tier 2 & 3)

Examples:

| You edit… | Extra rules activate |
|-----------|----------------------|
| `packages/**/*.py`, `libs/**/*.py` | module boundaries, package structure, hexagonal layout |
| `**/routes/**`, `**/api.py` | FastAPI facades — thin routes only |
| `**/tasks.py`, worker apps | Celery workers, task constants |
| `module_documents/**`, dms-sync, ingestion | **Document.status** only via `DocumentsModule.mark_*` |
| `module_ai/**` | AI agents — facade only, SearchPort read |
| `apps/web-client/**` | React — `/api/*` proxy, port 5174 |

Full index: [.cursor/rules/README.md](../../../.cursor/rules/README.md)

---

## Skills (no slash — mention in chat or auto)

| Skill | Say something like… |
|-------|---------------------|
| `python-tdd-with-uv` | “Add this test-first with uv/pytest” |
| `parallel-exploring` | “Where is sync triggered?” / “Map the ingestion flow” |
| `grinding-until-pass` | Same as `/flct` |
| `verifying-in-browser` | “Check the UI on 5174 after this change” |
| `frontend-dev-starter` | “I'm starting work on web-client” |

Index: [.cursor/skills/README.md](../../../.cursor/skills/README.md)

---

## Six invariants (human + AI)

Memorize these — they appear in rules, docs, and code review:

1. **Thin app shell** — no domain logic in `apps/*/main.py`
2. **Facade only** — cross-module via `module_*/api.py`
3. **`Document.status`** — only `DocumentsModule.mark_*()` in `module-documents`
4. **Celery** — task names from `cortex_core.messaging.tasks` (no hardcoded strings)
5. **After boundary changes** — `make lint-imports`
6. **ORM** — only `libs/cortex-models`

---

## Makefile commands (every developer)

```bash
make dev            # full local stack
make lint-imports   # after import / module boundary changes
make flct           # full quality gate — run before every PR
make db-setup       # alembic upgrade head
```

---

## FAQ

**Do I need `/onboard` every time?**  
No. Use it for new chats, unfamiliar areas, or cross-module work. Small edits → just ask.

**Can I edit `.cursor/rules/`?**  
Yes — treat like code. Update the README index, open a PR, `make flct`. Big convention changes → add an ADR.

**Does this work in VS Code without Cursor?**  
Rules/skills are Cursor-specific. Humans still use `docs/engineering/` and `make flct` the same way.

**Where is the AI entry point?**  
[AGENTS.md](../../../AGENTS.md) — short summary for agents; this page is for humans.

---

## Related

- [Developer onboarding](../README.md) — architecture reading list
- [first-pr-checklist.md](first-pr-checklist.md) — before merge
- [feature-placement.md](feature-placement.md) — where code goes
