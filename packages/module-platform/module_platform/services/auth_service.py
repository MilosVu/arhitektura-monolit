"""Autentifikacija — AD/OIDC port + JWT."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from cortex_core.errors import NotAuthenticatedError
from cortex_core.infrastructure.redis.session_cache import AdSessionCache
from cortex_core.settings import get_settings
from cortex_models import AuditLog, User
from jose import jwt
from sqlalchemy.orm import Session

from module_platform.ports.identity_provider_port import (
    IdentityClaims,
    IdentityProviderPort,
)


class AuthService:
    def __init__(
        self,
        identity: IdentityProviderPort,
        session_cache: AdSessionCache | None = None,
    ) -> None:
        self._identity = identity
        self._session_cache = session_cache or AdSessionCache()
        self._settings = get_settings()

    def build_sso_authorize_url(self, *, state: str) -> str:
        return self._identity.build_authorize_url(state=state)

    def login_with_sso_code(self, code: str, db: Session) -> tuple[str, User]:
        claims = self._identity.exchange_code(code)
        user = self._upsert_user(claims, db)
        self.cache_user_session(user)
        token = self._issue_jwt(user)
        self._audit_login(user, db, method="sso")
        return token, user

    def login_mock(self, username: str, password: str, db: Session) -> tuple[str, User]:
        if not self._settings.auth_mock_enabled:
            raise NotAuthenticatedError("Mock login is disabled")

        user = db.query(User).filter(User.ad_username == username).first()
        if not user:
            raise NotAuthenticatedError("Invalid credentials")
        _ = password

        self.cache_user_session(user)
        token = self._issue_jwt(user)
        self._audit_login(user, db, method="mock")
        return token, user

    def cache_user_session(self, user: User) -> None:
        self._session_cache.set_session(
            user.id,
            roles=[user.role],
            ad_groups=[],
        )

    def _upsert_user(self, claims: IdentityClaims, db: Session) -> User:
        user = db.query(User).filter(User.ad_username == claims.ad_username).first()
        if user:
            return user

        role = claims.groups[0] if claims.groups else "lawyer"
        user = User(
            email=claims.email,
            full_name=claims.full_name,
            role=role,
            ad_username=claims.ad_username,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def _issue_jwt(self, user: User) -> str:
        expire = datetime.now(UTC) + timedelta(hours=8)
        return jwt.encode(
            {"sub": str(user.id), "role": user.role, "exp": expire},
            self._settings.jwt_secret,
            algorithm=self._settings.jwt_algorithm,
        )

    def _audit_login(self, user: User, db: Session, *, method: str) -> None:
        audit = AuditLog(
            user_id=user.id,
            action="login",
            resource_type="user",
            resource_id=str(user.id),
            details=f"Login via {method} for {user.ad_username}",
        )
        db.add(audit)
        db.commit()
