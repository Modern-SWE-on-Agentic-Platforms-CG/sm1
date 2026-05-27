"""Tests for analytics API endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


def test_analytics_summary_unauthenticated(client):
    response = client.get("/api/v1/reports/analytics/summary")
    assert response.status_code in (401, 403)


def test_status_pie_unauthenticated(client):
    response = client.get("/api/v1/reports/analytics/status-pie")
    assert response.status_code in (401, 403)


def test_arc_deviations_unauthenticated(client):
    response = client.get("/api/v1/reports/analytics/arc-deviations")
    assert response.status_code in (401, 403)


def test_rejection_reasons_unauthenticated(client):
    response = client.get("/api/v1/reports/analytics/rejection-reasons")
    assert response.status_code in (401, 403)


def test_interview_data_unauthenticated(client):
    response = client.get("/api/v1/reports/analytics/interview-data")
    assert response.status_code in (401, 403)
