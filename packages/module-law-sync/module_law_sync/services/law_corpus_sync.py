import json
from datetime import UTC, datetime

from cortex_core.enums import LawSyncJobStatus
from cortex_core.ports.law_source import LawSourcePort
from cortex_models import LawSyncJob
from sqlalchemy.orm import Session

from module_law_sync.services.law_version_service import LawVersionService


class LawCorpusSyncService:
    """Orchestrates law source fetch and version persistence."""

    def __init__(self, db: Session, *, law_source: LawSourcePort) -> None:
        self._db = db
        self._law_source = law_source
        self._versions = LawVersionService(db)

    def sync_scope(self, job_id: str, scope: str) -> dict:
        job = self._db.query(LawSyncJob).filter(LawSyncJob.id == job_id).first()
        if not job:
            return {"status": "failed", "reason": "job not found"}

        job.status = LawSyncJobStatus.RUNNING.value
        job.message = f"Syncing law corpus for scope {scope}"
        job.progress = 10
        self._db.commit()

        synced_refs: list[str] = []
        version_ids: list[int] = []

        try:
            refs = self._law_source.list_refs_for_scope(scope)
            total = max(len(refs), 1)

            for index, ref in enumerate(refs, start=1):
                payload = self._law_source.fetch_provision(ref, scope=scope)
                if payload is None:
                    continue
                version = self._versions.create_version(payload, law_sync_job_id=job_id)
                synced_refs.append(ref)
                version_ids.append(version.id)
                job.progress = int(10 + (80 * index / total))

            self._db.commit()

            stats = {
                "scope": scope,
                "provision_count": len(synced_refs),
                "refs": synced_refs,
                "version_ids": version_ids,
            }
            job.status = LawSyncJobStatus.COMPLETED.value
            job.progress = 100
            job.message = f"Synced {len(synced_refs)} provision(s)"
            job.stats_json = json.dumps(stats)
            job.finished_at = datetime.now(UTC)
            self._db.commit()
            return {"status": "completed", **stats}
        except Exception as exc:
            job.status = LawSyncJobStatus.FAILED.value
            job.message = str(exc)
            job.finished_at = datetime.now(UTC)
            self._db.commit()
            return {"status": "failed", "reason": str(exc)}
