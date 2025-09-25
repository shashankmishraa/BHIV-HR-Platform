#!/usr/bin/env python3
"""
BHIV HR Platform - End-to-End Workflow Testing
Comprehensive multi-service workflow validation covering complete user journeys
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import time
import uuid

import requests


class E2ETestConfig:
    """Configuration for end-to-end tests"""

    API_BASE = "http://localhost:8000"
    AI_BASE = "http://localhost:9000"
    PORTAL_BASE = "http://localhost:8501"
    CLIENT_PORTAL_BASE = "http://localhost:8502"

    API_KEY = "myverysecureapikey123"
    HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    REQUEST_TIMEOUT = 10
    WORKFLOW_TIMEOUT = 30
    CLEANUP_ENABLED = True


class WorkflowTestData:
    """Test data factory for E2E workflows"""

    @staticmethod
    def create_test_job(client_id: int = 1, suffix: str = None) -> Dict[str, Any]:
        unique_id = suffix or str(uuid.uuid4())[:8]
        return {
            "title": f"E2E Test Python Developer {unique_id}",
            "description": f"End-to-end test job for workflow validation {unique_id}",
            "client_id": client_id,
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Senior",
            "employment_type": "Full-time",
            "requirements": "Python, FastAPI, PostgreSQL, Docker, AWS",
            "status": "active",
        }

    @staticmethod
    def create_test_candidates(job_id: int, count: int = 3) -> List[Dict[str, Any]]:
        candidates = []
        for i in range(count):
            unique_id = str(uuid.uuid4())[:8]
            candidates.append(
                {
                    "name": f"E2E Test Candidate {i+1} {unique_id}",
                    "email": f"e2e.candidate{i+1}.{unique_id}@testdomain.com",
                    "phone": f"+1-555-010{i+1}",
                    "location": "Remote" if i % 2 == 0 else "New York",
                    "experience_years": 3 + i,
                    "technical_skills": f"Python, FastAPI, PostgreSQL, Docker{', AWS' if i > 0 else ''}",
                    "seniority_level": "Senior" if i == 0 else "Mid-level",
                    "education_level": "Masters" if i == 0 else "Bachelors",
                    "job_id": job_id,
                    "status": "applied",
                }
            )
        return candidates


class E2EWorkflowTester:
    """End-to-end workflow testing framework"""

    def __init__(self):
        self.config = E2ETestConfig()
        self.created_resources = {
            "jobs": [],
            "candidates": [],
            "interviews": [],
            "offers": [],
            "feedback": [],
        }
        self.test_results = {}

    def cleanup_resources(self):
        if not self.config.CLEANUP_ENABLED:
            return
        print("\nCleaning up test resources...")

    def verify_service_health(self) -> bool:
        print("Verifying service health...")

        services = [
            ("API Gateway", f"{self.config.API_BASE}/health"),
            ("AI Agent", f"{self.config.AI_BASE}/health"),
        ]

        all_healthy = True
        for service_name, health_url in services:
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"   + {service_name}: Healthy")
                else:
                    print(f"   - {service_name}: Unhealthy ({response.status_code})")
                    all_healthy = False
            except Exception as e:
                print(f"   - {service_name}: Failed - {str(e)}")
                all_healthy = False

        return all_healthy

    def test_complete_hiring_workflow(self) -> bool:
        print("\n" + "=" * 60)
        print("COMPLETE HIRING WORKFLOW TEST")
        print("=" * 60)

        try:
            # Step 1: Create job position
            print("\nStep 1: Creating job position...")
            job_data = WorkflowTestData.create_test_job()

            response = requests.post(
                f"{self.config.API_BASE}/v1/jobs",
                headers=self.config.HEADERS,
                json=job_data,
                timeout=self.config.REQUEST_TIMEOUT,
            )

            if response.status_code != 200:
                print(f"   - Job creation failed: {response.status_code}")
                return False

            job_result = response.json()
            job_id = job_result.get("job_id")
            self.created_resources["jobs"].append(job_id)
            print(f"   + Job created: ID {job_id}")

            # Step 2: Upload candidates
            print("\nStep 2: Uploading candidates...")
            candidates_data = WorkflowTestData.create_test_candidates(job_id, 3)

            response = requests.post(
                f"{self.config.API_BASE}/v1/candidates/bulk",
                headers=self.config.HEADERS,
                json={"candidates": candidates_data},
                timeout=self.config.REQUEST_TIMEOUT,
            )

            if response.status_code != 200:
                print(f"   - Candidate upload failed: {response.status_code}")
                return False

            candidates_result = response.json()
            candidate_ids = candidates_result.get("candidate_ids", [])
            self.created_resources["candidates"].extend(candidate_ids)
            print(f"   + Candidates uploaded: {len(candidate_ids)} candidates")

            # Step 3: AI matching and scoring
            print("\nStep 3: AI matching and scoring...")

            response = requests.get(
                f"{self.config.API_BASE}/v1/match/{job_id}/top",
                headers=self.config.HEADERS,
                timeout=15,
            )

            if response.status_code != 200:
                print(f"   - AI matching failed: {response.status_code}")
                return False

            matching_result = response.json()
            top_candidates = matching_result.get("top_candidates", [])
            print(
                f"   + AI matching completed: {len(top_candidates)} candidates scored"
            )

            if not top_candidates:
                print("   ! No candidates returned from AI matching")
                return False

            best_candidate = top_candidates[0]
            best_candidate_id = best_candidate.get("candidate_id")
            print(
                f"   * Best match: Candidate {best_candidate_id} (Score: {best_candidate.get('score', 0):.1f})"
            )

            return True

        except Exception as e:
            print(f"   - Workflow failed: {str(e)}")
            return False

    def run_all_workflows(self) -> Dict[str, bool]:
        print("STARTING END-TO-END WORKFLOW TESTING")
        print("=" * 60)

        if not self.verify_service_health():
            print("- Services not healthy - aborting workflow tests")
            return {}

        workflows = [
            ("Complete Hiring Workflow", self.test_complete_hiring_workflow),
        ]

        results = {}

        for workflow_name, workflow_func in workflows:
            print(f"\nRunning: {workflow_name}")
            try:
                start_time = time.time()
                result = workflow_func()
                execution_time = time.time() - start_time

                results[workflow_name] = result
                status = "PASSED" if result else "FAILED"
                print(f"   {status} in {execution_time:.2f}s")

            except Exception as e:
                results[workflow_name] = False
                print(f"   FAILED - {str(e)}")

        self.cleanup_resources()
        self.print_workflow_summary(results)

        return results

    def print_workflow_summary(self, results: Dict[str, bool]):
        print("\n" + "=" * 60)
        print("END-TO-END WORKFLOW TEST SUMMARY")
        print("=" * 60)

        passed = sum(1 for result in results.values() if result)
        total = len(results)

        for workflow_name, result in results.items():
            status = "PASSED" if result else "FAILED"
            print(f"   {workflow_name:<30}: {status}")

        print(f"\nOverall Results: {passed}/{total} workflows passed")

        if passed == total:
            print("ALL END-TO-END WORKFLOWS PASSED!")
        else:
            print("SOME WORKFLOWS FAILED")


def main():
    tester = E2EWorkflowTester()
    results = tester.run_all_workflows()

    all_passed = all(results.values()) if results else False
    return 0 if all_passed else 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
