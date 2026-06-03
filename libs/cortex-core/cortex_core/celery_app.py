from celery import Celery

from cortex_core.settings import get_settings


def create_celery_app(app_name: str, include: list[str] | None = None) -> Celery:
    settings = get_settings()
    app = Celery(
        app_name,
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
        include=include or [],
    )
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Europe/Zurich",
        enable_utc=True,
        task_track_started=True,
        task_routes={
            "module_dms_sync.tasks.*": {"queue": "sync"},
            "module_law_sync.tasks.*": {"queue": "sync"},
            "module_ingestion.tasks.*": {"queue": "ingestion"},
        },
    )
    return app
