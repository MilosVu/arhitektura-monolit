# Cortex AI — Monolit arhitektura

Ista MVP funkcionalnost kao [mikroservisna verzija](../arhitektura-mikroservisi/), ali sa **modularnim monolitom**: jedan FastAPI server + odvojeni Celery workeri.

## Dokumentacija za tim

| Dokument | Svrha |
|----------|-------|
| **[docs/onboarding/README.md](docs/onboarding/README.md)** | **Početak za development tim** |
| [docs/onboarding/gde-sta-ide.md](docs/onboarding/gde-sta-ide.md) | Gde implementirati novi kod |
| [MODULE-BOUNDARIES.md](MODULE-BOUNDARIES.md) | Granice modula |
| [ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md) | Arhitektura i integracije |
| [docs/UPOREDBA-PROJEKAT-2.md](docs/UPOREDBA-PROJEKAT-2.md) | Razlike vs. referentni primer 2 |
| [AGENTS.md](AGENTS.md) | Vodič za AI asistente |

> Refactor plan: [REFACTOR-PLAN.md](REFACTOR-PLAN.md)

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
