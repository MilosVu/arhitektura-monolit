#!/usr/bin/env bash
# Pokreće monolit stack: API, oba Celery workera, Flower, web UI.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]] && [[ -f infra/.env.example ]]; then
  cp infra/.env.example .env
fi

cleanup() {
  trap - EXIT INT TERM
  kill 0 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Starting Cortex monolith (API :8000, workers, flower :5555, web :5174)..."

uv run uvicorn cortex_server.main:app \
  --app-dir apps/cortex-server \
  --host 0.0.0.0 --port 8000 --reload &

uv run celery -A sync_worker.tasks:celery_app worker \
  --loglevel=info -Q sync -n sync@%h &

uv run celery -A ingestion_worker.tasks:celery_app worker \
  --loglevel=info -Q ingestion -n ingest@%h &

uv run celery -A sync_worker.tasks:celery_app flower --port=5555 &

(cd apps/web-client && npx --yes pnpm@9 dev) &

wait
