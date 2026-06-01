"""DI registracija za module-dms-sync (Celery tasks — bez HTTP facade)."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry

from module_dms_sync.worker_deps import DmsSyncWorkerDeps, register_worker_dependencies


def register_services(registry: ServiceRegistry) -> DmsSyncWorkerDeps:
    """Worker modul — taskovi se registruju preko Celery autodiscover."""
    deps = register_worker_dependencies()
    registry.register(DmsSyncWorkerDeps, deps)
    return deps
