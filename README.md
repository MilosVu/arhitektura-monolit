# Cortex AI — Monolit arhitektura

Ista MVP funkcionalnost kao [mikroservisna verzija](../arhitektura-mikroservisi/), ali sa **modularnim monolitom**: jedan FastAPI server + odvojeni Celery workeri.

## Dokumentacija

| Publika | Ulazna tačka |
|---------|--------------|
| **Svi** | **[docs/README.md](docs/README.md)** |
| PM / product | [docs/product/README.md](docs/product/README.md) |
| Development tim | **[docs/engineering/README.md](docs/engineering/README.md)** |
| Arhitektonske odluke | [docs/engineering/decisions/README.md](docs/engineering/decisions/README.md) |
| AI asistenti | [AGENTS.md](AGENTS.md) |

## Arhitektura

```
web-client → cortex-server → module-platform / documents / chat / sync / ai
                                ↓
                             RabbitMQ → sync-worker (module-dms-sync)
                                      → ingestion-worker (module-ingestion)
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
| cortex-server | 8000 | API composition root |
| sync-worker | — | Celery queue `sync` |
| ingestion-worker | — | Celery queue `ingestion` |
| Flower | 5555 | Celery monitoring |

## Kubernetes

Namespace: **`cortex-monolith`**

```bash
make minikube-start
make k8s-build
make k8s-deploy
make k8s-url
```

Podovi: `cortex-server`, `sync-worker`, `ingestion-worker`, `web-client`, infra (postgres, redis, rabbitmq, weaviate, neo4j), flower.
