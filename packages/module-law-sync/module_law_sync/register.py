"""DI registration for module-law-sync."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry

from module_law_sync.api import LawSyncModule


def register_services(
    registry: ServiceRegistry,
    *,
    law_sync_module: LawSyncModule | None = None,
) -> LawSyncModule:
    module = law_sync_module or LawSyncModule()
    registry.register(LawSyncModule, module)
    return module
