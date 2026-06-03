from cortex_core.messaging.tasks import (
    TASK_REINDEX_LAW_VERSION,
    TASK_SYNC_LAW_CORPUS,
    TASK_SYNC_LAW_PROVISION,
)
from cortex_core.sync_worker_celery import get_sync_celery_app
from cortex_models import get_session_factory

from module_law_sync.services.law_corpus_sync import LawCorpusSyncService
from module_law_sync.worker_deps import register_worker_dependencies

celery_app = get_sync_celery_app()
_worker_deps = register_worker_dependencies()


@celery_app.task(name=TASK_SYNC_LAW_CORPUS, bind=True)
def sync_law_corpus(self, job_id: str, scope: str) -> dict:
    session = get_session_factory()()
    try:
        service = LawCorpusSyncService(session, law_source=_worker_deps.law_source)
        return service.sync_scope(job_id, scope)
    finally:
        session.close()


@celery_app.task(name=TASK_SYNC_LAW_PROVISION, bind=True)
def sync_law_provision(self, job_id: str, ref: str, scope: str) -> dict:
    """Sync a single provision — placeholder until phase 5."""
    session = get_session_factory()()
    try:
        payload = _worker_deps.law_source.fetch_provision(ref, scope=scope)
        if payload is None:
            return {"status": "failed", "reason": f"provision not found: {ref}"}
        from module_law_sync.services.law_version_service import LawVersionService

        version = LawVersionService(session).create_version(
            payload, law_sync_job_id=job_id
        )
        session.commit()
        return {"status": "completed", "version_id": version.id, "ref": ref}
    finally:
        session.close()


@celery_app.task(name=TASK_REINDEX_LAW_VERSION, bind=True)
def reindex_law_version(self, version_id: int) -> dict:
    """Re-index a law version into Weaviate — stub until phase 4."""
    return {"status": "stub", "version_id": version_id}
