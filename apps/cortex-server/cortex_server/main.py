from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from module_ai.api import AiModule
from module_ai.routes import router as ai_router
import module_platform.models  # noqa: F401 — register SQLAlchemy mappers
from module_platform.api import PlatformModule
from module_platform.routes import router as platform_router

ai_module = AiModule()
platform_module = PlatformModule(ai_module=ai_module)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        ai_module.seed_laws_on_startup()
    except Exception:
        pass
    yield


app = FastAPI(title="Cortex AI Monolith", version="0.1.0", lifespan=lifespan)
app.state.ai_module = ai_module
app.state.platform_module = platform_module

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://cortex-monolith.local"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(platform_router)
app.include_router(ai_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "cortex-server"}
