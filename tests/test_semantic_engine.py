#!/usr/bin/env python3
"""
Comprehensive test suite for semantic engine functionality
Tests all components and verifies proper integration
"""

from pathlib import Path
import json
import os
import sys
import time

import unittest

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from services.semantic_engine import (
        SemanticJobMatcher,
        AdvancedSemanticMatcher,
        BatchMatcher,
        SemanticProcessor,
        ModelManager,
    )

    SEMANTIC_AVAILABLE = True
except ImportError as e:
    print(f"Semantic engine not available: {e}")
    SEMANTIC_AVAILABLE = False


class TestSemanticEngine(unittest.TestCase):
    """Test semantic engine components"""

    def setUp(self):
        """Set up test fixtures"""
        if not SEMANTIC_AVAILABLE:
            self.skipTest("Semantic engine not available")

        self.job_matcher = SemanticJobMatcher()
        self.advanced_matcher = AdvancedSemanticMatcher()
        self.batch_matcher = BatchMatcher(max_workers=2)
        self.semantic_processor = SemanticProcessor()
        self.model_manager = ModelManager()

        # Test data
        self.sample_job = {
            "id": 1,
            "title": "Senior Python Developer",
            "description": "We are looking for an experienced Python developer with Django and React skills",
            "requirements": "Python, Django, React, SQL, 5+ years experience",
            "department": "Engineering",
            "location": "Mumbai",
            "experience_level": "Senior",
        }

        self.sample_candidate = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "technical_skills": "Python, Django, React, JavaScript, SQL, Git",
            "experience_years": 6,
            "seniority_level": "Senior Software Engineer",
            "education_level": "Masters in Computer Science",
            "location": "Mumbai",
        }

    def test_model_manager_initialization(self):
        """Test model manager initialization"""
        self.assertIsNotNone(self.model_manager)
        self.assertEqual(self.model_manager.version, "2.1.0")

        # Test skill embeddings
        self.assertGreater(len(self.model_manager.skill_embeddings), 0)

        # Test job templates
        self.assertGreater(len(self.model_manager.job_templates), 0)

        # Test model stats
        stats = self.model_manager.get_model_stats()
        self.assertIn("skill_embeddings_count", stats)
        self.assertIn("job_templates_count", stats)
        self.assertGreater(stats["skill_embeddings_count"], 0)

        print(
            f"Model Manager: {stats['skill_embeddings_count']} skills, {stats['job_templates_count']} templates"
        )

    def test_semantic_job_matcher(self):
        """Test basic semantic job matcher"""
        job_requirements = "Python Django React SQL experience"
        candidate_skills = "Python Django React JavaScript SQL Git"

        result = self.job_matcher.match(job_requirements, candidate_skills, "Senior", 5)

        self.assertIsInstance(result, dict)
        self.assertIn("overall_score", result)
        self.assertIn("skill_score", result)
        self.assertIn("matched_skills", result)

        # Score should be reasonable
        self.assertGreaterEqual(result["overall_score"], 0.0)
        self.assertLessEqual(result["overall_score"], 1.0)

        # Should have matched skills
        self.assertGreater(len(result["matched_skills"]), 0)

        print(
            f"Semantic Matcher: Score {result['overall_score']:.3f}, Skills: {result['matched_skills']}"
        )

    def test_advanced_semantic_matcher(self):
        """Test advanced semantic matcher with bias mitigation"""
        result = self.advanced_matcher.advanced_match(
            self.sample_job, self.sample_candidate
        )

        self.assertIsInstance(result, dict)
        self.assertIn("score", result)
        self.assertIn("reasoning", result)
        self.assertIn("bias_adjusted", result)
        self.assertIn("advanced_factors", result)

        # Score should be in 0-100 range
        self.assertGreaterEqual(result["score"], 0.0)
        self.assertLessEqual(result["score"], 100.0)

        # Should have bias adjustment
        self.assertTrue(result["bias_adjusted"])

        # Should have advanced factors
        advanced_factors = result["advanced_factors"]
        self.assertIn("cultural_fit", advanced_factors)
        self.assertIn("growth_potential", advanced_factors)

        print(
            f"Advanced Matcher: Score {result['score']}, Bias Adjusted: {result['bias_adjusted']}"
        )


def run_semantic_engine_tests():
    """Run all semantic engine tests"""
    print("\n" + "=" * 60)
    print("BHIV Semantic Engine Test Suite")
    print("=" * 60)

    if not SEMANTIC_AVAILABLE:
        print("Semantic engine not available - skipping tests")
        print("Install dependencies: pip install numpy scipy scikit-learn nltk")
        return False

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticEngine))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("All semantic engine tests passed!")
        print(f"Ran {result.testsRun} tests successfully")
    else:
        print(f"{len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        for test, error in result.failures + result.errors:
            print(f"   - {test}: {error.split(chr(10))[0]}")

    print("=" * 60)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_semantic_engine_tests()
    sys.exit(0 if success else 1)
