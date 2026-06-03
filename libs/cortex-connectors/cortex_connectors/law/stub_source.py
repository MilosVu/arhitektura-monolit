"""Stub law source — returns fixture provisions for dev and tests."""

from datetime import date

from cortex_core.enums import LawJurisdiction, LawSourceType
from cortex_core.ports.law_source import LawProvisionPayload, LawSourcePort

_STUB_OR_41 = LawProvisionPayload(
    ref="or-41",
    law_code="OR",
    law_title="Obligationenrecht",
    jurisdiction=LawJurisdiction.FEDERAL.value,
    canton_code=None,
    article_number="41",
    article_title="Schadenersatz",
    content=(
        "Wer unrichtig, unsorgfältig oder in Übertretung vertraglicher oder "
        "gesetzlicher Pflichten einen Schaden verursacht, haftet dem Geschädigten "
        "für dessen Behebung."
    ),
    valid_from=date(2020, 1, 1),
    source=LawSourceType.STUB.value,
    source_version_id="stub-or-41-v1",
)


class StubLawSource(LawSourcePort):
    """MVP stub — one federal provision until Fedlex adapter lands."""

    def list_refs_for_scope(self, scope: str) -> list[str]:
        if scope == "federal":
            return ["or-41"]
        return []

    def fetch_provision(self, ref: str, *, scope: str) -> LawProvisionPayload | None:
        if scope == "federal" and ref == "or-41":
            return _STUB_OR_41
        return None
