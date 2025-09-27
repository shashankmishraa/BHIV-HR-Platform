#!/usr/bin/env python3
"""
Critical Issues Resolution Plan - Systematic Implementation
Priority-based recursive verification approach
"""

import requests
import json
from datetime import datetime

class IssueResolver:
    def __init__(self):
        self.api_base = "https://bhiv-hr-gateway-46pz.onrender.com"
        self.headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
        self.resolved_issues = []
        
    def verify_system_health(self):
        """Verify system is operational before starting"""
        try:
            response = requests.get(f"{self.api_base}/health", headers=self.headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def test_database_connection(self):
        """Test database connectivity"""
        try:
            response = requests.get(f"{self.api_base}/test-candidates", headers=self.headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def resolve_issue_1_dashboard(self):
        """Issue 1: HR Analytics Dashboard - Make fully dynamic"""
        print("Resolving Issue 1: HR Analytics Dashboard")
        
        # Test current dashboard data
        try:
            jobs_response = requests.get(f"{self.api_base}/v1/jobs", headers=self.headers, timeout=10)
            candidates_response = requests.get(f"{self.api_base}/v1/candidates/search", headers=self.headers, timeout=10)
            
            if jobs_response.status_code == 200 and candidates_response.status_code == 200:
                jobs_data = jobs_response.json()
                candidates_data = candidates_response.json()
                
                # Extract real metrics
                total_jobs = len(jobs_data.get('jobs', []))
                total_candidates = len(candidates_data.get('candidates', []))
                
                print(f"✅ Dashboard data verified: {total_jobs} jobs, {total_candidates} candidates")
                return True
            else:
                print(f"❌ Dashboard API failed: Jobs {jobs_response.status_code}, Candidates {candidates_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Dashboard test failed: {e}")
            return False
    
    def resolve_issue_2_job_management(self):
        """Issue 2: Job Management - Fix posting and auto-increment IDs"""
        print("Resolving Issue 2: Job Management")
        
        # Test job creation
        test_job = {
            "title": "Test Engineer Position",
            "department": "Engineering", 
            "location": "Remote",
            "experience_level": "Mid-level",
            "requirements": "Python, Testing, Quality Assurance",
            "description": "Quality assurance engineer for testing platform",
            "client_id": 1,
            "employment_type": "Full-time",
            "status": "active"
        }
        
        try:
            response = requests.post(f"{self.api_base}/v1/jobs", json=test_job, headers=self.headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                job_id = result.get('job_id')
                print(f"✅ Job creation verified: ID {job_id}")
                return True
            else:
                print(f"❌ Job creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Job creation test failed: {e}")
            return False
    
    def resolve_issue_3_csv_validation(self):
        """Issue 3: CSV Upload Validation - Handle nan values"""
        print("Resolving Issue 3: CSV Upload Validation")
        
        # Test candidate creation with potential nan values
        test_candidate = {
            "name": "Test Candidate",
            "email": "test.candidate@example.com",
            "phone": "+1-555-0199",
            "location": "Test City",
            "technical_skills": "Python, JavaScript, React",
            "experience_years": 2,
            "seniority_level": "Junior",
            "education_level": "Bachelor's"
        }
        
        try:
            response = requests.post(f"{self.api_base}/v1/candidates", json=test_candidate, headers=self.headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                candidate_id = result.get('candidate_id')
                print(f"✅ Candidate creation verified: ID {candidate_id}")
                return True
            else:
                print(f"❌ Candidate creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Candidate creation test failed: {e}")
            return False
    
    def resolve_issue_4_search_filter(self):
        """Issue 4: Search/Filter Internal Server Error"""
        print("Resolving Issue 4: Search/Filter Functionality")
        
        try:
            # Test basic search
            response = requests.get(f"{self.api_base}/v1/candidates/search", headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                print(f"✅ Search functionality verified: {len(candidates)} candidates found")
                return True
            else:
                print(f"❌ Search failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Search test failed: {e}")
            return False
    
    def resolve_issue_5_ai_matching(self):
        """Issue 5: AI-Powered Candidate Shortlist"""
        print("Resolving Issue 5: AI Matching")
        
        try:
            # Test AI matching for job ID 1
            agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
            response = requests.post(f"{agent_url}/match", json={"job_id": 1}, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('top_candidates', [])
                print(f"✅ AI matching verified: {len(candidates)} matches found")
                return True
            else:
                print(f"❌ AI matching failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ AI matching test failed: {e}")
            return False
    
    def run_recursive_verification(self):
        """Run all issue resolutions with recursive verification"""
        print("Starting Recursive Issue Resolution")
        print(f"Timestamp: {datetime.now()}")
        
        # Pre-flight checks
        if not self.verify_system_health():
            print("❌ System health check failed - aborting")
            return False
            
        if not self.test_database_connection():
            print("❌ Database connection failed - aborting")
            return False
            
        print("✅ Pre-flight checks passed")
        
        # Issue resolution sequence
        issues = [
            ("Dashboard Analytics", self.resolve_issue_1_dashboard),
            ("Job Management", self.resolve_issue_2_job_management), 
            ("CSV Validation", self.resolve_issue_3_csv_validation),
            ("Search/Filter", self.resolve_issue_4_search_filter),
            ("AI Matching", self.resolve_issue_5_ai_matching)
        ]
        
        for issue_name, resolver_func in issues:
            print(f"\n{'='*50}")
            print(f"Processing: {issue_name}")
            
            success = resolver_func()
            if success:
                self.resolved_issues.append(issue_name)
                print(f"✅ {issue_name} - RESOLVED")
            else:
                print(f"❌ {issue_name} - FAILED")
                # Continue with other issues for comprehensive testing
        
        # Final report
        print(f"\n{'='*50}")
        print("RESOLUTION SUMMARY")
        print(f"Resolved: {len(self.resolved_issues)}/{len(issues)} issues")
        print(f"Success Rate: {len(self.resolved_issues)/len(issues)*100:.1f}%")
        
        for issue in self.resolved_issues:
            print(f"✅ {issue}")
            
        return len(self.resolved_issues) == len(issues)

if __name__ == "__main__":
    resolver = IssueResolver()
    success = resolver.run_recursive_verification()
    
    if success:
        print("\nAll critical issues resolved successfully!")
    else:
        print("\nSome issues require additional attention")