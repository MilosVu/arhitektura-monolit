from datetime import date, datetime
from uuid import uuid4

from cortex_core.db import Base
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LawSyncJob(Base):
    __tablename__ = "law_sync_jobs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    scope: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    message: Mapped[str | None] = mapped_column(Text)
    stats_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    versions: Mapped[list["LawVersion"]] = relationship(back_populates="sync_job")


class LawVersion(Base):
    __tablename__ = "law_versions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    provision_id: Mapped[int] = mapped_column(
        ForeignKey("law_provisions.id"), nullable=False
    )
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_to: Mapped[date | None] = mapped_column(Date)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    source_version_id: Mapped[str | None] = mapped_column(String(255))
    content_checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    blob_path: Mapped[str | None] = mapped_column(String(500))
    content: Mapped[str | None] = mapped_column(Text)
    law_sync_job_id: Mapped[str | None] = mapped_column(ForeignKey("law_sync_jobs.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    provision: Mapped["LawProvision"] = relationship(back_populates="versions")
    sync_job: Mapped["LawSyncJob | None"] = relationship(back_populates="versions")
