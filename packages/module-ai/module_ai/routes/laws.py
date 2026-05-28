from typing import Annotated

from fastapi import APIRouter, Depends

from module_platform.models import User
from module_ai.routes.deps import get_ai_module, get_current_user
from module_ai.schemas import LawNodeResponse

router = APIRouter(prefix="/laws", tags=["laws"])


@router.get("/{law_ref}", response_model=LawNodeResponse)
def get_law(
    law_ref: str,
    current_user: Annotated[User, Depends(get_current_user)],
    ai: Annotated[object, Depends(get_ai_module)],
):
    return ai.lookup_law(law_ref)
