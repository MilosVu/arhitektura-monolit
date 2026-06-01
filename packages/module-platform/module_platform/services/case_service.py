"""Case management — lista slučajeva filtrirana po AD ownership-u."""

from cortex_core.base.service import BaseService
from cortex_core.domain.exceptions import ForbiddenError
from cortex_models import Case, Document, User
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from module_platform.schemas import CaseDetail, CaseSummary, UserResponse


class CaseService(BaseService):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user: User) -> list[CaseSummary]:
        cases = self._db.query(Case).filter(Case.owner_id == user.id).all()
        result: list[CaseSummary] = []
        for case in cases:
            doc_count = (
                self._db.query(func.count(Document.id))
                .filter(Document.case_id == case.id)
                .scalar()
                or 0
            )
            summary = CaseSummary.model_validate(case)
            summary.document_count = doc_count
            result.append(summary)
        return result

    def get_detail(self, case_id: int, user: User) -> CaseDetail:
        case = (
            self._db.query(Case)
            .options(joinedload(Case.owner))
            .filter(Case.id == case_id, Case.owner_id == user.id)
            .first()
        )
        if not case:
            raise ForbiddenError(f"Case {case_id} not accessible for user {user.id}")
        return CaseDetail(
            id=case.id,
            case_number=case.case_number,
            title=case.title,
            description=case.description,
            owner=UserResponse.model_validate(case.owner),
            last_synced_at=case.last_synced_at,
            created_at=case.created_at,
        )

    def assert_case_access(self, case_id: int, user: User) -> Case:
        case = (
            self._db.query(Case)
            .filter(Case.id == case_id, Case.owner_id == user.id)
            .first()
        )
        if not case:
            raise ForbiddenError(f"Case {case_id} not accessible")
        return case
