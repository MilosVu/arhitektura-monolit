"""Dedicated Celery app for DMS sync worker modules."""

from celery import Celery

from cortex_core.celery_app import create_celery_app

_sync_app: Celery | None = None


def get_sync_celery_app() -> Celery:
    global _sync_app
    if _sync_app is None:
        _sync_app = create_celery_app(
            "sync_worker",
            include=["module_dms_sync.tasks"],
        )
    return _sync_app
