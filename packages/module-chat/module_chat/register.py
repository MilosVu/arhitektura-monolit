"""DI registracija za module-chat."""

from __future__ import annotations

from cortex_core.registry import ServiceRegistry
from module_ai.api import AiModule

from module_chat.adapters.redis_chat_store import RedisChatStore
from module_chat.api import ChatModule


def register_services(
    registry: ServiceRegistry,
    *,
    ai_module: AiModule | None = None,
    chat_module: ChatModule | None = None,
) -> ChatModule:
    if ai_module is None and registry.is_registered(AiModule):
        ai_module = registry.resolve(AiModule)
    store = RedisChatStore()
    module = chat_module or ChatModule(ai_module=ai_module, chat_store=store)
    registry.register(ChatModule, module)
    return module
