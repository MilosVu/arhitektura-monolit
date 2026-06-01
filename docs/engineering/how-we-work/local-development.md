# Local Development

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Docker (for infra)
- Node/pnpm (for web-client — Makefile uses `npx pnpm`)

## First time

```bash
make infra-up      # Postgres, Redis, RabbitMQ, Weaviate, Neo4j
make install       # uv sync + web-client deps
make seed-neo4j    # optional, law graph
make lint-imports  # architectural boundaries
```

## Running

### Everything at once (recommended)

```bash
make dev
# or
./scripts/dev.sh
```

### Individually

```bash
make dev-server
make dev-sync-worker
make dev-ingestion-worker
make dev-flower
make dev-web
```

## Ports

| Service | Port |
|---------|------|
| web-client | 5174 |
| cortex-server | 8000 |
| Flower | 5555 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| RabbitMQ | 5672 (AMQP), 15672 (UI) |
| Weaviate | 8080 |
| Neo4j | 7687 |

## Before a PR

```bash
make lint-imports
make flct          # format + lint + mypy + import-linter + test
make db-setup      # alembic upgrade head (empty schema, no seed)
```

Seed data: `infra/postgres/init.sql` on first `docker compose up` (init script).

## K8s (optional)

```bash
make minikube-start
make k8s-build
make k8s-deploy
make k8s-url
```

Namespace: `cortex-monolith`.
