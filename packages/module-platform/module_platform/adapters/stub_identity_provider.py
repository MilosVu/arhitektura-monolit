"""Stub OIDC — MVP bez pravog AD tenanta."""

from __future__ import annotations

from urllib.parse import urlencode

from cortex_core.errors import NotAuthenticatedError
from cortex_core.settings import get_settings

from module_platform.ports.identity_provider_port import IdentityClaims


class StubIdentityProvider:
    """Dev stub: authorize URL vodi na frontend callback sa stub code-om."""

    def build_authorize_url(self, *, state: str) -> str:
        settings = get_settings()
        params = urlencode({"code": "stub-hmueller", "state": state})
        base = settings.ad_redirect_uri.rstrip("/")
        return f"{base}?{params}"

    def exchange_code(self, code: str) -> IdentityClaims:
        if not code.startswith("stub-"):
            raise NotAuthenticatedError("Invalid SSO code (stub provider)")

        username = code.removeprefix("stub-")
        known = {
            "hmueller": ("judge.mueller@gericht.bs.ch", "Dr. Hans Müller", "judge"),
            "aweber": ("clerk.weber@gericht.bs.ch", "Anna Weber", "clerk"),
        }
        if username not in known:
            raise NotAuthenticatedError(f"Unknown stub user: {username}")

        email, full_name, role_group = known[username]
        return IdentityClaims(
            ad_username=username,
            email=email,
            full_name=full_name,
            groups=(role_group,),
        )
