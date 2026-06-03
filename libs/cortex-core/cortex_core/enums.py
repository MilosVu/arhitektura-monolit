import enum


class UserRole(str, enum.Enum):
    JUDGE = "judge"
    CLERK = "clerk"
    ADMIN = "admin"


class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    SYNCING = "syncing"
    INGESTING = "ingesting"
    READY = "ready"
    FAILED = "failed"


class SyncJobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class LawJurisdiction(str, enum.Enum):
    FEDERAL = "federal"
    CANTONAL = "cantonal"


class LawSourceType(str, enum.Enum):
    FEDLEX_API = "fedlex_api"
    SCRAPER = "scraper"
    STUB = "stub"


class LawSyncJobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
