#!/usr/bin/env python3
"""
BHIV HR Platform - Detailed Issue Investigation
Investigating specific issues found in comprehensive testing
"""

import requests
import json
import time
from datetime import datetime

class DetailedInvestigator:
    def __init__(self):
        self.base_urls = {
            "gateway": "https://bhiv-hr-gateway.onrender.com",
            "agent": "https://bhiv-hr-agent.onrender.com", 
            "portal": "https://bhiv-hr-portal.onrender.com",
            "client_portal": "https://bhiv-hr-client-portal.onrender.com"
        }
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def investigate_portal_health_issues(self):
        """Investigate portal health endpoint issues"""
        print("\nINVESTIGATING PORTAL HEALTH ISSUES")
        print("-" * 50)
        
        for portal_name, url in [("HR Portal", self.base_urls["portal"]), 
                                ("Client Portal", self.base_urls["client_portal"])]:
            print(f"\n{portal_name}: {url}")
            
            # Test different endpoints
            endpoints_to_test = ["/", "/health", "/_stcore/health"]
            
            for endpoint in endpoints_to_test:
                try:
                    response = requests.get(f"{url}{endpoint}", timeout=10)
                    print(f"  {endpoint}: Status {response.status_code}")
                    if response.status_code == 200:
                        print(f"    Content-Type: {response.headers.get('content-type', 'N/A')}")
                        print(f"    Content-Length: {len(response.content)} bytes")
                except Exception as e:
                    print(f"  {endpoint}: ERROR - {str(e)}")

    def investigate_candidate_endpoints(self):
        """Investigate candidate endpoint issues"""
        print("\nINVESTIGATING CANDIDATE ENDPOINTS")
        print("-" * 50)
        
        # Test different candidate endpoints
        candidate_endpoints = [
            "/v1/candidates",
            "/v1/candidates/",
            "/candidates",
            "/test-candidates"
        ]
        
        for endpoint in candidate_endpoints:
            try:
                response = requests.get(f"{self.base_urls['gateway']}{endpoint}", 
                                      headers=self.headers, timeout=10)
                print(f"{endpoint}: Status {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'candidates' in data:
                        print(f"  Found {len(data['candidates'])} candidates")
                    elif isinstance(data, list):
                        print(f"  Found {len(data)} items")
                    else:
                        print(f"  Response type: {type(data)}")
            except Exception as e:
                print(f"{endpoint}: ERROR - {str(e)}")

    def investigate_authentication_behavior(self):
        """Investigate authentication behavior"""
        print("\nINVESTIGATING AUTHENTICATION BEHAVIOR")
        print("-" * 50)
        
        # Test without any headers
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", timeout=10)
            print(f"No auth headers: Status {response.status_code}")
            if response.status_code in [401, 403]:
                print(f"  Response: {response.text[:200]}")
        except Exception as e:
            print(f"No auth: ERROR - {str(e)}")
        
        # Test with invalid API key
        try:
            invalid_headers = {"Authorization": "Bearer invalid_key"}
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=invalid_headers, timeout=10)
            print(f"Invalid API key: Status {response.status_code}")
        except Exception as e:
            print(f"Invalid key: ERROR - {str(e)}")
        
        # Test with valid API key
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            print(f"Valid API key: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Jobs found: {len(data.get('jobs', []))}")
        except Exception as e:
            print(f"Valid key: ERROR - {str(e)}")

    def test_ai_agent_detailed(self):
        """Test AI Agent service in detail"""
        print("\nTESTING AI AGENT SERVICE DETAILED")
        print("-" * 50)
        
        agent_url = self.base_urls["agent"]
        
        # Test root endpoint
        try:
            response = requests.get(f"{agent_url}/", timeout=10)
            print(f"Agent root: Status {response.status_code}")
            if response.status_code == 200:
                print(f"  Response: {response.text[:200]}")
        except Exception as e:
            print(f"Agent root: ERROR - {str(e)}")
        
        # Test docs endpoint
        try:
            response = requests.get(f"{agent_url}/docs", timeout=10)
            print(f"Agent docs: Status {response.status_code}")
        except Exception as e:
            print(f"Agent docs: ERROR - {str(e)}")
        
        # Test matching with proper data
        try:
            match_data = {
                "job_requirements": ["Python", "FastAPI", "Machine Learning"],
                "job_title": "Senior Python Developer",
                "experience_level": "senior"
            }
            response = requests.post(f"{agent_url}/match", json=match_data, timeout=15)
            print(f"Agent matching: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Matches found: {len(data.get('matches', []))}")
        except Exception as e:
            print(f"Agent matching: ERROR - {str(e)}")

    def test_security_features_detailed(self):
        """Test security features in detail"""
        print("\nTESTING SECURITY FEATURES DETAILED")
        print("-" * 50)
        
        # Test 2FA endpoints
        print("\n2FA Testing:")
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/security/2fa/qr", 
                                  headers=self.headers, timeout=10)
            print(f"2FA QR: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  QR data available: {'qr_code' in data}")
        except Exception as e:
            print(f"2FA QR: ERROR - {str(e)}")
        
        # Test password validation with real data
        print("\nPassword Validation:")
        try:
            password_data = {"password": "TestPassword123!"}
            response = requests.post(f"{self.base_urls['gateway']}/v1/password/validate", 
                                   headers=self.headers, json=password_data, timeout=10)
            print(f"Password validation: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Strength: {data.get('password_strength')}")
                print(f"  Score: {data.get('score')}/100")
        except Exception as e:
            print(f"Password validation: ERROR - {str(e)}")
        
        # Test rate limiting status
        print("\nRate Limiting:")
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/security/rate-limit-status", 
                                  headers=self.headers, timeout=10)
            print(f"Rate limit status: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Current requests: {data.get('current_requests', 'N/A')}")
                print(f"  Limit: {data.get('limit', 'N/A')}")
        except Exception as e:
            print(f"Rate limit: ERROR - {str(e)}")

    def test_data_integrity(self):
        """Test data integrity and consistency"""
        print("\nTESTING DATA INTEGRITY")
        print("-" * 50)
        
        # Test job data consistency
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                print(f"Jobs endpoint: {len(jobs)} jobs found")
                
                if jobs:
                    sample_job = jobs[0]
                    print(f"  Sample job fields: {list(sample_job.keys())}")
                    print(f"  Job ID: {sample_job.get('id', 'N/A')}")
                    print(f"  Job title: {sample_job.get('title', 'N/A')}")
        except Exception as e:
            print(f"Job data: ERROR - {str(e)}")
        
        # Test AI matching with real job
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/match/1/top", 
                                  headers=self.headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                print(f"AI matching: {len(matches)} matches found")
                
                if matches:
                    sample_match = matches[0]
                    print(f"  Sample match fields: {list(sample_match.keys())}")
                    print(f"  Match score: {sample_match.get('score', 'N/A')}")
        except Exception as e:
            print(f"AI matching: ERROR - {str(e)}")

    def test_monitoring_capabilities(self):
        """Test monitoring and observability capabilities"""
        print("\nTESTING MONITORING CAPABILITIES")
        print("-" * 50)
        
        # Test detailed health check
        try:
            response = requests.get(f"{self.base_urls['gateway']}/health/detailed", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"Detailed health: Status OK")
                print(f"  Services checked: {len(data.get('services', {}))}")
                print(f"  Overall status: {data.get('status', 'N/A')}")
                
                # Check individual service health
                services = data.get('services', {})
                for service, status in services.items():
                    print(f"    {service}: {status.get('status', 'N/A')}")
        except Exception as e:
            print(f"Detailed health: ERROR - {str(e)}")
        
        # Test metrics endpoint
        try:
            response = requests.get(f"{self.base_urls['gateway']}/metrics", timeout=10)
            print(f"Metrics endpoint: Status {response.status_code}")
            if response.status_code == 200:
                metrics_text = response.text
                print(f"  Metrics size: {len(metrics_text)} characters")
                # Count different metric types
                lines = metrics_text.split('\n')
                metric_lines = [l for l in lines if l and not l.startswith('#')]
                print(f"  Metric entries: {len(metric_lines)}")
        except Exception as e:
            print(f"Metrics: ERROR - {str(e)}")

    def test_client_portal_functionality(self):
        """Test client portal specific functionality"""
        print("\nTESTING CLIENT PORTAL FUNCTIONALITY")
        print("-" * 50)
        
        # Test client login endpoint
        try:
            login_data = {
                "username": "TECH001",
                "password": "demo123"
            }
            response = requests.post(f"{self.base_urls['gateway']}/v1/client/login", 
                                   json=login_data, timeout=10)
            print(f"Client login: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Login successful: {data.get('success', False)}")
                print(f"  Client ID: {data.get('client_id', 'N/A')}")
        except Exception as e:
            print(f"Client login: ERROR - {str(e)}")

    def run_detailed_investigation(self):
        """Run all detailed investigations"""
        print("BHIV HR PLATFORM - DETAILED ISSUE INVESTIGATION")
        print("=" * 60)
        
        self.investigate_portal_health_issues()
        self.investigate_candidate_endpoints()
        self.investigate_authentication_behavior()
        self.test_ai_agent_detailed()
        self.test_security_features_detailed()
        self.test_data_integrity()
        self.test_monitoring_capabilities()
        self.test_client_portal_functionality()
        
        print("\n" + "=" * 60)
        print("DETAILED INVESTIGATION COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    investigator = DetailedInvestigator()
    investigator.run_detailed_investigation()