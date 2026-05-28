"""Backward-compatible re-exports — prefer module_platform.models in new code."""

from cortex_core.db import Base, get_db, get_engine, get_session_factory
from module_platform.models import AuditLog, Case, Document, SyncJob, User

__all__ = [
    "AuditLog",
    "Base",
    "Case",
    "Document",
    "SyncJob",
    "User",
    "get_db",
    "get_engine",
    "get_session_factory",
]
