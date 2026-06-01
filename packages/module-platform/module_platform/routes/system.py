from typing import Annotated

from cortex_models import User
from fastapi import APIRouter, Depends

from module_platform.api import PlatformModule
from module_platform.deps import get_current_user, get_platform_module
from module_platform.schemas import SystemStatusResponse

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status", response_model=SystemStatusResponse)
async def system_status(
    platform: Annotated[PlatformModule, Depends(get_platform_module)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await platform.get_system_status()
