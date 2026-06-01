"""Celery task konvencije i bazna klasa za workere."""

from abc import ABC, abstractmethod

# Imena queue-ova (RabbitMQ)
QUEUE_SYNC = "sync"
QUEUE_INGESTION = "ingestion"

# Imena taskova (modularni monolit)
TASK_SYNC_CASE = "module_dms_sync.tasks.sync_case_from_dms"
TASK_INGEST_DOCUMENT = "module_ingestion.tasks.ingest_document"
TASK_FINALIZE_SYNC = "module_dms_sync.tasks.finalize_sync_job"


class BaseWorkerTask(ABC):
    """
    Bazni Celery task — svaki worker task nasleđuje ovu strukturu.

    Pattern:
      1. učitaj kontekst iz PostgreSQL
      2. pozovi domain service
      3. ažuriraj status + SyncProgressPublisher
    """

    @abstractmethod
    def run(self, *args, **kwargs):
        """Implementacija u sync-worker / ingestion-worker."""
