"""DI registracija za module-sync."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry

from module_sync.api import SyncModule


def register_services(
    registry: ServiceRegistry,
    *,
    sync_module: SyncModule | None = None,
) -> SyncModule:
    module = sync_module or SyncModule()
    registry.register(SyncModule, module)
    return module
