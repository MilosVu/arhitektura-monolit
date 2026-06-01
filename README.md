# Cortex AI — Modular Monolith

Single-repo backend: **FastAPI** (`cortex-server`) + **two Celery workers** (`sync-worker`, `ingestion-worker`) + **React** frontend (`web-client`). Seven domain modules with strict import boundaries.

## Documentation

| Audience | Start here |
|----------|------------|
| **Everyone** | [docs/README.md](docs/README.md) |
| **Developers** | [docs/engineering/README.md](docs/engineering/README.md) |
| **Cursor / AI setup** | [docs/engineering/how-we-work/cursor-for-the-team.md](docs/engineering/how-we-work/cursor-for-the-team.md) |
| **PM / product** | [docs/product/README.md](docs/product/README.md) |
| **Architecture decisions (ADR)** | [docs/engineering/decisions/README.md](docs/engineering/decisions/README.md) |
| **AI assistants** | [AGENTS.md](AGENTS.md) |

## Architecture (high level)

```
web-client → cortex-server → module-platform / documents / chat / sync / ai
                                ↓
                             RabbitMQ → sync-worker (module-dms-sync)
                                      → ingestion-worker (module-ingestion)
```

Details: [docs/engineering/architecture/overview.md](docs/engineering/architecture/overview.md)

## Quick start

```bash
make infra-up
make install
make dev
```

- App: **http://localhost:5174**
- API: **http://localhost:8000**
- Flower: **http://localhost:5555**
- MVP login: `hmueller` / `mock`

## Local services

| Service | Port | Role |
|---------|------|------|
| web-client | 5174 | React frontend (Vite) |
| cortex-server | 8000 | API composition root |
| sync-worker | — | Celery queue `sync` |
| ingestion-worker | — | Celery queue `ingestion` |
| Flower | 5555 | Celery monitoring |

## Quality gate (before every PR)

```bash
make lint-imports   # after module boundary changes
make flct           # format + lint + mypy + import-linter + test
```

## Cursor (AI-assisted development)

This repo ships **Cursor rules, skills, and slash commands** in `.cursor/`. Open **this folder as the workspace root** in Cursor.

**New chat or big feature → type `/onboard` first.**

Team guide: [cursor-for-the-team.md](docs/engineering/how-we-work/cursor-for-the-team.md)

## Kubernetes (optional)

Namespace: **`cortex-monolith`**

```bash
make minikube-start
make k8s-build
make k8s-deploy
make k8s-url
```

Pods: `cortex-server`, `sync-worker`, `ingestion-worker`, `web-client`, infra (postgres, redis, rabbitmq, weaviate, neo4j), flower.
