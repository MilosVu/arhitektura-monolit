from cortex_core.base.repository import BaseRepository
from module_platform.models import Case


class CaseRepository(BaseRepository[Case]):
    def get_by_id(self, entity_id: int) -> Case | None:
        return self.session.query(Case).filter(Case.id == entity_id).first()

    def save(self, entity: Case) -> Case:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def list_by_owner(self, owner_id: int) -> list[Case]:
        return self.session.query(Case).filter(Case.owner_id == owner_id).all()
