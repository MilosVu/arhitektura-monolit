"""Observability stubs — no-op telemetry hooks for MVP."""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any


@contextmanager
def trace_span(name: str, **attributes: Any) -> Generator[None, None, None]:
    """Context manager za distributed tracing span (stub)."""
    _ = (name, attributes)
    yield


def record_metric(name: str, value: float, **tags: str) -> None:
    """Zabeleži metriku (stub no-op)."""
    _ = (name, value, tags)


def increment_counter(name: str, **tags: str) -> None:
    """Inkrementiraj counter metriku (stub no-op)."""
    _ = (name, tags)
