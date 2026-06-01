---
name: verifying-in-browser
description: >-
  Start make dev (or web-client), open http://localhost:5174, verify UI rendering,
  console errors, and API proxy health. Use after frontend or API changes affecting the UI.
---

# Verify in Browser (Cortex web-client)

## Stack facts

- Frontend: `apps/web-client/` — React + Vite + TypeScript + **pnpm**
- Dev URL: **http://localhost:5174** (not 5173)
- API proxy: `/api/*` → `http://localhost:8000` (see `vite.config.ts`)
- MVP login: `hmueller` / `mock`

## Steps

1. **Check if dev server is running** — list terminals. If not:

   ```bash
   make dev-web    # frontend only
   # or full stack:
   make dev
   ```

2. **Open browser** (Cursor built-in browser if available):

   - URL: `http://localhost:5174`
   - Login page → mock credentials → cases list

3. **Health checks**

   - **Console** — no uncaught errors (warnings OK)
   - **Network** — `/api/*` requests should not be 502/503 (backend down)
   - **Visual** — page renders, no infinite spinner

4. **Test changed flows**

   | Flow | What to verify |
   |------|----------------|
   | Login | JWT stored, redirect to cases |
   | Cases | list loads from `/api/cases` |
   | Documents | list per case |
   | Sync | trigger + job polling |
   | Chat | thread + stream |
   | RAG | search returns results |

5. **Report**

   - Pass: "Verified — 5174 renders, no console errors, API proxy healthy"
   - Fail: list errors with network status codes and console messages

## If backend is down

Frontend may load but API calls fail. Start full stack:

```bash
make infra-up && make dev
```

## Before frontend work starts

Read `.cursor/skills/frontend-dev-starter/SKILL.md` and `.cursor/rules/frontend-web-client.mdc`.

## Notes

- Never hardcode `http://localhost:8000` in components — use `/api/...` paths
- After backend route changes, update `apps/web-client/src/api/client.ts` if paths broke
