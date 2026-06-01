from fastapi import APIRouter

from module_documents.routes.documents import router as documents_router

router = APIRouter()
router.include_router(documents_router)
