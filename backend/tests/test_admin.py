"""Tests for admin API endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


def test_get_towers_unauthenticated(client):
    response = client.get("/api/v1/admin/towers")
    assert response.status_code in (401, 403)


def test_get_skills_unauthenticated(client):
    response = client.get("/api/v1/admin/skills")
    assert response.status_code in (401, 403)


def test_get_sources_unauthenticated(client):
    response = client.get("/api/v1/admin/sources")
    assert response.status_code in (401, 403)


def test_get_approver_dl_unauthenticated(client):
    response = client.get("/api/v1/admin/approver-dl")
    assert response.status_code in (401, 403)


def test_create_tower_unauthenticated(client):
    response = client.post("/api/v1/admin/towers", json={"tower_name": "Test"})
    assert response.status_code in (401, 403)
