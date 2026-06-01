"""Postgres implementacija DocumentRepositoryPort."""

from __future__ import annotations

from cortex_models import Case, Document
from sqlalchemy.orm import Session


class PostgresDocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_case_for_owner(self, case_id: int, owner_id: int) -> Case | None:
        return (
            self._session.query(Case)
            .filter(Case.id == case_id, Case.owner_id == owner_id)
            .first()
        )

    def get_owned_document(self, document_id: int, owner_id: int) -> Document | None:
        return (
            self._session.query(Document)
            .join(Case)
            .filter(Document.id == document_id, Case.owner_id == owner_id)
            .first()
        )

    def get_by_id(self, document_id: int) -> Document | None:
        return self._session.query(Document).filter(Document.id == document_id).first()

    def list_by_case(self, case_id: int) -> list[Document]:
        return (
            self._session.query(Document)
            .filter(Document.case_id == case_id)
            .order_by(Document.created_at.desc())
            .all()
        )

    def save(self, entity: Document) -> Document:
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity

    def delete(self, entity: Document) -> None:
        self._session.delete(entity)
        self._session.commit()
