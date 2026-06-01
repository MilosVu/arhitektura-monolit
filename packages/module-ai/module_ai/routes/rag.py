from typing import Annotated

from cortex_models import Case, User, get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from module_ai.routes.deps import get_ai_module, get_current_user
from module_ai.schemas import RagSearchRequest, RagSearchResponse

router = APIRouter(tags=["rag"])


@router.post("/cases/{case_id}/search", response_model=RagSearchResponse)
def search_case_documents(
    case_id: int,
    body: RagSearchRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    ai: Annotated[object, Depends(get_ai_module)],
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id, Case.owner_id == current_user.id)
        .first()
    )
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return ai.rag_search(body.query, case_id, body.limit)
