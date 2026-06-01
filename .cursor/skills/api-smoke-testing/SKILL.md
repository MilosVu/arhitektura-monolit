---
name: api-smoke-testing
description: >-
  Discover FastAPI routes in cortex-server, hit endpoints with curl/TestClient, and report
  health vs auth-required vs real errors. Use after route changes or before release.
disable-model-invocation: true
---

# API Smoke Testing (Cortex monolith)

Verify HTTP surface is mounted and responds sensibly.

## 1. Discover routes

Search:

- `packages/module_*/module_*/routes/**/*.py` — `@router.get`, `@router.post`, etc.
- `apps/cortex-server/cortex_server/main.py` — `include_router` list

Build a table: method, path, module, auth required (yes/no).

Known routers: platform, documents, chat, sync, ai.

## 2. Server running

```bash
make dev          # full stack
# or API only:
uv run uvicorn cortex_server.main:app --reload --port 8000
```

Check `http://localhost:8000/health` — expect `{"status":"ok","service":"cortex-server"}`.

## 3. Auth for protected routes

MVP mock login:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"hmueller","password":"mock"}' | jq -r '.access_token')
```

Use `-H "Authorization: Bearer $TOKEN"` for protected endpoints.

## 4. Hit endpoints

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/cases
```

For POST/PATCH, send minimal valid JSON from Pydantic schemas in `module_*/schemas/`.

## 5. Classify

| Status | Meaning |
|--------|---------|
| 200–299 | OK |
| 401/403 | Auth required or forbidden — expected if no/ wrong token |
| 404 | Route not mounted — **bug** if defined in code |
| 422 | Validation — expected for empty invalid body |
| 500 | Server error — **bug**; read uvicorn logs |

## 6. Prefer pytest for regression

Add or extend tests in `apps/cortex-server/tests/` using the existing `client` fixture:

```python
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
```

Run: `uv run pytest apps/cortex-server/tests -v`

## 7. Report

```
API Smoke Test:
  Tested: N endpoints
  OK: ...
  Auth required (expected): ...
  BUGS:
    500 POST /... — <summary>
    404 GET /... — router not mounted
```

Fix 500s from stack trace; fix 404s in `main.py` router wiring or route prefix.
