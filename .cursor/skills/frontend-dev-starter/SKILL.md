---
name: frontend-dev-starter
description: >-
  Starting point for web-client development — stack, folders, API proxy, auth flow,
  and rules to add when frontend work begins. Use when editing apps/web-client/ or
  planning UI features.
---

# Frontend Dev Starter (Cortex web-client)

Use this when **starting or expanding** frontend work. Backend rules still apply — UI calls modules via HTTP only.

## Read first

1. `.cursor/rules/frontend-web-client.mdc` (auto-applies on `apps/web-client/**`)
2. `apps/web-client/ONBOARDING.md`
3. `docs/engineering/how-we-work/auth.md` — AD/SSO target vs mock MVP

## Stack

| Piece | Choice |
|-------|--------|
| Framework | React 18+ functional components |
| Build | Vite |
| Package manager | **pnpm** (from `apps/web-client/`) |
| Language | TypeScript strict |
| Styling | *(team decision pending — document in ADR when chosen)* |
| State | React Context for auth; no Redux until needed |
| API | `src/api/client.ts` — all calls via `/api/*` proxy |

## Folder map

```
apps/web-client/src/
├── pages/          # route-level screens
├── components/     # shared UI
├── api/            # client.ts, types.ts — mirror backend DTOs
├── context/        # AuthContext
└── App.tsx         # routes
```

## Invariants

1. **No hardcoded backend URL** — `/api/...` only (Vite proxy)
2. **Port 5174** for monolith dev
3. **JWT** in `Authorization: Bearer` header after login
4. When backend route moves modules, update `client.ts` + types — check owning module in `feature-placement.mdc`
5. English UI copy for new strings (product localization later in `docs/product/`)

## Dev commands

```bash
make dev-web              # from repo root
cd apps/web-client && pnpm dev   # direct
make dev                  # full stack (API + workers + UI)
```

## Suggested rules to add when frontend ramps up

When the team starts serious UI work, add **one rule or skill at a time** (do not bulk-add):

| Priority | Add | When |
|----------|-----|------|
| P0 | Keep `frontend-web-client.mdc` updated | Now — already exists |
| P1 | `verifying-in-browser` skill | After first UI feature PR |
| P2 | Component conventions rule (`.mdc`) | When 5+ shared components exist — naming, props, a11y |
| P2 | `network-request-auditing` pattern | When sync/chat/RAG flows are wired in UI |
| P3 | Playwright E2E skill | When MVP flows stable (login → case → sync → doc ready) |
| P3 | `responsive-testing` / `accessibility-auditing` | Before production UI |

## Component rule template (create when ready)

Save as `.cursor/rules/frontend-components.mdc` with globs `apps/web-client/src/components/**/*.tsx`:

- Props interface exported; no `any`
- Loading / error / empty states for every data fetch
- Accessible labels on forms (prep for AD login redirect flow)

## API type sync

When backend Pydantic schemas change:

1. Find schema in `packages/module-*/module_*/schemas/`
2. Update matching type in `apps/web-client/src/api/types.ts`
3. Run `verifying-in-browser` skill — login + affected page

## Do not

- Put business logic in components that belongs in backend modules
- Call Alfresco, Weaviate, or Redis from frontend
- Add document status logic in UI — display what API returns

## Deep dive

- Backend route map: `.cursor/rules/fastapi-routes-facades.mdc`
- Full stack local: `docs/engineering/how-we-work/local-development.md`
