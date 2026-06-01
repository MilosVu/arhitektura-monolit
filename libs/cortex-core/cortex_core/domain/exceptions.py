"""Backward-compatible re-exports — prefer ``cortex_core.errors``."""

from cortex_core.errors import (
    CortexError,
    DocumentNotFoundError,
    ForbiddenError,
    SyncJobNotFoundError,
)

__all__ = [
    "CortexError",
    "DocumentNotFoundError",
    "ForbiddenError",
    "SyncJobNotFoundError",
]
