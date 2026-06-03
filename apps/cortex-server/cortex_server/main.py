from contextlib import asynccontextmanager

import cortex_models  # noqa: F401 — register SQLAlchemy mappers
from cortex_core.logging import setup_logging
from cortex_core.registry import ServiceRegistry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from module_ai.register import register_services as register_ai
from module_ai.routes import router as ai_router
from module_chat.register import register_services as register_chat
from module_chat.routes import router as chat_router
from module_documents.register import register_services as register_documents
from module_documents.routes import router as documents_router
from module_law_sync.register import register_services as register_law_sync
from module_law_sync.routes import router as law_sync_router
from module_platform.register import register_services as register_platform
from module_platform.routes import router as platform_router
from module_sync.register import register_services as register_sync
from module_sync.routes import router as sync_router

from cortex_server.middleware.correlation import CorrelationIdMiddleware
from cortex_server.middleware.error_handling import register_error_handlers

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    registry = ServiceRegistry()
    ai_module = register_ai(registry)
    platform_module = register_platform(registry, ai_module=ai_module)
    documents_module = register_documents(registry)
    chat_module = register_chat(registry, ai_module=ai_module)
    sync_module = register_sync(registry)
    law_sync_module = register_law_sync(registry)

    app.state.registry = registry
    app.state.ai_module = ai_module
    app.state.platform_module = platform_module
    app.state.documents_module = documents_module
    app.state.chat_module = chat_module
    app.state.sync_module = sync_module
    app.state.law_sync_module = law_sync_module

    try:
        ai_module.seed_laws_on_startup()
    except Exception:
        pass
    yield
    registry.reset()


app = FastAPI(title="Cortex AI Monolith", version="0.1.0", lifespan=lifespan)
register_error_handlers(app)

app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://cortex-monolith.local",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(platform_router)
app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(sync_router)
app.include_router(law_sync_router)
app.include_router(ai_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "cortex-server"}
