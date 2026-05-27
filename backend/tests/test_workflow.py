"""Tests for workflow API endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


def test_get_workflow_candidates_unauthenticated(client):
    response = client.get("/api/v1/workflow/candidates")
    assert response.status_code in (401, 403)


def test_get_workflow_possible_status_unauthenticated(client):
    response = client.get("/api/v1/workflow/possible-status")
    assert response.status_code in (401, 403)


def test_get_threshold_unauthenticated(client):
    response = client.get("/api/v1/workflow/threshold")
    assert response.status_code in (401, 403)


def test_workflow_action_invalid_id_unauthenticated(client):
    response = client.post("/api/v1/workflow/99999/action", json={"action": "Approve"})
    assert response.status_code in (401, 403)
