import hashlib
from datetime import date

from cortex_core.enums import LawJurisdiction
from cortex_core.ports.law_source import LawProvisionPayload
from cortex_models import LawCode, LawProvision, LawVersion
from sqlalchemy.orm import Session


class LawVersionService:
    """Immutable law version records — sole writer of LawVersion rows."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create_version(
        self,
        payload: LawProvisionPayload,
        *,
        law_sync_job_id: str | None = None,
    ) -> LawVersion:
        law_code = self._get_or_create_law_code(payload)
        provision = self._get_or_create_provision(law_code, payload)
        self._supersede_current_version(provision.id, payload.valid_from)

        checksum = hashlib.sha256(payload.content.encode()).hexdigest()
        blob_path = self._blob_path(payload)

        version = LawVersion(
            provision_id=provision.id,
            valid_from=payload.valid_from,
            valid_to=None,
            source=payload.source,
            source_version_id=payload.source_version_id,
            content_checksum=checksum,
            blob_path=blob_path,
            content=payload.content,
            law_sync_job_id=law_sync_job_id,
        )
        self._db.add(version)
        self._db.flush()
        return version

    def get_current_version(self, provision_id: int) -> LawVersion | None:
        return (
            self._db.query(LawVersion)
            .filter(
                LawVersion.provision_id == provision_id,
                LawVersion.valid_to.is_(None),
            )
            .first()
        )

    def _get_or_create_law_code(self, payload: LawProvisionPayload) -> LawCode:
        existing = (
            self._db.query(LawCode)
            .filter(
                LawCode.code == payload.law_code,
                LawCode.jurisdiction == payload.jurisdiction,
                LawCode.canton_code == payload.canton_code,
            )
            .first()
        )
        if existing:
            return existing

        law_code = LawCode(
            code=payload.law_code,
            title=payload.law_title,
            jurisdiction=payload.jurisdiction,
            canton_code=payload.canton_code,
        )
        self._db.add(law_code)
        self._db.flush()
        return law_code

    def _get_or_create_provision(
        self, law_code: LawCode, payload: LawProvisionPayload
    ) -> LawProvision:
        existing = (
            self._db.query(LawProvision)
            .filter(
                LawProvision.law_code_id == law_code.id,
                LawProvision.ref == payload.ref,
            )
            .first()
        )
        if existing:
            return existing

        provision = LawProvision(
            law_code_id=law_code.id,
            ref=payload.ref,
            article_number=payload.article_number,
            title=payload.article_title,
        )
        self._db.add(provision)
        self._db.flush()
        return provision

    def _supersede_current_version(
        self, provision_id: int, new_valid_from: date
    ) -> None:
        current = self.get_current_version(provision_id)
        if current is None:
            return
        if current.valid_from >= new_valid_from:
            return
        current.valid_to = new_valid_from

    @staticmethod
    def _blob_path(payload: LawProvisionPayload) -> str:
        if payload.jurisdiction == LawJurisdiction.FEDERAL.value:
            prefix = f"laws/federal/{payload.law_code.lower()}/{payload.ref}"
        else:
            canton = (payload.canton_code or "unknown").lower()
            prefix = f"laws/cantonal/{canton}/{payload.law_code.lower()}/{payload.ref}"
        return f"{prefix}/{payload.valid_from.isoformat()}.md"
