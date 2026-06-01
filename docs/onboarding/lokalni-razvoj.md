# Lokalni razvoj

## Preduslovi

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Docker (za infra)
- Node/pnpm (za web-client — Makefile koristi `npx pnpm`)

## Prvi put

```bash
cd arhitektura-monolit
make infra-up      # Postgres, Redis, RabbitMQ, Weaviate, Neo4j
make install       # uv sync + web-client deps
make seed-neo4j    # opciono, law graph
make lint-imports  # arhitekturne granice
```

## Pokretanje

### Sve odjednom (preporučeno)

```bash
make dev
# ili
./scripts/dev.sh
```

### Pojedinačno

```bash
make dev-server
make dev-sync-worker
make dev-ingestion-worker
make dev-flower
make dev-web
```

## Portovi

| Servis | Port |
|--------|------|
| web-client | 5174 |
| cortex-server | 8000 |
| Flower | 5555 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| RabbitMQ | 5672 (AMQP), 15672 (UI) |
| Weaviate | 8080 |
| Neo4j | 7687 |

## Pre PR-a

```bash
make lint-imports
```

```bash
make flct          # format + lint + mypy + import-linter + test
make db-setup      # alembic upgrade head (prazna šema, bez seed-a)
```

Seed podaci: `infra/postgres/init.sql` pri prvom `docker compose up` (init skripta).

## K8s (opciono)

```bash
make minikube-start
make k8s-build
make k8s-deploy
make k8s-url
```

Namespace: `cortex-monolith`.
