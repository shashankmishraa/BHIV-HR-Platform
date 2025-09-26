"""Advanced tests for Gateway service - Full API coverage."""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client."""
    from services.gateway.app.main import app

    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Mock authentication headers."""
    return {"Authorization": "Bearer test-api-key-for-ci"}


class TestCoreEndpoints:
    """Test core API endpoints."""

    def test_health_endpoint(self, client):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_docs_endpoint(self, client):
        """Test API documentation."""
        response = client.get("/docs")
        assert response.status_code == 200


class TestJobEndpoints:
    """Test job management endpoints."""

    def test_create_job(self, client, auth_headers):
        """Test job creation."""
        job_data = {
            "title": "Software Engineer",
            "description": "Develop amazing software applications",
            "requirements": "Python, FastAPI, PostgreSQL",
            "location": "San Francisco, CA",
            "department": "Engineering",
            "experience_level": "Mid-level",
            "salary_min": 80000,
            "salary_max": 120000,
            "job_type": "Full-time",
        }

        with patch("services.gateway.app.shared.database.get_db_connection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = (1,)
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_db.return_value.__enter__.return_value = mock_conn

            response = client.post("/v1/jobs", json=job_data, headers=auth_headers)
            assert response.status_code in [200, 201]

    def test_get_jobs(self, client, auth_headers):
        """Test job retrieval."""
        with patch("services.gateway.app.shared.database.get_db_connection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = []
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_db.return_value.__enter__.return_value = mock_conn

            response = client.get("/v1/jobs", headers=auth_headers)
            assert response.status_code == 200


class TestCandidateEndpoints:
    """Test candidate management endpoints."""

    def test_candidate_search(self, client, auth_headers):
        """Test candidate search."""
        with patch("services.gateway.app.shared.database.get_db_connection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = []
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_db.return_value.__enter__.return_value = mock_conn

            response = client.get("/v1/candidates/search", headers=auth_headers)
            assert response.status_code == 200


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_token_validation(self, client):
        """Test token validation."""
        response = client.post("/v1/auth/validate", json={"token": "test-token"})
        assert response.status_code in [200, 401, 422]


class TestMatchingEndpoints:
    """Test AI matching endpoints."""

    def test_job_matching(self, client, auth_headers):
        """Test job matching."""
        with patch("services.gateway.app.shared.database.get_db_connection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = []
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_db.return_value.__enter__.return_value = mock_conn

            response = client.get("/v1/match/1/top", headers=auth_headers)
            assert response.status_code in [200, 404]


class TestMonitoringEndpoints:
    """Test monitoring endpoints."""

    def test_health_detailed(self, client, auth_headers):
        """Test detailed health check."""
        response = client.get("/health/detailed", headers=auth_headers)
        assert response.status_code in [200, 404]

    def test_metrics(self, client, auth_headers):
        """Test metrics endpoint."""
        response = client.get("/metrics", headers=auth_headers)
        assert response.status_code in [200, 404]
