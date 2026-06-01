"""
AD sesija / JWT metadata keš — smanjuje opterećenje Active Directory-a.

Ključevi:
  cortex:ad:session:{user_id}  → { roles, groups, cached_at }
  cortex:ad:token:{jti}        → invalidacija / blacklist (future)
"""

from datetime import UTC, datetime

from cortex_core.infrastructure.redis.client import RedisCacheAdapter

AD_SESSION_TTL = 3600  # 1h


class AdSessionCache:
    """Kešira AD grupe i uloge nakon prvog login-a (api-gateway)."""

    def __init__(self, cache: RedisCacheAdapter | None = None) -> None:
        self._cache = cache or RedisCacheAdapter()

    def _key(self, user_id: int) -> str:
        return f"cortex:ad:session:{user_id}"

    def get_session(self, user_id: int) -> dict | None:
        return self._cache.get_json(self._key(user_id))

    def set_session(
        self, user_id: int, *, roles: list[str], ad_groups: list[str]
    ) -> None:
        payload = {
            "user_id": user_id,
            "roles": roles,
            "ad_groups": ad_groups,
            "cached_at": datetime.now(UTC).isoformat(),
        }
        self._cache.set_json(self._key(user_id), payload, ttl_seconds=AD_SESSION_TTL)

    def invalidate(self, user_id: int) -> None:
        self._cache.delete(self._key(user_id))
