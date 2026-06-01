from fastapi import APIRouter

from module_sync.routes.sync import router as sync_router

router = APIRouter()
router.include_router(sync_router)
