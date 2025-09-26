"""Advanced tests for AI Agent service - Full AI functionality."""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client."""
    from services.agent.app import app

    return TestClient(app)


class TestAIMatchingCore:
    """Test core AI matching functionality."""

    def test_health_endpoint(self, client):
        """Test agent health."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_match_endpoint(self, client):
        """Test AI matching endpoint."""
        match_data = {"job_id": 1}

        with patch(
            "services.agent.semantic_engine.advanced_matcher.AdvancedMatcher"
        ) as mock_matcher:
            mock_instance = MagicMock()
            mock_instance.match_candidates_for_job.return_value = {
                "top_candidates": [],
                "algorithm_version": "v3.2.0",
                "processing_time": 0.1,
            }
            mock_matcher.return_value = mock_instance

            response = client.post("/match", json=match_data)
            assert response.status_code in [200, 422]

    def test_analytics_endpoint(self, client):
        """Test analytics endpoint."""
        response = client.get("/analytics")
        assert response.status_code in [200, 404]


class TestSemanticEngine:
    """Test semantic matching engine."""

    def test_model_loading(self):
        """Test model manager initialization."""
        from services.agent.semantic_engine.model_manager import ModelManager

        manager = ModelManager()
        assert manager.version == "2.1.0"
        assert isinstance(manager.skill_embeddings, dict)
        assert isinstance(manager.job_templates, dict)

    def test_skill_similarity(self):
        """Test skill similarity calculation."""
        from services.agent.semantic_engine.model_manager import ModelManager

        manager = ModelManager()
        similarity = manager.calculate_skill_similarity("python", "java")
        assert 0.0 <= similarity <= 1.0

    def test_job_template_matching(self):
        """Test job template retrieval."""
        from services.agent.semantic_engine.model_manager import ModelManager

        manager = ModelManager()
        template = manager.get_job_template("software engineer")
        assert template is not None
        assert "required_skills" in template


class TestAdvancedMatching:
    """Test advanced matching algorithms."""

    @patch("services.agent.semantic_engine.advanced_matcher.get_db_connection")
    def test_candidate_scoring(self, mock_db):
        """Test candidate scoring algorithm."""
        from services.agent.semantic_engine.advanced_matcher import AdvancedMatcher

        # Mock database
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_db.return_value.__enter__.return_value = mock_conn

        matcher = AdvancedMatcher()
        result = matcher.match_candidates_for_job(1)

        assert "top_candidates" in result
        assert "algorithm_version" in result
        assert "processing_time" in result
