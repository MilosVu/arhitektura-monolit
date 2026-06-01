"""Port za persistence dokumenta."""

from __future__ import annotations

from typing import Protocol

from cortex_models import Case, Document


class DocumentRepositoryPort(Protocol):
    def get_case_for_owner(self, case_id: int, owner_id: int) -> Case | None: ...

    def get_owned_document(
        self, document_id: int, owner_id: int
    ) -> Document | None: ...

    def get_by_id(self, document_id: int) -> Document | None: ...

    def list_by_case(self, case_id: int) -> list[Document]: ...

    def save(self, entity: Document) -> Document: ...

    def delete(self, entity: Document) -> None: ...
