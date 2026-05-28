"""Shared Celery app for worker modules (avoids module → cortex-worker import cycle)."""

from celery import Celery

from cortex_core.celery_app import create_celery_app

_worker_app: Celery | None = None


def get_worker_celery_app() -> Celery:
    global _worker_app
    if _worker_app is None:
        _worker_app = create_celery_app(
            "cortex_worker",
            include=["module_alfresco.tasks", "module_ingestion.tasks"],
        )
    return _worker_app
