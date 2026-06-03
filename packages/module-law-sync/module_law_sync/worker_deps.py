"""Worker composition root — shared dependencies for law sync Celery tasks."""

from __future__ import annotations

from dataclasses import dataclass

from cortex_connectors import get_law_source
from cortex_core.ports.law_source import LawSourcePort


@dataclass(frozen=True)
class LawSyncWorkerDeps:
    law_source: LawSourcePort


def register_worker_dependencies() -> LawSyncWorkerDeps:
    return LawSyncWorkerDeps(law_source=get_law_source())
