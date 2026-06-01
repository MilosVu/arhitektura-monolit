# Frontend — placement in the monolith

React app lives in **`apps/web-client/`** (Vite + TypeScript + pnpm).

## Where to add code

| What | Folder |
|------|--------|
| New screen | `src/pages/` |
| Shared UI | `src/components/` |
| API calls / types | `src/api/client.ts`, `src/api/types.ts` |
| Auth state (token, user) | `src/context/AuthContext.tsx` |
| Routes | `src/App.tsx` |

## Auth flow (target)

1. User hits login → redirect to **AD SSO** (not local password in production).
2. Callback with token → backend `module-platform` validation.
3. Frontend stores JWT and sends `Authorization: Bearer` on API calls.

MVP: `LoginPage` + mock credentials — replace with AD redirect when backend SSO is ready.

## Local dev

```bash
make dev-web    # from repo root
make dev        # full stack
```

Port: **5174** (avoids conflict with microservices UI on 5173).

All API calls use `/api/*` (Vite proxy to `localhost:8000`) — never hardcode backend URL.

## Cursor

- Rule (auto on edit): `.cursor/rules/frontend-web-client.mdc`
- Skill: `.cursor/skills/frontend-dev-starter/SKILL.md`
- Verify UI: `.cursor/skills/verifying-in-browser/SKILL.md`

Backend docs: [docs/engineering/README.md](../../docs/engineering/README.md).
