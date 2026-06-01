from cortex_core.errors import ForbiddenError, NotFoundError


def test_forbidden_error_code() -> None:
    exc = ForbiddenError("denied")
    assert exc.code == "forbidden"


def test_not_found_is_cortex_error() -> None:
    exc = NotFoundError("missing")
    assert str(exc) == "missing"
