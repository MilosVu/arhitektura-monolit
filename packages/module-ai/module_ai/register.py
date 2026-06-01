"""DI registracija za module-ai."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry

from module_ai.api import AiModule


def register_services(
    registry: ServiceRegistry,
    *,
    ai_module: AiModule | None = None,
) -> AiModule:
    module = ai_module or AiModule()
    registry.register(AiModule, module)
    return module
