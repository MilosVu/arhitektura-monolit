from pydantic import BaseModel

from cortex_core.enums import UserRole


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
