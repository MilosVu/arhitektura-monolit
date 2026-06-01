"""Enqueue DMS sync — sends task name only (no DMS logic)."""

from cortex_core.celery_app import create_celery_app
from cortex_core.messaging.tasks import QUEUE_SYNC, TASK_SYNC_CASE

_producer_app = create_celery_app("cortex_server")


def enqueue_sync_job(case_id: int, job_id: str) -> None:
    _producer_app.send_task(
        TASK_SYNC_CASE,
        args=[case_id, job_id],
        queue=QUEUE_SYNC,
    )
