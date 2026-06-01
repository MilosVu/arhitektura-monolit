"""Šablon unit testa — DocumentService sa in-memory portom (bez Docker/Postgres)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cortex_core.enums import DocumentStatus
from cortex_models import Case, Document
from module_documents.services.document_service import DocumentService


@dataclass
class FakeDocumentRepository:
    """Minimalna in-memory implementacija DocumentRepositoryPort."""

    cases: dict[int, Case] = field(default_factory=dict)
    documents: dict[int, Document] = field(default_factory=dict)
    _next_id: int = 1

    def get_case_for_owner(self, case_id: int, owner_id: int) -> Case | None:
        case = self.cases.get(case_id)
        if case and case.owner_id == owner_id:
            return case
        return None

    def get_owned_document(self, document_id: int, owner_id: int) -> Document | None:
        doc = self.documents.get(document_id)
        if not doc:
            return None
        case = self.cases.get(doc.case_id)
        if case and case.owner_id == owner_id:
            return doc
        return None

    def get_by_id(self, document_id: int) -> Document | None:
        return self.documents.get(document_id)

    def list_by_case(self, case_id: int) -> list[Document]:
        return [d for d in self.documents.values() if d.case_id == case_id]

    def save(self, entity: Document) -> Document:
        if entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        self.documents[entity.id] = entity
        return entity

    def delete(self, entity: Document) -> None:
        if entity.id is not None:
            self.documents.pop(entity.id, None)


class _FakeSession:
    """Placeholder — repo ne koristi session u fake implementaciji."""


def test_mark_syncing_updates_status() -> None:
    repo = FakeDocumentRepository()
    case = Case(id=1, case_number="C-1", title="Test", owner_id=10)
    repo.cases[1] = case
    doc = Document(
        id=1,
        case_id=1,
        filename="a.pdf",
        status=DocumentStatus.PENDING.value,
    )
    repo.documents[1] = doc

    service = DocumentService(repo_factory=lambda _db: repo)
    session: Any = _FakeSession()

    service.mark_syncing(1, session)

    assert repo.documents[1].status == DocumentStatus.SYNCING.value
