"""Domen greške — dele se između svih servisa."""


class CortexError(Exception):
    """Korenska greška platforme."""


class ForbiddenError(CortexError):
    """Korisnik nema pristup resursu (case ownership / AD role)."""


class DocumentNotFoundError(CortexError):
    """Dokument ne postoji ili nije vidljiv korisniku."""


class SyncJobNotFoundError(CortexError):
    """Sync job ne postoji."""
