"""Pytest fixtures za cortex-server."""

import os

import pytest

os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://cortex:cortex@localhost:5432/cortex"
)
os.environ.setdefault("JWT_SECRET", "test-secret-key-for-pytest-only")
os.environ.setdefault("CELERY_BROKER_URL", "memory://")
os.environ.setdefault("CELERY_RESULT_BACKEND", "cache+memory://")


@pytest.fixture
def client():
    from cortex_server.main import app
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client
