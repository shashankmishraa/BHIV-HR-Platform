"""Basic tests for Gateway service."""
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint():
    """Test health endpoint."""
    from services.gateway.app.main import app
    
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_docs_endpoint():
    """Test API documentation endpoint."""
    from services.gateway.app.main import app
    
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200