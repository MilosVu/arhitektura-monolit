"""DI registracija za module-platform."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry
from module_ai.api import AiModule

from module_platform.adapters.stub_identity_provider import StubIdentityProvider
from module_platform.api import PlatformModule
from module_platform.services.auth_service import AuthService


def register_services(
    registry: ServiceRegistry,
    *,
    ai_module: AiModule | None = None,
    platform_module: PlatformModule | None = None,
) -> PlatformModule:
    ai = ai_module
    if ai is not None and not registry.is_registered(AiModule):
        registry.register(AiModule, ai)
    elif ai is None and registry.is_registered(AiModule):
        ai = registry.resolve(AiModule)

    auth = AuthService(identity=StubIdentityProvider())
    registry.register(AuthService, auth)

    module = platform_module or PlatformModule(ai_module=ai, auth_service=auth)
    registry.register(PlatformModule, module)
    return module
