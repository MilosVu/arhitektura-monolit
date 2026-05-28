from fastapi import APIRouter

from module_ai.routes import laws, rag, translate

router = APIRouter()
router.include_router(rag.router)
router.include_router(laws.router)
router.include_router(translate.router)
