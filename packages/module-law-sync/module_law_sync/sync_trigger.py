"""Enqueue law corpus sync — sends task name only."""

from cortex_core.celery_app import create_celery_app
from cortex_core.messaging.tasks import QUEUE_SYNC, TASK_SYNC_LAW_CORPUS

_producer_app = create_celery_app("cortex_server")


def enqueue_law_sync_job(job_id: str, scope: str) -> None:
    _producer_app.send_task(
        TASK_SYNC_LAW_CORPUS,
        args=[job_id, scope],
        queue=QUEUE_SYNC,
    )
