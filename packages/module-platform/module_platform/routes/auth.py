from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from module_platform.api import PlatformModule
from module_platform.deps import get_current_user, get_platform_module
from module_platform.models import User, get_db
from module_platform.schemas import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    body: LoginRequest,
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    db: Session = Depends(get_db),
):
    return platform.login(body, db)


@router.get("/me", response_model=UserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return UserResponse.model_validate(current_user)
