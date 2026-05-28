from fastapi import APIRouter

from module_platform.routes import audit, auth, cases, chat, documents, sync, system

router = APIRouter()
router.include_router(auth.router)
router.include_router(cases.router)
router.include_router(documents.router)
router.include_router(sync.router)
router.include_router(chat.router)
router.include_router(audit.router)
router.include_router(system.router)
