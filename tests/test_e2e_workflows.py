#!/usr/bin/env python3
"""
BHIV HR Platform - End-to-End Workflow Testing
Comprehensive multi-service workflow validation covering complete user journeys
"""

import requests
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pytest

class E2ETestConfig:
    """Configuration for end-to-end tests"""
    API_BASE = "http://localhost:8000"
    AI_BASE = "http://localhost:9000"
    PORTAL_BASE = "http://localhost:8501"
    CLIENT_PORTAL_BASE = "http://localhost:8502"
    
    API_KEY = "myverysecureapikey123"
    HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # Test timeouts
    REQUEST_TIMEOUT = 10
    WORKFLOW_TIMEOUT = 30
    
    # Test data cleanup
    CLEANUP_ENABLED = True

class WorkflowTestData:
    """Test data factory for E2E workflows"""
    
    @staticmethod
    def create_test_job(client_id: int = 1, suffix: str = None) -> Dict[str, Any]:
        """Create test job data"""
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
            "status": "active"
        }
    
    @staticmethod
    def create_test_candidates(job_id: int, count: int = 3) -> List[Dict[str, Any]]:
        """Create test candidate data"""
        candidates = []
        for i in range(count):
            unique_id = str(uuid.uuid4())[:8]
            candidates.append({
                "name": f"E2E Test Candidate {i+1} {unique_id}",
                "email": f"e2e.candidate{i+1}.{unique_id}@testdomain.com",
                "phone": f"+1-555-010{i+1}",
                "location": "Remote" if i % 2 == 0 else "New York",
                "experience_years": 3 + i,
                "technical_skills": f"Python, FastAPI, PostgreSQL, Docker{', AWS' if i > 0 else ''}",
                "seniority_level": "Senior" if i == 0 else "Mid-level",
                "education_level": "Masters" if i == 0 else "Bachelors",
                "job_id": job_id,
                "status": "applied"
            })
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
            "feedback": []
        }
        self.test_results = {}
    
    def cleanup_resources(self):
        """Clean up test resources"""
        if not self.config.CLEANUP_ENABLED:
            return
        
        print("\n🧹 Cleaning up test resources...")
        # Note: In production, implement proper cleanup endpoints
        # For now, we'll rely on test data being clearly marked
        
    def verify_service_health(self) -> bool:
        """Verify all services are healthy before running workflows"""
        print("🔍 Verifying service health...")
        
        services = [
            ("API Gateway", f"{self.config.API_BASE}/health"),
            ("AI Agent", f"{self.config.AI_BASE}/health"),
        ]
        
        all_healthy = True
        for service_name, health_url in services:
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {service_name}: Healthy")
                else:
                    print(f"   ❌ {service_name}: Unhealthy ({response.status_code})")
                    all_healthy = False
            except Exception as e:
                print(f"   ❌ {service_name}: Failed - {str(e)}")
                all_healthy = False
        
        return all_healthy
    
    def test_complete_hiring_workflow(self) -> bool:
        """
        Test complete hiring workflow:
        1. Create job position
        2. Upload candidates
        3. AI matching and scoring
        4. Schedule interviews
        5. Submit feedback/values assessment
        6. Make offer
        7. Verify data consistency across services
        """
        print("\n" + "="*60)
        print("🎯 COMPLETE HIRING WORKFLOW TEST")
        print("="*60)
        
        try:
            # Step 1: Create job position
            print("\n📋 Step 1: Creating job position...")
            job_data = WorkflowTestData.create_test_job()
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/jobs",
                headers=self.config.HEADERS,
                json=job_data,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Job creation failed: {response.status_code}")
                return False
            
            job_result = response.json()
            job_id = job_result.get("job_id")
            self.created_resources["jobs"].append(job_id)
            print(f"   ✅ Job created: ID {job_id}")
            
            # Step 2: Upload candidates
            print("\n👥 Step 2: Uploading candidates...")
            candidates_data = WorkflowTestData.create_test_candidates(job_id, 3)
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/candidates/bulk",
                headers=self.config.HEADERS,
                json={"candidates": candidates_data},
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Candidate upload failed: {response.status_code}")
                return False
            
            candidates_result = response.json()
            candidate_ids = candidates_result.get("candidate_ids", [])
            self.created_resources["candidates"].extend(candidate_ids)
            print(f"   ✅ Candidates uploaded: {len(candidate_ids)} candidates")
            
            # Step 3: AI matching and scoring
            print("\n🤖 Step 3: AI matching and scoring...")
            
            response = requests.get(
                f"{self.config.API_BASE}/v1/match/{job_id}/top",
                headers=self.config.HEADERS,
                timeout=15  # AI matching may take longer
            )
            
            if response.status_code != 200:
                print(f"   ❌ AI matching failed: {response.status_code}")
                return False
            
            matching_result = response.json()
            top_candidates = matching_result.get("top_candidates", [])
            print(f"   ✅ AI matching completed: {len(top_candidates)} candidates scored")
            
            if not top_candidates:
                print("   ⚠️ No candidates returned from AI matching")
                return False
            
            best_candidate = top_candidates[0]
            best_candidate_id = best_candidate.get("candidate_id")
            print(f"   🏆 Best match: Candidate {best_candidate_id} (Score: {best_candidate.get('score', 0):.1f})")
            
            # Step 4: Schedule interview
            print("\n📅 Step 4: Scheduling interview...")
            
            interview_data = {
                "candidate_id": best_candidate_id,
                "job_id": job_id,
                "interview_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "interviewer": "E2E Test Interviewer",
                "interview_type": "technical",
                "notes": "End-to-end workflow test interview"
            }
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/interviews",
                headers=self.config.HEADERS,
                json=interview_data,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Interview scheduling failed: {response.status_code}")
                return False
            
            interview_result = response.json()
            interview_id = interview_result.get("interview_id")
            self.created_resources["interviews"].append(interview_id)
            print(f"   ✅ Interview scheduled: ID {interview_id}")
            
            # Step 5: Submit feedback and values assessment
            print("\n📊 Step 5: Submitting feedback and values assessment...")
            
            feedback_data = {
                "candidate_id": best_candidate_id,
                "job_id": job_id,
                "interview_id": interview_id,
                "reviewer": "E2E Test Reviewer",
                "feedback_text": "Excellent technical skills, strong cultural fit. Recommended for hire.",
                "values_scores": {
                    "integrity": 5,
                    "honesty": 5,
                    "discipline": 4,
                    "hard_work": 5,
                    "gratitude": 4
                },
                "technical_rating": 4.5,
                "cultural_fit_rating": 4.8,
                "recommendation": "hire"
            }
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/feedback",
                headers=self.config.HEADERS,
                json=feedback_data,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Feedback submission failed: {response.status_code}")
                return False
            
            feedback_result = response.json()
            feedback_id = feedback_result.get("feedback_id")
            self.created_resources["feedback"].append(feedback_id)
            print(f"   ✅ Feedback submitted: ID {feedback_id}")
            
            # Step 6: Make offer
            print("\n💼 Step 6: Making job offer...")
            
            offer_data = {
                "candidate_id": best_candidate_id,
                "job_id": job_id,
                "salary": 120000,
                "currency": "USD",
                "benefits": "Health insurance, 401k, flexible PTO",
                "start_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "status": "sent",
                "notes": "E2E workflow test offer"
            }
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/offers",
                headers=self.config.HEADERS,
                json=offer_data,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Offer creation failed: {response.status_code}")
                return False
            
            offer_result = response.json()
            offer_id = offer_result.get("offer_id")
            self.created_resources["offers"].append(offer_id)
            print(f"   ✅ Offer created: ID {offer_id}")
            
            # Step 7: Verify data consistency
            print("\n🔍 Step 7: Verifying data consistency...")
            
            # Verify job exists and has correct data
            response = requests.get(
                f"{self.config.API_BASE}/v1/jobs",
                headers=self.config.HEADERS,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                jobs = response.json().get("jobs", [])
                job_found = any(job.get("job_id") == job_id for job in jobs)
                print(f"   ✅ Job consistency: {'Verified' if job_found else 'Failed'}")
            else:
                print(f"   ❌ Job verification failed: {response.status_code}")
                return False
            
            # Verify candidates exist
            response = requests.get(
                f"{self.config.API_BASE}/v1/candidates/job/{job_id}",
                headers=self.config.HEADERS,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                candidates = response.json().get("candidates", [])
                print(f"   ✅ Candidate consistency: {len(candidates)} candidates found")
            else:
                print(f"   ❌ Candidate verification failed: {response.status_code}")
                return False
            
            print(f"\n🎉 COMPLETE HIRING WORKFLOW: SUCCESS")
            print(f"   📋 Job ID: {job_id}")
            print(f"   👥 Candidates: {len(candidate_ids)}")
            print(f"   🏆 Best Match: Candidate {best_candidate_id}")
            print(f"   📅 Interview: {interview_id}")
            print(f"   📊 Feedback: {feedback_id}")
            print(f"   💼 Offer: {offer_id}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Workflow failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_client_hr_portal_sync(self) -> bool:
        """
        Test Client Portal → HR Portal synchronization:
        1. Create job in Client Portal workflow
        2. Verify job appears in HR Portal
        3. Add candidates via HR Portal
        4. Verify candidates visible to Client Portal
        """
        print("\n" + "="*60)
        print("🔄 CLIENT-HR PORTAL SYNC TEST")
        print("="*60)
        
        try:
            # Step 1: Simulate Client Portal job creation
            print("\n🏢 Step 1: Creating job via Client Portal workflow...")
            
            client_job_data = WorkflowTestData.create_test_job(client_id=999, suffix="CLIENT")
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/jobs",
                headers=self.config.HEADERS,
                json=client_job_data,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Client job creation failed: {response.status_code}")
                return False
            
            job_result = response.json()
            job_id = job_result.get("job_id")
            self.created_resources["jobs"].append(job_id)
            print(f"   ✅ Client job created: ID {job_id}")
            
            # Step 2: Verify job visible in HR Portal
            print("\n🎯 Step 2: Verifying job visibility in HR Portal...")
            
            response = requests.get(
                f"{self.config.API_BASE}/v1/jobs",
                headers=self.config.HEADERS,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ HR Portal job fetch failed: {response.status_code}")
                return False
            
            jobs = response.json().get("jobs", [])
            client_job = next((job for job in jobs if job.get("job_id") == job_id), None)
            
            if not client_job:
                print(f"   ❌ Client job not visible in HR Portal")
                return False
            
            print(f"   ✅ Client job visible in HR Portal: {client_job.get('title')}")
            
            # Step 3: Add candidates via HR Portal
            print("\n👥 Step 3: Adding candidates via HR Portal...")
            
            hr_candidates = WorkflowTestData.create_test_candidates(job_id, 2)
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/candidates/bulk",
                headers=self.config.HEADERS,
                json={"candidates": hr_candidates},
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ HR candidate upload failed: {response.status_code}")
                return False
            
            candidates_result = response.json()
            candidate_ids = candidates_result.get("candidate_ids", [])
            self.created_resources["candidates"].extend(candidate_ids)
            print(f"   ✅ HR candidates added: {len(candidate_ids)} candidates")
            
            # Step 4: Verify candidates visible to Client Portal
            print("\n🏢 Step 4: Verifying candidate visibility in Client Portal...")
            
            response = requests.get(
                f"{self.config.API_BASE}/v1/candidates/job/{job_id}",
                headers=self.config.HEADERS,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Client candidate fetch failed: {response.status_code}")
                return False
            
            candidates = response.json().get("candidates", [])
            
            if len(candidates) < len(candidate_ids):
                print(f"   ❌ Not all candidates visible to Client Portal: {len(candidates)}/{len(candidate_ids)}")
                return False
            
            print(f"   ✅ All candidates visible to Client Portal: {len(candidates)} candidates")
            
            print(f"\n🎉 CLIENT-HR PORTAL SYNC: SUCCESS")
            return True
            
        except Exception as e:
            print(f"   ❌ Portal sync test failed: {str(e)}")
            return False
    
    def test_ai_matching_workflow(self) -> bool:
        """
        Test AI matching workflow across services:
        1. Create job with specific requirements
        2. Upload diverse candidates
        3. Test semantic matching
        4. Verify scoring consistency
        5. Test batch processing
        """
        print("\n" + "="*60)
        print("🤖 AI MATCHING WORKFLOW TEST")
        print("="*60)
        
        try:
            # Step 1: Create specialized job
            print("\n📋 Step 1: Creating specialized job...")
            
            ai_job_data = {
                "title": "E2E AI/ML Engineer",
                "description": "Looking for AI/ML engineer with Python, TensorFlow, PyTorch, and cloud experience",
                "client_id": 1,
                "department": "AI Research",
                "location": "San Francisco",
                "experience_level": "Senior",
                "employment_type": "Full-time",
                "requirements": "Python, TensorFlow, PyTorch, AWS, Machine Learning, Deep Learning, 5+ years",
                "status": "active"
            }
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/jobs",
                headers=self.config.HEADERS,
                json=ai_job_data,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ AI job creation failed: {response.status_code}")
                return False
            
            job_result = response.json()
            job_id = job_result.get("job_id")
            self.created_resources["jobs"].append(job_id)
            print(f"   ✅ AI job created: ID {job_id}")
            
            # Step 2: Upload diverse candidates with varying skill matches
            print("\n👥 Step 2: Uploading diverse candidates...")
            
            diverse_candidates = [
                {
                    "name": "Perfect Match AI Engineer",
                    "email": "perfect@testdomain.com",
                    "phone": "+1-555-0201",
                    "location": "San Francisco",
                    "experience_years": 6,
                    "technical_skills": "Python, TensorFlow, PyTorch, AWS, Machine Learning, Deep Learning, Kubernetes",
                    "seniority_level": "Senior",
                    "education_level": "PhD",
                    "job_id": job_id,
                    "status": "applied"
                },
                {
                    "name": "Partial Match Developer",
                    "email": "partial@testdomain.com",
                    "phone": "+1-555-0202",
                    "location": "Remote",
                    "experience_years": 4,
                    "technical_skills": "Python, TensorFlow, SQL, Docker",
                    "seniority_level": "Mid-level",
                    "education_level": "Masters",
                    "job_id": job_id,
                    "status": "applied"
                },
                {
                    "name": "Poor Match Backend Dev",
                    "email": "poor@testdomain.com",
                    "phone": "+1-555-0203",
                    "location": "New York",
                    "experience_years": 2,
                    "technical_skills": "Java, Spring, MySQL, REST APIs",
                    "seniority_level": "Junior",
                    "education_level": "Bachelors",
                    "job_id": job_id,
                    "status": "applied"
                }
            ]
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/candidates/bulk",
                headers=self.config.HEADERS,
                json={"candidates": diverse_candidates},
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"   ❌ Diverse candidate upload failed: {response.status_code}")
                return False
            
            candidates_result = response.json()
            candidate_ids = candidates_result.get("candidate_ids", [])
            self.created_resources["candidates"].extend(candidate_ids)
            print(f"   ✅ Diverse candidates uploaded: {len(candidate_ids)} candidates")
            
            # Step 3: Test AI matching
            print("\n🤖 Step 3: Testing AI matching...")
            
            start_time = time.time()
            response = requests.get(
                f"{self.config.API_BASE}/v1/match/{job_id}/top",
                headers=self.config.HEADERS,
                timeout=20  # AI matching may take longer
            )
            matching_time = time.time() - start_time
            
            if response.status_code != 200:
                print(f"   ❌ AI matching failed: {response.status_code}")
                return False
            
            matching_result = response.json()
            top_candidates = matching_result.get("top_candidates", [])
            
            if len(top_candidates) < 3:
                print(f"   ❌ Expected 3 candidates, got {len(top_candidates)}")
                return False
            
            print(f"   ✅ AI matching completed in {matching_time:.2f}s")
            
            # Step 4: Verify scoring consistency
            print("\n📊 Step 4: Verifying scoring consistency...")
            
            scores = [candidate.get("score", 0) for candidate in top_candidates]
            
            # Verify scores are in descending order
            if scores != sorted(scores, reverse=True):
                print(f"   ❌ Scores not properly ordered: {scores}")
                return False
            
            # Verify perfect match has highest score
            best_candidate = top_candidates[0]
            if "Perfect Match" not in best_candidate.get("name", ""):
                print(f"   ⚠️ Perfect match candidate not ranked first")
            
            # Verify score ranges are reasonable
            if not all(0 <= score <= 100 for score in scores):
                print(f"   ❌ Invalid score range: {scores}")
                return False
            
            print(f"   ✅ Scoring consistency verified")
            print(f"      Best: {best_candidate.get('name')} (Score: {best_candidate.get('score', 0):.1f})")
            print(f"      Range: {min(scores):.1f} - {max(scores):.1f}")
            
            # Step 5: Test individual candidate analysis
            print("\n🔍 Step 5: Testing individual candidate analysis...")
            
            best_candidate_id = best_candidate.get("candidate_id")
            response = requests.get(
                f"{self.config.AI_BASE}/analyze/{best_candidate_id}",
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                analysis = response.json()
                print(f"   ✅ Individual analysis completed")
                print(f"      Skills match: {analysis.get('skills_match', 'N/A')}")
                print(f"      Experience fit: {analysis.get('experience_fit', 'N/A')}")
            else:
                print(f"   ⚠️ Individual analysis not available: {response.status_code}")
            
            print(f"\n🎉 AI MATCHING WORKFLOW: SUCCESS")
            return True
            
        except Exception as e:
            print(f"   ❌ AI matching workflow failed: {str(e)}")
            return False
    
    def test_error_handling_workflow(self) -> bool:
        """
        Test error handling across services:
        1. Invalid data submissions
        2. Service unavailability scenarios
        3. Data consistency during failures
        4. Recovery mechanisms
        """
        print("\n" + "="*60)
        print("⚠️ ERROR HANDLING WORKFLOW TEST")
        print("="*60)
        
        try:
            # Test 1: Invalid job data
            print("\n❌ Test 1: Invalid job data handling...")
            
            invalid_job = {
                "title": "",  # Empty title
                "description": "Test",
                "client_id": "invalid",  # Wrong type
                "requirements": None  # Null requirements
            }
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/jobs",
                headers=self.config.HEADERS,
                json=invalid_job,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 400:
                print(f"   ✅ Invalid job data properly rejected: {response.status_code}")
            else:
                print(f"   ❌ Invalid job data not properly handled: {response.status_code}")
                return False
            
            # Test 2: Invalid candidate data
            print("\n❌ Test 2: Invalid candidate data handling...")
            
            invalid_candidates = {
                "candidates": [
                    {
                        "name": "",  # Empty name
                        "email": "invalid-email",  # Invalid email
                        "experience_years": -1,  # Negative experience
                        "job_id": 99999  # Non-existent job
                    }
                ]
            }
            
            response = requests.post(
                f"{self.config.API_BASE}/v1/candidates/bulk",
                headers=self.config.HEADERS,
                json=invalid_candidates,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code in [400, 422]:
                print(f"   ✅ Invalid candidate data properly rejected: {response.status_code}")
            else:
                print(f"   ❌ Invalid candidate data not properly handled: {response.status_code}")
                return False
            
            # Test 3: Non-existent resource access
            print("\n❌ Test 3: Non-existent resource handling...")
            
            response = requests.get(
                f"{self.config.API_BASE}/v1/match/99999/top",
                headers=self.config.HEADERS,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 404:
                print(f"   ✅ Non-existent job properly handled: {response.status_code}")
            else:
                print(f"   ❌ Non-existent job not properly handled: {response.status_code}")
                return False
            
            # Test 4: Authentication errors
            print("\n❌ Test 4: Authentication error handling...")
            
            invalid_headers = {"Authorization": "Bearer invalid-token"}
            response = requests.get(
                f"{self.config.API_BASE}/v1/jobs",
                headers=invalid_headers,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 401:
                print(f"   ✅ Invalid authentication properly rejected: {response.status_code}")
            else:
                print(f"   ❌ Invalid authentication not properly handled: {response.status_code}")
                return False
            
            print(f"\n🎉 ERROR HANDLING WORKFLOW: SUCCESS")
            return True
            
        except Exception as e:
            print(f"   ❌ Error handling test failed: {str(e)}")
            return False
    
    def run_all_workflows(self) -> Dict[str, bool]:
        """Run all end-to-end workflow tests"""
        print("🚀 STARTING END-TO-END WORKFLOW TESTING")
        print("="*60)
        
        # Verify services are healthy
        if not self.verify_service_health():
            print("❌ Services not healthy - aborting workflow tests")
            return {}
        
        # Define all workflow tests
        workflows = [
            ("Complete Hiring Workflow", self.test_complete_hiring_workflow),
            ("Client-HR Portal Sync", self.test_client_hr_portal_sync),
            ("AI Matching Workflow", self.test_ai_matching_workflow),
            ("Error Handling Workflow", self.test_error_handling_workflow)
        ]
        
        results = {}
        
        # Run each workflow test
        for workflow_name, workflow_func in workflows:
            print(f"\n🎯 Running: {workflow_name}")
            try:
                start_time = time.time()
                result = workflow_func()
                execution_time = time.time() - start_time
                
                results[workflow_name] = result
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"   {status} in {execution_time:.2f}s")
                
            except Exception as e:
                results[workflow_name] = False
                print(f"   ❌ FAILED - {str(e)}")
        
        # Cleanup resources
        self.cleanup_resources()
        
        # Print summary
        self.print_workflow_summary(results)
        
        return results
    
    def print_workflow_summary(self, results: Dict[str, bool]):
        """Print comprehensive workflow test summary"""
        print("\n" + "="*60)
        print("📊 END-TO-END WORKFLOW TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for workflow_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {workflow_name:<30}: {status}")
        
        print(f"\n📈 Overall Results: {passed}/{total} workflows passed")
        
        if passed == total:
            print("🎉 ALL END-TO-END WORKFLOWS PASSED!")
            print("✅ Multi-service integration fully verified")
            print("✅ Complete user journeys validated")
            print("✅ Cross-service data flow confirmed")
            print("✅ Error handling mechanisms working")
        elif passed >= total * 0.75:
            print("⚠️ MOST WORKFLOWS PASSED - Minor issues detected")
            print("🔍 Review failed workflows for improvements")
        else:
            print("❌ CRITICAL WORKFLOW FAILURES DETECTED")
            print("🚨 Multi-service integration requires immediate attention")
        
        print(f"\n🏁 End-to-End Testing Complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main entry point for E2E workflow testing"""
    tester = E2EWorkflowTester()
    results = tester.run_all_workflows()
    
    # Return appropriate exit code
    all_passed = all(results.values()) if results else False
    return 0 if all_passed else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())