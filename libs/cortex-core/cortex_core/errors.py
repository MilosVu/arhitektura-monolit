"""Domen greške — dele se između svih modula."""

from __future__ import annotations


class CortexError(Exception):
    """Korenska greška platforme."""


class NotFoundError(CortexError):
    """Traženi resurs ne postoji."""


class ValidationError(CortexError):
    """Ulaz nije prošao domensku validaciju."""


class ConflictError(CortexError):
    """Zahtev je u konfliktu sa trenutnim stanjem resursa."""


class ServiceNotRegisteredError(CortexError):
    """Traženi servis nije registrovan u registry-ju."""


class ConfigurationError(CortexError):
    """Obavezna konfiguracija ili port nije podešen."""


class NotAuthenticatedError(CortexError):
    """Nedostaju ili su nevažeći kredencijali (HTTP 401)."""

    def __init__(self, message: str, *, code: str = "not_authenticated") -> None:
        super().__init__(message)
        self.code = code


class ForbiddenError(CortexError):
    """Autentifikovani korisnik nema pristup resursu (HTTP 403)."""

    def __init__(self, message: str, *, code: str = "forbidden") -> None:
        super().__init__(message)
        self.code = code


class DocumentNotFoundError(NotFoundError):
    """Dokument ne postoji ili nije vidljiv korisniku."""


class SyncJobNotFoundError(NotFoundError):
    """Sync job ne postoji."""
