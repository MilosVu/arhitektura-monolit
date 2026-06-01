# Frontend — smeštaj u monolitu

React aplikacija živi u **`apps/web-client/`** (Vite + TypeScript).

## Gde dodati kod

| Šta | Folder |
|-----|--------|
| Novi ekran | `src/pages/` |
| Deljeni UI | `src/components/` |
| API pozivi / tipovi | `src/api/client.ts`, `src/api/types.ts` |
| Auth state (token, user) | `src/context/AuthContext.tsx` |
| Rute | `src/App.tsx` |

## Auth flow (cilj)

1. Korisnik na login → redirect na **AD SSO** (ne lokalna lozinka u produkciji).
2. Callback sa tokenom → backend `module-platform` validacija.
3. Frontend čuva JWT i šalje `Authorization: Bearer` na API.

MVP: `LoginPage` + mock credentials — zameniti AD redirect kada backend SSO bude spreman.

## Lokalno

```bash
# iz root monolita
make dev-web
# ili ceo stack
make dev
```

Port: **5174** (da ne konflikuje sa mikroservisnim UI na 5173).

Backend dokumentacija: [docs/engineering/README.md](../../docs/engineering/README.md).
