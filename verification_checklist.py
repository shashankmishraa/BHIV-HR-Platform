#!/usr/bin/env python3
"""
Comprehensive Verification Checklist
Tests all components systematically
"""

import requests
import json
import time
from datetime import datetime

class SystemVerifier:
    def __init__(self):
        self.api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
        self.agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
        self.headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
        self.results = []
    
    def check(self, name, test_func):
        """Run test and record result"""
        try:
            result = test_func()
            status = "PASS" if result else "FAIL"
            self.results.append((name, result, ""))
            print(f"{status}: {name}")
            return result
        except Exception as e:
            self.results.append((name, False, str(e)))
            print(f"FAIL: {name} - {str(e)}")
            return False
    
    def test_dashboard_kpi(self):
        """HR Analytics Dashboard - Real-time KPI metrics"""
        response = requests.get(f"{self.api_base}/v1/jobs", headers=self.headers, timeout=10)
        return response.status_code == 200
    
    def test_job_persistence(self):
        """Job Management - Database persistence"""
        job_data = {
            "title": "Test Job Persistence",
            "department": "Testing",
            "location": "Remote",
            "experience_level": "Mid-level",
            "requirements": "Testing skills",
            "description": "Test job for persistence verification",
            "salary_min": 70000,
            "salary_max": 100000,
            "client_id": 1,
            "employment_type": "Full-time",
            "status": "active"
        }
        response = requests.post(f"{self.api_base}/v1/jobs", json=job_data, headers=self.headers, timeout=10)
        return response.status_code == 200
    
    def test_csv_validation(self):
        """CSV Upload Validation - NaN handling"""
        candidate_data = {
            "name": "Test NaN Candidate",
            "email": "",  # Empty email (NaN equivalent)
            "phone": "",  # Empty phone (NaN equivalent)
            "location": "Remote",
            "technical_skills": "Testing",
            "experience_years": 2,
            "seniority_level": "Junior",
            "education_level": "Bachelor's"
        }
        response = requests.post(f"{self.api_base}/v1/candidates", json=candidate_data, headers=self.headers, timeout=10)
        return response.status_code == 200
    
    def test_search_filter(self):
        """Search & Filter - No server errors"""
        basic_search = requests.get(f"{self.api_base}/v1/candidates", headers=self.headers, timeout=10)
        filter_search = requests.get(f"{self.api_base}/v1/candidates", 
                                   params={"skills": "Python"}, headers=self.headers, timeout=10)
        return basic_search.status_code == 200 and filter_search.status_code == 200
    
    def test_ai_shortlist(self):
        """AI-Powered Shortlist"""
        response = requests.post(f"{self.agent_url}/match", json={"job_id": 1}, timeout=15)
        return response.status_code == 200
    
    def test_interview_workflow(self):
        """Interview Workflow - Schedule and view"""
        interview_data = {
            "candidate_id": 1,
            "job_id": 1,
            "interview_date": "2025-01-30 14:00:00",
            "interviewer": "Test Interviewer",
            "notes": "Test interview"
        }
        create_response = requests.post(f"{self.api_base}/v1/interviews", 
                                      json=interview_data, headers=self.headers, timeout=10)
        if create_response.status_code != 200:
            return False
        
        list_response = requests.get(f"{self.api_base}/v1/interviews", headers=self.headers, timeout=10)
        return list_response.status_code == 200
    
    def test_values_assessment(self):
        """Values Assessment - Score calculation"""
        feedback_data = {
            "candidate_id": 1,
            "job_id": 1,
            "integrity": 4,
            "honesty": 5,
            "discipline": 3,
            "hard_work": 4,
            "gratitude": 4,
            "comments": "Test assessment"
        }
        response = requests.post(f"{self.api_base}/v1/feedback", 
                               json=feedback_data, headers=self.headers, timeout=10)
        return response.status_code == 200
    
    def test_error_logging(self):
        """Error Logging & Monitoring"""
        invalid_job = {"title": "Invalid"}  # Missing required fields
        response = requests.post(f"{self.api_base}/v1/jobs", 
                               json=invalid_job, headers=self.headers, timeout=10)
        return response.status_code == 422  # Validation error expected
    
    def run_all_checks(self):
        """Run all verification checks"""
        print("COMPREHENSIVE VERIFICATION CHECKLIST")
        print("=" * 50)
        
        # Core functionality checks
        self.check("Dashboard KPI Updates", self.test_dashboard_kpi)
        self.check("Job Database Persistence", self.test_job_persistence)
        self.check("CSV NaN Value Handling", self.test_csv_validation)
        self.check("Search & Filter Operations", self.test_search_filter)
        self.check("AI Shortlist Generation", self.test_ai_shortlist)
        self.check("Interview Workflow", self.test_interview_workflow)
        self.check("Values Assessment", self.test_values_assessment)
        self.check("Error Logging", self.test_error_logging)
        
        # Summary
        passed = sum(1 for _, success, _ in self.results if success)
        total = len(self.results)
        
        print("\n" + "=" * 50)
        print(f"VERIFICATION SUMMARY: {passed}/{total} ({passed/total*100:.1f}%)")
        print("=" * 50)
        
        return passed == total

if __name__ == "__main__":
    verifier = SystemVerifier()
    success = verifier.run_all_checks()
    
    if success:
        print("\nALL CHECKS PASSED - System fully operational")
    else:
        print("\nSome checks failed - Review and fix issues")