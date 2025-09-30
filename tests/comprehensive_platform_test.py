#!/usr/bin/env python3
"""
BHIV HR Platform - COMPLETE Feature Verification Test
Tests ALL services, endpoints, functionality, integration, and syncing
Covers: 46 API endpoints, 5 services, portal integration, AI matching, security, monitoring
"""

import requests
import json
import time
import random
import string
from datetime import datetime
from typing import Dict, List, Any
import os
import concurrent.futures
import threading

class BHIVPlatformTester:
    def __init__(self):
        # Production URLs
        self.gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
        self.agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
        self.portal_url = "https://bhiv-hr-portal-cead.onrender.com"
        self.client_portal_url = "https://bhiv-hr-client-portal-5g33.onrender.com"
        
        # API Keys
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Test data storage
        self.test_job_id = None
        self.test_candidate_ids = []
        self.test_interview_id = None
        
        # Test results
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "endpoints": {},
            "features": {},
            "integration": {},
            "security": {},
            "monitoring": {},
            "portal_tests": {},
            "ai_tests": {},
            "database_tests": {},
            "issues": [],
            "recommendations": [],
            "performance": {}
        }
        
    def log_result(self, category: str, name: str, status: str, details: str = ""):
        """Log test result"""
        if category not in self.results:
            self.results[category] = {}
        self.results[category][name] = {
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        print(f"[{status}] {category}/{name}: {details}")

    def test_service_health(self):
        """Test all service health endpoints"""
        print("\n=== TESTING SERVICE HEALTH ===")
        
        services = {
            "Gateway": f"{self.gateway_url}/health",
            "AI Agent": f"{self.agent_url}/health", 
            "HR Portal": f"{self.portal_url}/_stcore/health",
            "Client Portal": f"{self.client_portal_url}/_stcore/health"
        }
        
        for service, url in services.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.log_result("services", service, "✅ PASS", f"Status: {response.status_code}")
                else:
                    self.log_result("services", service, "❌ FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("services", service, "❌ ERROR", str(e))

    def test_all_46_endpoints(self):
        """Test all 46 API endpoints systematically"""
        print("\n=== TESTING ALL 46 API ENDPOINTS ===")
        
        # Core API Endpoints (3)
        core_endpoints = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/health", "Health check"),
            ("GET", "/test-candidates", "Test candidates")
        ]
        
        # Job Management (2)
        job_endpoints = [
            ("POST", "/v1/jobs", "Create job"),
            ("GET", "/v1/jobs", "List jobs")
        ]
        
        # Candidate Management (3)
        candidate_endpoints = [
            ("GET", "/v1/candidates/job/1", "Get candidates by job"),
            ("GET", "/v1/candidates/search", "Search candidates"),
            ("POST", "/v1/candidates/bulk", "Bulk upload candidates")
        ]
        
        # AI Matching (1)
        ai_endpoints = [
            ("GET", "/v1/match/1/top", "AI matching")
        ]
        
        # Assessment & Workflow (3)
        assessment_endpoints = [
            ("POST", "/v1/feedback", "Submit feedback"),
            ("GET", "/v1/interviews", "Get interviews"),
            ("POST", "/v1/interviews", "Schedule interview")
        ]
        
        # Analytics (2)
        analytics_endpoints = [
            ("GET", "/candidates/stats", "Candidate statistics"),
            ("GET", "/v1/reports/job/1/export.csv", "Export job report")
        ]
        
        # Client Portal (1)
        client_endpoints = [
            ("POST", "/v1/client/login", "Client authentication")
        ]
        
        # Security Testing (7)
        security_endpoints = [
            ("GET", "/v1/security/rate-limit-status", "Rate limit status"),
            ("GET", "/v1/security/blocked-ips", "Blocked IPs"),
            ("POST", "/v1/security/test-input-validation", "Input validation"),
            ("POST", "/v1/security/test-email-validation", "Email validation"),
            ("POST", "/v1/security/test-phone-validation", "Phone validation"),
            ("GET", "/v1/security/security-headers-test", "Security headers"),
            ("GET", "/v1/security/penetration-test-endpoints", "Penetration testing")
        ]
        
        # CSP Management (4)
        csp_endpoints = [
            ("POST", "/v1/security/csp-report", "CSP violation reporting"),
            ("GET", "/v1/security/csp-violations", "View CSP violations"),
            ("GET", "/v1/security/csp-policies", "Current CSP policies"),
            ("POST", "/v1/security/test-csp-policy", "Test CSP policy")
        ]
        
        # Two-Factor Authentication (8)
        twofa_endpoints = [
            ("POST", "/v1/2fa/setup", "Setup 2FA"),
            ("POST", "/v1/2fa/verify-setup", "Verify 2FA setup"),
            ("POST", "/v1/2fa/login-with-2fa", "Login with 2FA"),
            ("GET", "/v1/2fa/status/TECH001", "Get 2FA status"),
            ("POST", "/v1/2fa/disable", "Disable 2FA"),
            ("POST", "/v1/2fa/regenerate-backup-codes", "Regenerate backup codes"),
            ("GET", "/v1/2fa/test-token/TECH001/123456", "Test 2FA token"),
            ("GET", "/v1/2fa/demo-setup", "Demo 2FA setup")
        ]
        
        # Password Management (6)
        password_endpoints = [
            ("POST", "/v1/password/validate", "Validate password"),
            ("POST", "/v1/password/generate", "Generate password"),
            ("GET", "/v1/password/policy", "Password policy"),
            ("POST", "/v1/password/change", "Change password"),
            ("GET", "/v1/password/strength-test", "Password strength test"),
            ("GET", "/v1/password/security-tips", "Password security tips")
        ]
        
        # Monitoring (3)
        monitoring_endpoints = [
            ("GET", "/metrics", "Prometheus metrics"),
            ("GET", "/health/detailed", "Detailed health"),
            ("GET", "/metrics/dashboard", "Metrics dashboard")
        ]
        
        all_endpoint_groups = [
            ("Core API", core_endpoints),
            ("Job Management", job_endpoints),
            ("Candidate Management", candidate_endpoints),
            ("AI Matching", ai_endpoints),
            ("Assessment & Workflow", assessment_endpoints),
            ("Analytics", analytics_endpoints),
            ("Client Portal", client_endpoints),
            ("Security Testing", security_endpoints),
            ("CSP Management", csp_endpoints),
            ("Two-Factor Auth", twofa_endpoints),
            ("Password Management", password_endpoints),
            ("Monitoring", monitoring_endpoints)
        ]
        
        total_endpoints = 0
        for group_name, endpoints in all_endpoint_groups:
            print(f"\n--- Testing {group_name} ({len(endpoints)} endpoints) ---")
            total_endpoints += len(endpoints)
            
            for method, path, description in endpoints:
                self.test_single_endpoint(method, path, description, group_name)
        
        print(f"\n✅ Tested {total_endpoints} endpoints total (Expected: 46)")
        if total_endpoints != 46:
            self.results["issues"].append(f"Endpoint count mismatch: found {total_endpoints}, expected 46")
    
    def test_single_endpoint(self, method: str, path: str, description: str, category: str):
        """Test a single endpoint with appropriate data"""
        try:
            url = f"{self.gateway_url}{path}"
            
            # Prepare test data based on endpoint
            test_data = self.get_test_data_for_endpoint(path)
            
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=test_data, headers=self.headers, timeout=10)
            else:
                response = requests.request(method, url, json=test_data, headers=self.headers, timeout=10)
            
            if response.status_code in [200, 201]:
                self.log_result("endpoints", f"{method} {path}", "✅ PASS", 
                              f"{description} - Status: {response.status_code}")
            elif response.status_code == 401 and "security" not in path.lower():
                self.log_result("endpoints", f"{method} {path}", "⚠️ AUTH", 
                              "Authentication required (expected)")
            else:
                self.log_result("endpoints", f"{method} {path}", "❌ FAIL", 
                              f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("endpoints", f"{method} {path}", "❌ ERROR", str(e))
    
    def get_test_data_for_endpoint(self, path: str) -> dict:
        """Generate appropriate test data for each endpoint"""
        if "/v1/jobs" in path and "POST" in path:
            return {
                "title": f"Test Job {random.randint(1000, 9999)}",
                "department": "Engineering",
                "location": "Remote",
                "experience_level": "Mid-level",
                "requirements": "Python, FastAPI",
                "description": "Test job for verification"
            }
        elif "/v1/candidates/bulk" in path:
            return {
                "candidates": [{
                    "name": f"Test Candidate {random.randint(1000, 9999)}",
                    "email": f"test{random.randint(1000, 9999)}@example.com",
                    "phone": "+1-555-0123",
                    "skills": ["Python", "JavaScript"],
                    "experience": 3
                }]
            }
        elif "/v1/feedback" in path:
            return {
                "candidate_id": 1,
                "job_id": 1,
                "integrity": 4,
                "honesty": 5,
                "discipline": 4,
                "hard_work": 4,
                "gratitude": 5
            }
        elif "/v1/interviews" in path and "POST" in path:
            return {
                "candidate_id": 1,
                "job_id": 1,
                "interview_date": "2025-01-15T10:00:00",
                "interviewer": "Test Interviewer"
            }
        elif "/v1/client/login" in path:
            return {
                "client_id": "TECH001",
                "password": "demo123"
            }
        elif "/v1/security/test-input-validation" in path:
            return {
                "input_data": "<script>alert('test')</script>"
            }
        elif "/v1/security/test-email-validation" in path:
            return {
                "email": "test@example.com"
            }
        elif "/v1/security/test-phone-validation" in path:
            return {
                "phone": "+1-555-0123"
            }
        elif "/v1/security/csp-report" in path:
            return {
                "violated_directive": "script-src",
                "blocked_uri": "https://malicious.com/script.js",
                "document_uri": "https://bhiv-platform.com/page"
            }
        elif "/v1/security/test-csp-policy" in path:
            return {
                "policy": "default-src 'self'"
            }
        elif "/v1/2fa/setup" in path:
            return {
                "user_id": "test_user"
            }
        elif "/v1/2fa/verify-setup" in path or "/v1/2fa/login-with-2fa" in path:
            return {
                "user_id": "test_user",
                "totp_code": "123456"
            }
        elif "/v1/password/validate" in path:
            return {
                "password": "TestPassword123!"
            }
        elif "/v1/password/change" in path:
            return {
                "old_password": "oldpass123",
                "new_password": "NewPassword123!"
            }
        else:
            return {}

    def test_job_management(self):
        """Test job management functionality"""
        print("\n=== TESTING JOB MANAGEMENT ===")
        
        # Create test job
        test_job = {
            "title": f"Test Engineer {random.randint(1000, 9999)}",
            "company": "Test Company Inc",
            "location": "Remote",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "salary_range": "$80,000 - $120,000",
            "description": "Test job description for verification purposes",
            "requirements": ["Python", "FastAPI", "PostgreSQL"],
            "benefits": ["Health insurance", "Remote work", "Flexible hours"],
            "client_id": "TECH001"
        }
        
        try:
            # POST job
            response = requests.post(f"{self.gateway_url}/v1/jobs", 
                                   json=test_job, headers=self.headers, timeout=10)
            
            if response.status_code in [200, 201]:
                job_data = response.json()
                job_id = job_data.get("job_id")
                self.log_result("features", "Job Creation", "✅ PASS", 
                              f"Created job ID: {job_id}")
                
                # GET jobs
                response = requests.get(f"{self.gateway_url}/v1/jobs", 
                                      headers=self.headers, timeout=10)
                if response.status_code == 200:
                    jobs = response.json()
                    self.log_result("features", "Job Listing", "✅ PASS", 
                                  f"Retrieved {len(jobs)} jobs")
                else:
                    self.log_result("features", "Job Listing", "❌ FAIL", 
                                  f"Status: {response.status_code}")
            else:
                self.log_result("features", "Job Creation", "❌ FAIL", 
                              f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("features", "Job Management", "❌ ERROR", str(e))

    def test_candidate_management(self):
        """Test candidate management functionality"""
        print("\n=== TESTING CANDIDATE MANAGEMENT ===")
        
        try:
            # GET candidates
            response = requests.get(f"{self.gateway_url}/v1/candidates", 
                                  headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                candidates = response.json()
                self.log_result("features", "Candidate Listing", "✅ PASS", 
                              f"Retrieved {len(candidates)} candidates")
                
                # Test candidate stats
                response = requests.get(f"{self.gateway_url}/candidates/stats", 
                                      headers=self.headers, timeout=10)
                if response.status_code == 200:
                    stats = response.json()
                    self.log_result("features", "Candidate Stats", "✅ PASS", 
                                  f"Stats: {stats}")
                else:
                    self.log_result("features", "Candidate Stats", "❌ FAIL", 
                                  f"Status: {response.status_code}")
            else:
                self.log_result("features", "Candidate Listing", "❌ FAIL", 
                              f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("features", "Candidate Management", "❌ ERROR", str(e))

    def test_ai_matching(self):
        """Test AI matching functionality"""
        print("\n=== TESTING AI MATCHING ===")
        
        try:
            # Get jobs first
            response = requests.get(f"{self.gateway_url}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                jobs = response.json()
                if jobs:
                    job_id = jobs[0].get("id")
                    
                    # Test AI matching
                    response = requests.get(f"{self.gateway_url}/v1/match/{job_id}/top", 
                                          headers=self.headers, timeout=15)
                    
                    if response.status_code == 200:
                        matches = response.json()
                        self.log_result("features", "AI Matching", "✅ PASS", 
                                      f"Found {len(matches)} matches for job {job_id}")
                    else:
                        self.log_result("features", "AI Matching", "❌ FAIL", 
                                      f"Status: {response.status_code}")
                else:
                    self.log_result("features", "AI Matching", "⚠️ SKIP", 
                                  "No jobs available for matching")
            else:
                self.log_result("features", "AI Matching", "❌ FAIL", 
                              "Could not retrieve jobs")
                
        except Exception as e:
            self.log_result("features", "AI Matching", "❌ ERROR", str(e))

    def test_security_features(self):
        """Test security features"""
        print("\n=== TESTING SECURITY FEATURES ===")
        
        # Test rate limiting status
        try:
            response = requests.get(f"{self.gateway_url}/v1/security/rate-limit-status", 
                                  headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                rate_limit = response.json()
                self.log_result("features", "Rate Limiting", "✅ PASS", 
                              f"Rate limit info: {rate_limit}")
            else:
                self.log_result("features", "Rate Limiting", "❌ FAIL", 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("features", "Rate Limiting", "❌ ERROR", str(e))
        
        # Test unauthorized access
        try:
            response = requests.get(f"{self.gateway_url}/v1/jobs", timeout=10)
            
            if response.status_code == 401:
                self.log_result("features", "Authentication", "✅ PASS", 
                              "Properly blocks unauthorized access")
            else:
                self.log_result("features", "Authentication", "❌ FAIL", 
                              f"Should return 401, got {response.status_code}")
        except Exception as e:
            self.log_result("features", "Authentication", "❌ ERROR", str(e))

    def test_client_portal_auth(self):
        """Test client portal authentication"""
        print("\n=== TESTING CLIENT PORTAL AUTH ===")
        
        try:
            login_data = {
                "client_id": "TECH001",
                "password": "demo123"
            }
            
            response = requests.post(f"{self.gateway_url}/v1/client/login", 
                                   json=login_data, timeout=10)
            
            if response.status_code == 200:
                auth_data = response.json()
                self.log_result("features", "Client Authentication", "✅ PASS", 
                              f"Login successful: {auth_data.get('message', 'OK')}")
            else:
                self.log_result("features", "Client Authentication", "❌ FAIL", 
                              f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("features", "Client Authentication", "❌ ERROR", str(e))

    def test_bulk_operations(self):
        """Test bulk operations"""
        print("\n=== TESTING BULK OPERATIONS ===")
        
        # Test bulk candidate upload
        test_candidates = [
            {
                "name": f"Test Candidate {random.randint(1000, 9999)}",
                "email": f"test{random.randint(1000, 9999)}@example.com",
                "phone": f"+1-555-{random.randint(1000, 9999)}",
                "skills": ["Python", "JavaScript", "SQL"],
                "experience": random.randint(1, 10),
                "location": "Remote"
            }
        ]
        
        try:
            response = requests.post(f"{self.gateway_url}/v1/candidates/bulk", 
                                   json={"candidates": test_candidates}, 
                                   headers=self.headers, timeout=15)
            
            if response.status_code in [200, 201]:
                result = response.json()
                self.log_result("features", "Bulk Upload", "✅ PASS", 
                              f"Uploaded {len(test_candidates)} candidates")
            else:
                self.log_result("features", "Bulk Upload", "❌ FAIL", 
                              f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("features", "Bulk Upload", "❌ ERROR", str(e))

    def test_portal_integration(self):
        """Test portal integration and functionality"""
        print("\n=== TESTING PORTAL INTEGRATION ===")
        
        # Test HR Portal accessibility
        try:
            response = requests.get(f"{self.portal_url}/_stcore/health", timeout=10)
            if response.status_code == 200:
                self.log_result("portal_tests", "HR Portal Health", "✅ PASS", "Portal accessible")
            else:
                self.log_result("portal_tests", "HR Portal Health", "❌ FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("portal_tests", "HR Portal Health", "❌ ERROR", str(e))
        
        # Test Client Portal accessibility
        try:
            response = requests.get(f"{self.client_portal_url}/_stcore/health", timeout=10)
            if response.status_code == 200:
                self.log_result("portal_tests", "Client Portal Health", "✅ PASS", "Portal accessible")
            else:
                self.log_result("portal_tests", "Client Portal Health", "❌ FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("portal_tests", "Client Portal Health", "❌ ERROR", str(e))
    
    def test_ai_agent_integration(self):
        """Test AI agent service integration"""
        print("\n=== TESTING AI AGENT INTEGRATION ===")
        
        # Test AI agent health
        try:
            response = requests.get(f"{self.agent_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_result("ai_tests", "AI Agent Health", "✅ PASS", "AI service online")
            else:
                self.log_result("ai_tests", "AI Agent Health", "❌ FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("ai_tests", "AI Agent Health", "❌ ERROR", str(e))
        
        # Test AI matching functionality
        try:
            match_data = {"job_id": 1}
            response = requests.post(f"{self.agent_url}/match", json=match_data, timeout=15)
            if response.status_code == 200:
                result = response.json()
                candidates = result.get("top_candidates", [])
                self.log_result("ai_tests", "AI Matching", "✅ PASS", 
                              f"Found {len(candidates)} matches")
            else:
                self.log_result("ai_tests", "AI Matching", "❌ FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("ai_tests", "AI Matching", "❌ ERROR", str(e))
        
        # Test candidate analysis
        try:
            response = requests.get(f"{self.agent_url}/analyze/1", timeout=10)
            if response.status_code == 200:
                self.log_result("ai_tests", "Candidate Analysis", "✅ PASS", "Analysis working")
            else:
                self.log_result("ai_tests", "Candidate Analysis", "❌ FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("ai_tests", "Candidate Analysis", "❌ ERROR", str(e))
    
    def test_database_integration(self):
        """Test database connectivity and data integrity"""
        print("\n=== TESTING DATABASE INTEGRATION ===")
        
        # Test database connectivity through gateway
        try:
            response = requests.get(f"{self.gateway_url}/test-candidates", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                candidate_count = data.get("total_candidates", 0)
                self.log_result("database_tests", "Database Connectivity", "✅ PASS", 
                              f"Connected, {candidate_count} candidates")
            else:
                self.log_result("database_tests", "Database Connectivity", "❌ FAIL", 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("database_tests", "Database Connectivity", "❌ ERROR", str(e))
        
        # Test database through AI agent
        try:
            response = requests.get(f"{self.agent_url}/test-db", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "candidates_count" in data:
                    self.log_result("database_tests", "AI Agent DB Access", "✅ PASS", 
                                  f"AI can access DB, {data['candidates_count']} candidates")
                else:
                    self.log_result("database_tests", "AI Agent DB Access", "❌ FAIL", 
                                  "No candidate count returned")
            else:
                self.log_result("database_tests", "AI Agent DB Access", "❌ FAIL", 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("database_tests", "AI Agent DB Access", "❌ ERROR", str(e))
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        print("\n=== TESTING END-TO-END WORKFLOW ===")
        
        # Step 1: Create a job
        job_data = {
            "title": f"E2E Test Job {random.randint(1000, 9999)}",
            "department": "Engineering",
            "location": "Remote",
            "experience_level": "Mid-level",
            "requirements": "Python, FastAPI, PostgreSQL",
            "description": "End-to-end test job"
        }
        
        try:
            response = requests.post(f"{self.gateway_url}/v1/jobs", 
                                   json=job_data, headers=self.headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                self.test_job_id = result.get("job_id")
                self.log_result("integration", "Job Creation", "✅ PASS", 
                              f"Created job ID: {self.test_job_id}")
            else:
                self.log_result("integration", "Job Creation", "❌ FAIL", 
                              f"Status: {response.status_code}")
                return
        except Exception as e:
            self.log_result("integration", "Job Creation", "❌ ERROR", str(e))
            return
        
        # Step 2: Upload candidates
        candidates_data = {
            "candidates": [
                {
                    "name": f"E2E Test Candidate {random.randint(1000, 9999)}",
                    "email": f"e2e{random.randint(1000, 9999)}@example.com",
                    "phone": "+1-555-0199",
                    "skills": ["Python", "FastAPI"],
                    "experience": 3
                }
            ]
        }
        
        try:
            response = requests.post(f"{self.gateway_url}/v1/candidates/bulk", 
                                   json=candidates_data, headers=self.headers, timeout=10)
            if response.status_code == 200:
                self.log_result("integration", "Candidate Upload", "✅ PASS", 
                              "Candidates uploaded successfully")
            else:
                self.log_result("integration", "Candidate Upload", "❌ FAIL", 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("integration", "Candidate Upload", "❌ ERROR", str(e))
        
        # Step 3: Get AI matches
        if self.test_job_id:
            try:
                response = requests.get(f"{self.gateway_url}/v1/match/{self.test_job_id}/top", 
                                      headers=self.headers, timeout=15)
                if response.status_code == 200:
                    matches = response.json()
                    match_count = len(matches.get("matches", []))
                    self.log_result("integration", "AI Matching", "✅ PASS", 
                                  f"Found {match_count} matches")
                else:
                    self.log_result("integration", "AI Matching", "❌ FAIL", 
                                  f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("integration", "AI Matching", "❌ ERROR", str(e))
        
        # Step 4: Schedule interview
        interview_data = {
            "candidate_id": 1,
            "job_id": self.test_job_id or 1,
            "interview_date": "2025-01-15T10:00:00",
            "interviewer": "E2E Test Interviewer"
        }
        
        try:
            response = requests.post(f"{self.gateway_url}/v1/interviews", 
                                   json=interview_data, headers=self.headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                self.test_interview_id = result.get("interview_id")
                self.log_result("integration", "Interview Scheduling", "✅ PASS", 
                              f"Scheduled interview ID: {self.test_interview_id}")
            else:
                self.log_result("integration", "Interview Scheduling", "❌ FAIL", 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("integration", "Interview Scheduling", "❌ ERROR", str(e))
        
        # Step 5: Submit feedback
        feedback_data = {
            "candidate_id": 1,
            "job_id": self.test_job_id or 1,
            "integrity": 4,
            "honesty": 5,
            "discipline": 4,
            "hard_work": 4,
            "gratitude": 5
        }
        
        try:
            response = requests.post(f"{self.gateway_url}/v1/feedback", 
                                   json=feedback_data, headers=self.headers, timeout=10)
            if response.status_code == 200:
                self.log_result("integration", "Feedback Submission", "✅ PASS", 
                              "Feedback submitted successfully")
            else:
                self.log_result("integration", "Feedback Submission", "❌ FAIL", 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("integration", "Feedback Submission", "❌ ERROR", str(e))
    
    def test_performance_metrics(self):
        """Test system performance and response times"""
        print("\n=== TESTING PERFORMANCE METRICS ===")
        
        # Test API response times
        endpoints_to_test = [
            ("/health", "Health Check"),
            ("/v1/jobs", "Job Listing"),
            ("/v1/candidates/search", "Candidate Search"),
            ("/metrics", "Metrics Endpoint")
        ]
        
        for endpoint, name in endpoints_to_test:
            start_time = time.time()
            try:
                response = requests.get(f"{self.gateway_url}{endpoint}", 
                                      headers=self.headers, timeout=10)
                response_time = (time.time() - start_time) * 1000  # Convert to ms
                
                if response.status_code == 200:
                    if response_time < 1000:  # Less than 1 second
                        self.log_result("performance", f"{name} Response Time", "✅ PASS", 
                                      f"{response_time:.0f}ms")
                    else:
                        self.log_result("performance", f"{name} Response Time", "⚠️ SLOW", 
                                      f"{response_time:.0f}ms")
                else:
                    self.log_result("performance", f"{name} Response Time", "❌ FAIL", 
                                  f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("performance", f"{name} Response Time", "❌ ERROR", str(e))
    
    def test_concurrent_requests(self):
        """Test system under concurrent load"""
        print("\n=== TESTING CONCURRENT LOAD ===")
        
        def make_request():
            try:
                response = requests.get(f"{self.gateway_url}/health", 
                                      headers=self.headers, timeout=5)
                return response.status_code == 200
            except:
                return False
        
        # Test with 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        success_count = sum(results)
        success_rate = (success_count / len(results)) * 100
        
        if success_rate >= 90:
            self.log_result("performance", "Concurrent Load Test", "✅ PASS", 
                          f"{success_count}/10 requests successful ({success_rate:.0f}%)")
        else:
            self.log_result("performance", "Concurrent Load Test", "❌ FAIL", 
                          f"{success_count}/10 requests successful ({success_rate:.0f}%)")
    
    def test_monitoring_endpoints(self):
        """Test monitoring and analytics endpoints"""
        print("\n=== TESTING MONITORING SYSTEM ===")
        
        monitoring_endpoints = [
            ("/metrics", "Prometheus Metrics"),
            ("/health/detailed", "Detailed Health Check"),
            ("/metrics/dashboard", "Metrics Dashboard")
        ]
        
        for endpoint, description in monitoring_endpoints:
            try:
                response = requests.get(f"{self.gateway_url}{endpoint}", 
                                      headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    # Check if response contains expected monitoring data
                    if endpoint == "/metrics":
                        if "http_requests_total" in response.text or "system_" in response.text:
                            self.log_result("monitoring", description, "✅ PASS", 
                                          "Prometheus metrics available")
                        else:
                            self.log_result("monitoring", description, "⚠️ PARTIAL", 
                                          "Metrics endpoint accessible but limited data")
                    else:
                        self.log_result("monitoring", description, "✅ PASS", 
                                      "Endpoint accessible")
                else:
                    self.log_result("monitoring", description, "❌ FAIL", 
                                  f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("monitoring", description, "❌ ERROR", str(e))

    def analyze_results(self):
        """Analyze test results and generate recommendations"""
        print("\n=== ANALYZING RESULTS ===")
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        for category in self.results:
            if isinstance(self.results[category], dict):
                for test_name, result in self.results[category].items():
                    if isinstance(result, dict) and "status" in result:
                        total_tests += 1
                        if "✅ PASS" in result["status"]:
                            passed_tests += 1
                        elif "❌ FAIL" in result["status"]:
                            failed_tests += 1
                        elif "❌ ERROR" in result["status"]:
                            error_tests += 1
        
        # Calculate success rate
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "success_rate": f"{success_rate:.1f}%"
        }
        
        # Generate recommendations
        if failed_tests > 0:
            self.results["recommendations"].append("Review failed tests and fix underlying issues")
        if error_tests > 0:
            self.results["recommendations"].append("Investigate error conditions and network connectivity")
        if success_rate < 90:
            self.results["recommendations"].append("Platform stability needs improvement")
        else:
            self.results["recommendations"].append("Platform is performing well")

    def run_all_tests(self):
        """Run comprehensive test suite covering ALL platform functionality"""
        print("🚀 BHIV HR Platform - COMPLETE SYSTEM VERIFICATION")
        print("=" * 80)
        print("Testing: 46 API endpoints, 5 services, portal integration, AI matching,")
        print("         security features, monitoring, database, and end-to-end workflows")
        print("=" * 80)
        
        # Core system tests
        self.test_service_health()
        self.test_all_46_endpoints()
        
        # Feature-specific tests
        self.test_job_management()
        self.test_candidate_management()
        self.test_ai_matching()
        self.test_security_features()
        self.test_client_portal_auth()
        self.test_bulk_operations()
        
        # Integration tests
        self.test_portal_integration()
        self.test_ai_agent_integration()
        self.test_database_integration()
        self.test_end_to_end_workflow()
        
        # Performance and monitoring
        self.test_performance_metrics()
        self.test_concurrent_requests()
        self.test_monitoring_endpoints()
        
        # Analysis and reporting
        self.analyze_results()
        self.generate_comprehensive_report()
        
        return self.results
    
    def generate_comprehensive_report(self):
        """Generate detailed analysis report"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 80)
        
        # Count results by category
        categories = ["services", "endpoints", "features", "integration", 
                     "security", "monitoring", "portal_tests", "ai_tests", 
                     "database_tests", "performance"]
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for category in categories:
            if category in self.results:
                category_tests = self.results[category]
                for test_name, result in category_tests.items():
                    if isinstance(result, dict) and "status" in result:
                        total_tests += 1
                        if "✅ PASS" in result["status"]:
                            passed_tests += 1
                        elif "❌" in result["status"]:
                            failed_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Total Tests Executed: {total_tests}")
        print(f"   Passed: {passed_tests} (✅)")
        print(f"   Failed: {failed_tests} (❌)")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Category breakdown
        print(f"\n📋 CATEGORY BREAKDOWN:")
        for category in categories:
            if category in self.results and self.results[category]:
                cat_total = len(self.results[category])
                cat_passed = sum(1 for r in self.results[category].values() 
                               if isinstance(r, dict) and "✅ PASS" in r.get("status", ""))
                print(f"   {category.title().replace('_', ' ')}: {cat_passed}/{cat_total} passed")
        
        # Feature completeness analysis
        print(f"\n🎯 FEATURE COMPLETENESS ANALYSIS:")
        
        # Check if all 46 endpoints were tested
        endpoint_count = len(self.results.get("endpoints", {}))
        print(f"   API Endpoints: {endpoint_count}/46 tested")
        
        # Check service availability
        service_count = len([s for s in self.results.get("services", {}).values() 
                           if isinstance(s, dict) and "✅ PASS" in s.get("status", "")])
        print(f"   Services Online: {service_count}/4 services")
        
        # Check integration completeness
        integration_features = ["Job Creation", "Candidate Upload", "AI Matching", 
                              "Interview Scheduling", "Feedback Submission"]
        working_integrations = sum(1 for feature in integration_features 
                                 if any(feature in test for test in self.results.get("integration", {})))
        print(f"   Integration Workflow: {working_integrations}/{len(integration_features)} steps")
        
        # Security feature analysis
        security_features = len(self.results.get("security", {}))
        print(f"   Security Features: {security_features} tested")
        
        # Performance analysis
        performance_tests = len(self.results.get("performance", {}))
        print(f"   Performance Tests: {performance_tests} executed")
        
        # Generate recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if success_rate >= 95:
            print("   ✅ Excellent: Platform is production-ready with comprehensive functionality")
        elif success_rate >= 85:
            print("   ✅ Good: Platform is stable with minor issues to address")
        elif success_rate >= 70:
            print("   ⚠️  Fair: Platform needs attention in several areas")
        else:
            print("   ❌ Poor: Platform requires significant fixes before production use")
        
        if failed_tests > 0:
            print(f"   • Review and fix {failed_tests} failed tests")
        
        if endpoint_count < 46:
            print(f"   • Verify all {46 - endpoint_count} missing API endpoints")
        
        if service_count < 4:
            print(f"   • Investigate {4 - service_count} offline services")
        
        # Missing features analysis
        print(f"\n🔍 MISSING FEATURES ANALYSIS:")
        
        expected_features = {
            "Job Management": ["Create Job", "List Jobs", "Update Job", "Delete Job"],
            "Candidate Management": ["Search Candidates", "Bulk Upload", "Individual Profile"],
            "AI Matching": ["Semantic Matching", "Score Calculation", "Ranking Algorithm"],
            "Assessment": ["Values Assessment", "Interview Scheduling", "Feedback System"],
            "Security": ["Authentication", "Rate Limiting", "Input Validation", "2FA"],
            "Monitoring": ["Health Checks", "Metrics", "Performance Tracking"]
        }
        
        for feature_category, features in expected_features.items():
            working_features = 0
            for feature in features:
                # Check if feature is working based on test results
                feature_working = any(
                    feature.lower() in test_name.lower() and "✅ PASS" in result.get("status", "")
                    for category_results in self.results.values()
                    if isinstance(category_results, dict)
                    for test_name, result in category_results.items()
                    if isinstance(result, dict)
                )
                if feature_working:
                    working_features += 1
            
            print(f"   {feature_category}: {working_features}/{len(features)} features working")
        
        print(f"\n📊 DETAILED RESULTS SAVED TO: platform_test_results.json")
        print("=" * 80)

    def save_results(self, filename: str = "platform_test_results.json"):
        """Save test results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📊 Results saved to: {filename}")

if __name__ == "__main__":
    tester = BHIVPlatformTester()
    results = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    summary = results.get("summary", {})
    print(f"Total Tests: {summary.get('total_tests', 0)}")
    print(f"Passed: {summary.get('passed', 0)}")
    print(f"Failed: {summary.get('failed', 0)}")
    print(f"Errors: {summary.get('errors', 0)}")
    print(f"Success Rate: {summary.get('success_rate', '0%')}")
    
    if results.get("recommendations"):
        print("\n💡 RECOMMENDATIONS:")
        for rec in results["recommendations"]:
            print(f"  • {rec}")
    
    tester.save_results()