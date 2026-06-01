"""DI registracija za module-ingestion (Celery pipeline)."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry

from module_ingestion.worker_deps import (
    IngestionWorkerDeps,
    register_worker_dependencies,
)


def register_services(registry: ServiceRegistry) -> IngestionWorkerDeps:
    deps = register_worker_dependencies()
    registry.register(IngestionWorkerDeps, deps)
    return deps
