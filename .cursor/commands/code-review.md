# Code review (pre-commit)

Follow `.cursor/skills/code-review/SKILL.md`.

Review local changes **before commit** — architecture, security, correctness, tests. Read-only report with verdict (OK / fix first / do not commit).

```bash
git status --short
git diff --stat
make lint-imports   # if module boundaries may have changed
make flct           # include results in report
```

Launch parallel read-only reviewers (architecture, security, correctness, tests). **Do not edit code** unless asked after the report.

**Staged only:** `/code-review staged`

**vs main:** `/code-review vs main`

After blockers fixed → `/code-review` again → `/flct` → commit.
