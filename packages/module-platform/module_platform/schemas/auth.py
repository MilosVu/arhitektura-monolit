from cortex_core.enums import UserRole
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str = "mock"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    ad_username: str

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class SsoUrlResponse(BaseModel):
    authorize_url: str
    state: str


class SsoCallbackRequest(BaseModel):
    code: str
    state: str | None = None
