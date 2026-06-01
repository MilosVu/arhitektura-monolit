"""Public facade for the platform domain module."""

from __future__ import annotations

import secrets

from cortex_core.errors import ForbiddenError, NotAuthenticatedError
from cortex_models import User
from fastapi import HTTPException, status
from module_ai.api import AiModule
from sqlalchemy.orm import Session

from module_platform.schemas import (
    AuditLogResponse,
    CaseDetail,
    CaseSummary,
    LoginRequest,
    LoginResponse,
    SsoCallbackRequest,
    SsoUrlResponse,
    SystemStatusResponse,
    UserResponse,
)
from module_platform.services.auth_service import AuthService
from module_platform.services.case_service import CaseService
from module_platform.system import get_system_status


class PlatformModule:
    """In-process facade for auth, cases, audit, and system health."""

    def __init__(
        self,
        ai_module: AiModule | None = None,
        auth_service: AuthService | None = None,
    ) -> None:
        from module_platform.adapters.stub_identity_provider import StubIdentityProvider

        self._ai = ai_module or AiModule()
        self._auth = auth_service or AuthService(identity=StubIdentityProvider())

    @property
    def ai(self) -> AiModule:
        return self._ai

    async def get_system_status(self) -> SystemStatusResponse:
        return await get_system_status(self._ai)

    def get_sso_url(self) -> SsoUrlResponse:
        state = secrets.token_urlsafe(16)
        url = self._auth.build_sso_authorize_url(state=state)
        return SsoUrlResponse(authorize_url=url, state=state)

    def sso_callback(self, body: SsoCallbackRequest, db: Session) -> LoginResponse:
        try:
            token, user = self._auth.login_with_sso_code(body.code, db)
        except NotAuthenticatedError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc
        return LoginResponse(access_token=token, user=UserResponse.model_validate(user))

    def login(self, body: LoginRequest, db: Session) -> LoginResponse:
        try:
            token, user = self._auth.login_mock(body.username, body.password, db)
        except NotAuthenticatedError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc
        return LoginResponse(access_token=token, user=UserResponse.model_validate(user))

    def list_cases(self, user: User, db: Session) -> list[CaseSummary]:
        return CaseService(db).list_for_user(user)

    def get_case(self, case_id: int, user: User, db: Session) -> CaseDetail:
        try:
            return CaseService(db).get_detail(case_id, user)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

    def list_audit_logs(
        self, user: User, db: Session, limit: int = 50
    ) -> list[AuditLogResponse]:
        from cortex_models import AuditLog

        logs = (
            db.query(AuditLog)
            .filter(AuditLog.user_id == user.id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )
        return [AuditLogResponse.model_validate(log) for log in logs]
