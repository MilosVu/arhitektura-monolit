"""Apstrakcija keša — Redis implementacija u infrastructure sloju."""

from abc import ABC, abstractmethod
from typing import Any


class CachePort(ABC):
    """Generički key-value + pub/sub interfejs (Redis iza scene)."""

    @abstractmethod
    def get(self, key: str) -> str | None: ...

    @abstractmethod
    def set(self, key: str, value: str, *, ttl_seconds: int | None = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def publish(self, channel: str, message: str) -> None: ...

    @abstractmethod
    def ping(self) -> bool: ...

    # LangGraph checkpoint hook
    @abstractmethod
    def get_json(self, key: str) -> dict[str, Any] | None: ...

    @abstractmethod
    def set_json(
        self, key: str, payload: dict[str, Any], *, ttl_seconds: int | None = None
    ) -> None: ...
