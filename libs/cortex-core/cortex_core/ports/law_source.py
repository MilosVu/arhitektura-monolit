"""Port for external Swiss law sources (Fedlex API, scrapers)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LawProvisionPayload:
    """Normalized law provision from any source adapter."""

    ref: str
    law_code: str
    law_title: str
    jurisdiction: str
    canton_code: str | None
    article_number: str | None
    article_title: str | None
    content: str
    valid_from: date
    source: str
    source_version_id: str | None = None


class LawSourcePort(ABC):
    """Fetch law provisions from official APIs or scrapers."""

    @abstractmethod
    def list_refs_for_scope(self, scope: str) -> list[str]:
        """Return provision refs to sync for scope (e.g. federal, cantonal:ZH)."""

    @abstractmethod
    def fetch_provision(self, ref: str, *, scope: str) -> LawProvisionPayload | None:
        """Fetch a single provision by stable ref."""
