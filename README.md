# Cortex AI — Monolit arhitektura

Ista MVP funkcionalnost kao [mikroservisna verzija](../arhitektura-mikroservisi/), ali sa **jednim FastAPI serverom** (API + AI in-process) i **jednim Celery workerom** (sync + ingestion).

## Arhitektura

```
web-client (React) → cortex-server (FastAPI) → PostgreSQL / Redis
                        ↓ in-process              ↓
                     AI modul                   RabbitMQ → cortex-worker
                        ↓                                          ↓
                    Weaviate / Neo4j                          Weaviate
```

## Brzo pokretanje

```bash
make infra-up
make install
make dev
```

Otvori **http://localhost:5174** (monolit koristi port 5174 da ne konflikuje sa mikroservisima na 5173).

Login: `hmueller` / `mock`

## Servisi (lokalno)

| Servis | Port | Opis |
|--------|------|------|
| web-client | 5174 | React frontend |
| cortex-server | 8000 | API + AI (monolit) |
| cortex-worker | — | Celery (sync + ingestion queue) |
| Flower | 5555 | Celery monitoring |

## Kubernetes

Namespace: **`cortex-monolith`** (paralelno sa `cortex-ai` mikroservisa)

```bash
make k8s-build
make k8s-deploy
make k8s-seed-neo4j
make k8s-url
```

| URL | Port |
|-----|------|
| App | `:30081` |
| Flower | `:30556` |
| RabbitMQ UI | `:31673` |

## Poređenje

Vidi [analiza-komparativna.md](../analiza-komparativna.md) u root folderu.
