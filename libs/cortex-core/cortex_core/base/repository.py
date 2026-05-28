"""Repository abstrakcija — pristup PostgreSQL entitetima."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Bazna klasa za persistence sloj (api-gateway, workeri)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    @property
    def session(self) -> Session:
        return self._session

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T | None:
        """Učitaj entitet po primarnom ključu."""

    @abstractmethod
    def save(self, entity: T) -> T:
        """Persistuj entitet (insert/update)."""

    def flush(self) -> None:
        self._session.flush()
