from cortex_core.base.repository import BaseRepository
from module_platform.models import Document


class DocumentRepository(BaseRepository[Document]):
    def get_by_id(self, entity_id: int) -> Document | None:
        return self.session.query(Document).filter(Document.id == entity_id).first()

    def save(self, entity: Document) -> Document:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def list_by_case(self, case_id: int) -> list[Document]:
        return (
            self.session.query(Document)
            .filter(Document.case_id == case_id)
            .order_by(Document.created_at.desc())
            .all()
        )
