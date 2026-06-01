from typing import Annotated

from cortex_models import Case, Document, User, get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from module_ai.routes.deps import get_ai_module, get_current_user
from module_ai.schemas import TranslateRequest, TranslateResponse

router = APIRouter(tags=["translate"])


@router.post("/documents/{document_id}/translate", response_model=TranslateResponse)
def translate_doc(
    document_id: int,
    body: TranslateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    ai: Annotated[object, Depends(get_ai_module)],
):
    doc = (
        db.query(Document)
        .join(Case)
        .filter(Document.id == document_id, Case.owner_id == current_user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    mock_text = (
        f"[Mock extracted text from {doc.filename}] Die Parteien vereinbaren hiermit..."
    )
    return ai.translate(
        document_id=document_id,
        text=mock_text,
        source_lang=body.source_lang,
        target_lang=body.target_lang,
    )
