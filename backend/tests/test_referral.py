"""Tests for referral portal API endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


# Public endpoints — should return 200
def test_get_technologies_public(client):
    response = client.get("/api/v1/referral/technologies")
    assert response.status_code == 200


def test_get_notice_periods_public(client):
    response = client.get("/api/v1/referral/notice-periods")
    assert response.status_code == 200


def test_get_locations_public(client):
    response = client.get("/api/v1/referral/locations")
    assert response.status_code == 200


def test_submit_referral_missing_fields(client):
    response = client.post("/api/v1/referral/submit", json={})
    assert response.status_code == 422  # validation error


def test_submit_referral_valid(client):
    response = client.post("/api/v1/referral/submit", json={
        "candidate_name": "Test Candidate",
        "email": "testcandidate@example.com",
    })
    # Accept 201 (created) or 409 (duplicate) in test environments
    assert response.status_code in (201, 409)


# Protected endpoints
def test_list_referral_candidates_unauthenticated(client):
    response = client.get("/api/v1/referral/candidates")
    assert response.status_code in (401, 403)


def test_referral_reports_by_bu_unauthenticated(client):
    response = client.get("/api/v1/referral/reports/by-bu")
    assert response.status_code in (401, 403)
