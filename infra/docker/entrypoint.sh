#!/bin/sh
set -e

cd /app

SERVICE="${SERVICE:-cortex-server}"

case "$SERVICE" in
  cortex-server)
    exec /app/.venv/bin/uvicorn cortex_server.main:app --host 0.0.0.0 --port 8000
    ;;
  cortex-worker)
    exec /app/.venv/bin/celery -A cortex_worker.tasks:celery_app worker --loglevel=info -Q sync,ingestion -n worker@%h
    ;;
  flower)
    exec /app/.venv/bin/celery -A cortex_worker.tasks:celery_app flower --port=5555 --address=0.0.0.0
    ;;
  *)
    echo "Unknown SERVICE: $SERVICE"
    exit 1
    ;;
esac
