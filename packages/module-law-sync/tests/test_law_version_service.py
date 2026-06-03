"""Unit tests for LawVersionService — immutable versions and supersede."""

from __future__ import annotations

from datetime import date

import cortex_models  # noqa: F401 — register mappers
from cortex_core.db import Base
from cortex_core.enums import LawJurisdiction, LawSourceType
from cortex_core.ports.law_source import LawProvisionPayload
from module_law_sync.services.law_version_service import LawVersionService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _payload(*, valid_from: date, content: str) -> LawProvisionPayload:
    return LawProvisionPayload(
        ref="or-41",
        law_code="OR",
        law_title="Obligationenrecht",
        jurisdiction=LawJurisdiction.FEDERAL.value,
        canton_code=None,
        article_number="41",
        article_title="Schadenersatz",
        content=content,
        valid_from=valid_from,
        source=LawSourceType.STUB.value,
        source_version_id=f"stub-{valid_from.isoformat()}",
    )


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_create_version_inserts_immutable_row() -> None:
    session = _session()
    service = LawVersionService(session)

    version = service.create_version(
        _payload(valid_from=date(2020, 1, 1), content="v1")
    )
    session.commit()

    assert version.id is not None
    assert version.valid_from == date(2020, 1, 1)
    assert version.valid_to is None
    assert version.blob_path == "laws/federal/or/or-41/2020-01-01.md"


def test_supersede_sets_valid_to_on_previous_version() -> None:
    session = _session()
    service = LawVersionService(session)

    first = service.create_version(_payload(valid_from=date(2020, 1, 1), content="v1"))
    session.commit()
    first_id = first.id

    second = service.create_version(
        _payload(valid_from=date(2024, 6, 15), content="v2 updated text")
    )
    session.commit()

    session.refresh(first)
    assert first.valid_to == date(2024, 6, 15)
    assert second.valid_to is None
    assert second.id != first_id
    assert second.content_checksum != first.content_checksum
