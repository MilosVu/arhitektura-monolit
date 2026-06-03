from fastapi import APIRouter

from module_law_sync.routes.law_sync import router as law_sync_router

router = APIRouter()
router.include_router(law_sync_router)
