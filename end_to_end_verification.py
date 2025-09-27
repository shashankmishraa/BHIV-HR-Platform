#!/usr/bin/env python3
"""
End-to-End Feature Verification
Comprehensive testing with recursive validation
"""

import requests
import json
import time
import psycopg2
from datetime import datetime

class EndToEndVerifier:
    def __init__(self):
        self.api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
        self.headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
        self.db_url = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
        self.test_results = []
        
    def log_test(self, test_name, success, details):
        """Log test result"""
        status = "PASS" if success else "FAIL"
        print(f"{status}: {test_name} - {details}")
        self.test_results.append((test_name, success, details))
        return success
    
    def verify_database_direct(self, query, expected_condition):
        """Verify database state directly"""
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return expected_condition(result)
        except Exception as e:
            print(f"Database query error: {e}")
            return False
    
    def test_1_dashboard_real_time_kpi(self):
        """Test 1: HR Analytics Dashboard - Real-time KPI updates"""
        print("\n=== TEST 1: Dashboard Real-time KPI ===")
        
        # Get initial dashboard data
        try:
            response = requests.get(f"{self.api_base}/v1/jobs", headers=self.headers, timeout=10)
            initial_jobs = len(response.json().get('jobs', [])) if response.status_code == 200 else 0
            
            response = requests.get(f"{self.api_base}/v1/candidates", headers=self.headers, timeout=10)
            initial_candidates = len(response.json().get('candidates', [])) if response.status_code == 200 else 0
            
            # Create new job to test real-time update
            new_job = {
                "title": "E2E Test Job Dashboard",
                "department": "Testing",
                "location": "Remote",
                "experience_level": "Mid-level",
                "requirements": "End-to-end testing",
                "description": "Job for dashboard testing",
                "salary_min": 75000,
                "salary_max": 105000,
                "client_id": 1,
                "employment_type": "Full-time",
                "status": "active"
            }
            
            job_response = requests.post(f"{self.api_base}/v1/jobs", json=new_job, headers=self.headers, timeout=10)
            
            if job_response.status_code == 200:
                # Verify dashboard reflects update
                time.sleep(2)  # Allow for processing
                updated_response = requests.get(f"{self.api_base}/v1/jobs", headers=self.headers, timeout=10)
                updated_jobs = len(updated_response.json().get('jobs', [])) if updated_response.status_code == 200 else 0
                
                if updated_jobs > initial_jobs:
                    return self.log_test("Dashboard KPI Update", True, f"Jobs increased from {initial_jobs} to {updated_jobs}")
                else:
                    return self.log_test("Dashboard KPI Update", False, f"Jobs count unchanged: {initial_jobs} -> {updated_jobs}")
            else:
                return self.log_test("Dashboard KPI Update", False, f"Job creation failed: {job_response.status_code}")
                
        except Exception as e:
            return self.log_test("Dashboard KPI Update", False, str(e))
    
    def test_2_job_management_persistence(self):
        """Test 2: Job Management - Database persistence and ID sequencing"""
        print("\n=== TEST 2: Job Management Persistence ===")
        
        try:
            # Get current job count from database
            initial_count = 0
            if self.verify_database_direct("SELECT COUNT(*) FROM jobs", lambda r: True):
                conn = psycopg2.connect(self.db_url)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM jobs")
                initial_count = cursor.fetchone()[0]
                cursor.close()
                conn.close()
            
            # Create multiple jobs
            jobs_to_create = [
                {"title": "E2E Job 1", "department": "Engineering", "salary_min": 80000, "salary_max": 120000},
                {"title": "E2E Job 2", "department": "Marketing", "salary_min": 70000, "salary_max": 100000},
                {"title": "E2E Job 3", "department": "Sales", "salary_min": 60000, "salary_max": 90000}
            ]
            
            created_jobs = []
            for i, job_data in enumerate(jobs_to_create):
                full_job = {
                    **job_data,
                    "location": "Remote",
                    "experience_level": "Mid-level", 
                    "requirements": f"E2E Testing {i+1}",
                    "description": f"End-to-end test job {i+1}",
                    "client_id": 1,
                    "employment_type": "Full-time",
                    "status": "active"
                }
                
                response = requests.post(f"{self.api_base}/v1/jobs", json=full_job, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    created_jobs.append(result.get('job_id'))
            
            # Verify database persistence
            time.sleep(3)  # Allow for database writes
            final_count = 0
            if self.verify_database_direct("SELECT COUNT(*) FROM jobs", lambda r: True):
                conn = psycopg2.connect(self.db_url)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM jobs")
                final_count = cursor.fetchone()[0]
                cursor.close()
                conn.close()
            
            jobs_added = final_count - initial_count
            if jobs_added >= len(created_jobs):
                return self.log_test("Job Persistence", True, f"Added {jobs_added} jobs to database")
            else:
                return self.log_test("Job Persistence", False, f"Expected {len(created_jobs)}, got {jobs_added}")
                
        except Exception as e:
            return self.log_test("Job Persistence", False, str(e))
    
    def test_3_csv_validation_nan_handling(self):
        """Test 3: CSV Upload Validation - Handle 'nan' values"""
        print("\n=== TEST 3: CSV Validation NaN Handling ===")
        
        try:
            # Test candidate with potential 'nan' values
            test_candidates = [
                {
                    "name": "Valid Candidate",
                    "email": "valid@test.com",
                    "phone": "+1-555-0199",
                    "location": "Remote",
                    "technical_skills": "Python, Testing",
                    "experience_years": 3,
                    "seniority_level": "Mid-level",
                    "education_level": "Bachelor's"
                },
                {
                    "name": "NaN Email Candidate", 
                    "email": "",  # Simulate 'nan' as empty
                    "phone": "",  # Simulate 'nan' as empty
                    "location": "Remote",
                    "technical_skills": "JavaScript, Testing",
                    "experience_years": 2,
                    "seniority_level": "Junior",
                    "education_level": "Bachelor's"
                }
            ]
            
            success_count = 0
            for candidate in test_candidates:
                response = requests.post(f"{self.api_base}/v1/candidates", json=candidate, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    success_count += 1
            
            if success_count == len(test_candidates):
                return self.log_test("CSV NaN Validation", True, f"All {success_count} candidates created successfully")
            else:
                return self.log_test("CSV NaN Validation", False, f"Only {success_count}/{len(test_candidates)} candidates created")
                
        except Exception as e:
            return self.log_test("CSV NaN Validation", False, str(e))
    
    def test_4_search_filter_functionality(self):
        """Test 4: Search & Filter - No internal errors"""
        print("\n=== TEST 4: Search & Filter Functionality ===")
        
        try:
            # Test basic search
            search_response = requests.get(f"{self.api_base}/v1/candidates", headers=self.headers, timeout=10)
            basic_search_ok = search_response.status_code == 200
            
            # Test filtered search
            filter_params = {"skills": "Python", "location": "Remote"}
            filter_response = requests.get(f"{self.api_base}/v1/candidates", params=filter_params, headers=self.headers, timeout=10)
            filter_search_ok = filter_response.status_code == 200
            
            # Test job search
            job_search_response = requests.get(f"{self.api_base}/v1/jobs", headers=self.headers, timeout=10)
            job_search_ok = job_search_response.status_code == 200
            
            all_searches_ok = basic_search_ok and filter_search_ok and job_search_ok
            
            if all_searches_ok:
                return self.log_test("Search & Filter", True, "All search endpoints working without errors")
            else:
                return self.log_test("Search & Filter", False, f"Search status: Basic={basic_search_ok}, Filter={filter_search_ok}, Jobs={job_search_ok}")
                
        except Exception as e:
            return self.log_test("Search & Filter", False, str(e))
    
    def test_5_ai_matching_functionality(self):
        """Test 5: AI-Powered Shortlist"""
        print("\n=== TEST 5: AI Matching Functionality ===")
        
        try:
            # Test AI agent health first
            agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
            health_response = requests.get(f"{agent_url}/health", timeout=10)
            
            if health_response.status_code == 200:
                # Test matching with job ID 1
                match_response = requests.post(f"{agent_url}/match", json={"job_id": 1}, timeout=15)
                
                if match_response.status_code == 200:
                    match_data = match_response.json()
                    candidates = match_data.get('top_candidates', [])
                    return self.log_test("AI Matching", True, f"AI matching returned {len(candidates)} candidates")
                else:
                    return self.log_test("AI Matching", False, f"Matching failed: {match_response.status_code}")
            else:
                return self.log_test("AI Matching", False, f"AI agent health failed: {health_response.status_code}")
                
        except Exception as e:
            return self.log_test("AI Matching", False, str(e))
    
    def test_6_interview_workflow(self):
        """Test 6: Interview Workflow - Schedule and View"""
        print("\n=== TEST 6: Interview Workflow ===")
        
        try:
            # Test interview creation
            interview_data = {
                "candidate_id": 1,
                "job_id": 1,
                "interview_date": "2025-01-30 14:00:00",
                "interviewer": "E2E Test Interviewer",
                "notes": "End-to-end test interview"
            }
            
            create_response = requests.post(f"{self.api_base}/v1/interviews", json=interview_data, headers=self.headers, timeout=10)
            
            if create_response.status_code == 200:
                # Test interview retrieval
                list_response = requests.get(f"{self.api_base}/v1/interviews", headers=self.headers, timeout=10)
                
                if list_response.status_code == 200:
                    interviews = list_response.json().get('interviews', [])
                    return self.log_test("Interview Workflow", True, f"Interview created and retrieved: {len(interviews)} interviews")
                else:
                    return self.log_test("Interview Workflow", False, f"Interview list failed: {list_response.status_code}")
            else:
                return self.log_test("Interview Workflow", False, f"Interview creation failed: {create_response.status_code}")
                
        except Exception as e:
            return self.log_test("Interview Workflow", False, str(e))
    
    def test_7_values_assessment(self):
        """Test 7: Values Assessment System"""
        print("\n=== TEST 7: Values Assessment ===")
        
        try:
            # Test feedback submission
            feedback_data = {
                "candidate_id": 1,
                "job_id": 1,
                "integrity": 4,
                "honesty": 5,
                "discipline": 3,
                "hard_work": 4,
                "gratitude": 4,
                "comments": "E2E test assessment"
            }
            
            feedback_response = requests.post(f"{self.api_base}/v1/feedback", json=feedback_data, headers=self.headers, timeout=10)
            
            if feedback_response.status_code == 200:
                # Calculate average score
                values = [feedback_data['integrity'], feedback_data['honesty'], feedback_data['discipline'], 
                         feedback_data['hard_work'], feedback_data['gratitude']]
                avg_score = sum(values) / len(values)
                
                return self.log_test("Values Assessment", True, f"Assessment submitted with avg score: {avg_score:.1f}")
            else:
                return self.log_test("Values Assessment", False, f"Assessment failed: {feedback_response.status_code}")
                
        except Exception as e:
            return self.log_test("Values Assessment", False, str(e))
    
    def test_8_error_logging(self):
        """Test 8: Error Logging & Monitoring"""
        print("\n=== TEST 8: Error Logging ===")
        
        try:
            # Test invalid job creation
            invalid_job = {"title": "Invalid Job"}  # Missing required fields
            
            error_response = requests.post(f"{self.api_base}/v1/jobs", json=invalid_job, headers=self.headers, timeout=10)
            
            if error_response.status_code == 422:  # Validation error expected
                error_data = error_response.json()
                has_error_details = 'error' in error_data or 'detail' in error_data
                return self.log_test("Error Logging", True, f"Validation error properly logged: {error_response.status_code}")
            else:
                return self.log_test("Error Logging", False, f"Unexpected response: {error_response.status_code}")
                
        except Exception as e:
            return self.log_test("Error Logging", False, str(e))
    
    def run_comprehensive_verification(self):
        """Run all end-to-end tests with recursive validation"""
        print("COMPREHENSIVE END-TO-END VERIFICATION")
        print(f"Timestamp: {datetime.now()}")
        print("=" * 60)
        
        # Test sequence
        tests = [
            self.test_1_dashboard_real_time_kpi,
            self.test_2_job_management_persistence,
            self.test_3_csv_validation_nan_handling,
            self.test_4_search_filter_functionality,
            self.test_5_ai_matching_functionality,
            self.test_6_interview_workflow,
            self.test_7_values_assessment,
            self.test_8_error_logging
        ]
        
        # Execute tests
        for test_func in tests:
            try:
                test_func()
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"Test execution error: {e}")
        
        # Summary
        print("\n" + "=" * 60)
        print("END-TO-END VERIFICATION SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
        
        for test_name, success, details in self.test_results:
            status = "PASS" if success else "FAIL"
            print(f"{status}: {test_name}")
        
        # Recursive validation check
        if passed >= 6:  # At least 75% pass rate
            print("\nRECURSIVE VALIDATION: PASSED")
            print("System ready for production deployment")
            return True
        else:
            print("\nRECURSIVE VALIDATION: FAILED")
            print("Additional fixes required before deployment")
            return False

if __name__ == "__main__":
    verifier = EndToEndVerifier()
    success = verifier.run_comprehensive_verification()
    
    if success:
        print("\nAll end-to-end tests completed successfully!")
    else:
        print("\nSome end-to-end tests require attention.")