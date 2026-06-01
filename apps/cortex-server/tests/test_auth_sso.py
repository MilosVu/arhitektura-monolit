"""SSO stub auth smoke test."""

import pytest


def test_sso_url(client) -> None:
    response = client.get("/auth/sso/url")
    assert response.status_code == 200
    data = response.json()
    assert "authorize_url" in data
    assert "state" in data


@pytest.mark.integration
def test_sso_callback_stub(client) -> None:
    """Zahteva PostgreSQL sa seed korisnicima (make infra-up)."""
    response = client.post(
        "/auth/sso/callback",
        json={"code": "stub-hmueller"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["user"]["ad_username"] == "hmueller"
