from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_platform.models import User, get_db
from module_ai.routes.deps import get_current_user, get_platform_module
from module_ai.schemas import TranslateRequest, TranslateResponse

router = APIRouter(tags=["translate"])


@router.post("/documents/{document_id}/translate", response_model=TranslateResponse)
def translate_doc(
    document_id: int,
    body: TranslateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    platform: Annotated[object, Depends(get_platform_module)],
):
    return platform.translate_document(document_id, body, current_user, db)
