"""Autentifikacija — AD + JWT + Redis session cache."""

from sqlalchemy.orm import Session

from cortex_core.base.service import BaseService
from cortex_core.infrastructure.redis.session_cache import AdSessionCache
from module_platform.models import User


class AuthService(BaseService):
    """
    Odgovornosti (produkcija):
      - validate_ad_credentials(username, password)
      - map_ad_groups_to_roles(groups) -> UserRole
      - issue_jwt(user) -> token
      - cache_ad_session(user_id, roles) u Redis
    """

    def __init__(self, db: Session, session_cache: AdSessionCache | None = None) -> None:
        self._db = db
        self._session_cache = session_cache or AdSessionCache()

    def find_user_by_username(self, username: str) -> User | None:
        return self._db.query(User).filter(User.ad_username == username).first()

    def cache_user_session(self, user: User) -> None:
        """Poziva se posle uspešnog login-a — smanjuje AD lookup-e."""
        self._session_cache.set_session(
            user.id,
            roles=[user.role],
            ad_groups=[],  # TODO: iz AD LDAP-a
        )

    def validate_ad_credentials(self, username: str, password: str) -> bool:
        """Stub — MVP prihvata bilo koji password za poznate usere."""
        _ = password
        return self.find_user_by_username(username) is not None
