#!/bin/sh
set -e

cd /app

SERVICE="${SERVICE:-cortex-server}"

case "$SERVICE" in
  cortex-server)
    exec /app/.venv/bin/uvicorn cortex_server.main:app --host 0.0.0.0 --port 8000
    ;;
  sync-worker)
    exec /app/.venv/bin/celery -A sync_worker.tasks:celery_app worker --loglevel=info -Q sync -n sync@%h
    ;;
  ingestion-worker)
    exec /app/.venv/bin/celery -A ingestion_worker.tasks:celery_app worker --loglevel=info -Q ingestion -n ingestion@%h
    ;;
  flower)
    exec /app/.venv/bin/celery -A sync_worker.tasks:celery_app flower --port=5555 --address=0.0.0.0
    ;;
  *)
    echo "Unknown SERVICE: $SERVICE"
    exit 1
    ;;
esac
