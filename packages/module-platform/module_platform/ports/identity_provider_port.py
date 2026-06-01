"""Port za AD / OIDC identitet."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class IdentityClaims:
    ad_username: str
    email: str
    full_name: str
    groups: tuple[str, ...] = ()


class IdentityProviderPort(Protocol):
    def build_authorize_url(self, *, state: str) -> str: ...

    def exchange_code(self, code: str) -> IdentityClaims: ...
