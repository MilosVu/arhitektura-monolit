from datetime import datetime

from cortex_core.db import Base
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LawCode(Base):
    __tablename__ = "law_codes"
    __table_args__ = (
        UniqueConstraint(
            "code",
            "jurisdiction",
            "canton_code",
            name="uq_law_codes_scope",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(20), nullable=False)
    canton_code: Mapped[str | None] = mapped_column(String(10))
    official_uri: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    provisions: Mapped[list["LawProvision"]] = relationship(back_populates="law_code")


class LawProvision(Base):
    __tablename__ = "law_provisions"
    __table_args__ = (
        UniqueConstraint("law_code_id", "ref", name="uq_law_provisions_ref"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    law_code_id: Mapped[int] = mapped_column(ForeignKey("law_codes.id"), nullable=False)
    ref: Mapped[str] = mapped_column(String(100), nullable=False)
    article_number: Mapped[str | None] = mapped_column(String(50))
    title: Mapped[str | None] = mapped_column(String(500))

    law_code: Mapped["LawCode"] = relationship(back_populates="provisions")
    versions: Mapped[list["LawVersion"]] = relationship(back_populates="provision")
