"""Dedicated Celery app for ingestion worker modules."""

from celery import Celery

from cortex_core.celery_app import create_celery_app

_ingestion_app: Celery | None = None


def get_ingestion_celery_app() -> Celery:
    global _ingestion_app
    if _ingestion_app is None:
        _ingestion_app = create_celery_app(
            "ingestion_worker",
            include=["module_ingestion.tasks"],
        )
    return _ingestion_app
