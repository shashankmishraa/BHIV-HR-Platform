#!/usr/bin/env python3
"""
Comprehensive Endpoint Verification Script
Tests all 114 endpoints (98 Gateway + 16 Agent) with aggressive validation
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

# Configuration
GATEWAY_BASE = "https://bhiv-hr-gateway.onrender.com"
AGENT_BASE = "https://bhiv-hr-agent.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

class EndpointTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def test_endpoint(self, method: str, url: str, data: Dict = None, expected_status: int = 200, description: str = ""):
        """Test individual endpoint with detailed validation"""
        self.total_tests += 1
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=HEADERS, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=HEADERS, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=HEADERS, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response_time = round((time.time() - start_time) * 1000, 2)
            
            # Validate response
            status_ok = response.status_code == expected_status or (200 <= response.status_code < 300)
            
            try:
                response_data = response.json() if response.content else {}
            except:
                response_data = {"raw_content": response.text[:200]}
                
            result = {
                "method": method,
                "url": url,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time_ms": response_time,
                "success": status_ok,
                "response_size": len(response.content),
                "headers": dict(response.headers),
                "data": response_data
            }
            
            if status_ok:
                self.passed_tests += 1
                print(f"PASS: {method} {url} ({response.status_code}) - {response_time}ms")
            else:
                self.failed_tests += 1
                print(f"FAIL: {method} {url} ({response.status_code}) - {response_time}ms")
                
        except Exception as e:
            self.failed_tests += 1
            result = {
                "method": method,
                "url": url,
                "description": description,
                "error": str(e),
                "success": False,
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }
            print(f"ERROR: {method} {url} - {str(e)}")
            
        self.results.append(result)
        return result

    def test_gateway_endpoints(self):
        """Test all 98 Gateway endpoints"""
        print("\n=== TESTING GATEWAY SERVICE (98 ENDPOINTS) ===")
        
        # Core API (4 endpoints)
        print("\n--- Core API (4) ---")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/", description="Root endpoint")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/health", description="Health check")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/test-candidates", description="Test candidates")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/http-methods-test", description="HTTP methods test")
        
        # Job Management (8 endpoints)
        print("\n--- Job Management (8) ---")
        job_data = {"title": "Test Job", "description": "Test Description", "requirements": ["Python"], "location": "Remote"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/jobs", data=job_data, description="Create job")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/jobs", description="List jobs")
        self.test_endpoint("PUT", f"{GATEWAY_BASE}/v1/jobs/1", data=job_data, description="Update job")
        self.test_endpoint("DELETE", f"{GATEWAY_BASE}/v1/jobs/1", description="Delete job")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/jobs/1", description="Get job by ID")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/jobs/search?q=python", description="Search jobs")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/jobs/stats", description="Job statistics")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/jobs/bulk", data={"jobs": [job_data]}, description="Bulk create jobs")
        
        # Candidate Management (12 endpoints)
        print("\n--- Candidate Management (12) ---")
        candidate_data = {"name": "Test Candidate", "email": "test@example.com", "skills": ["Python"]}
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates", description="List candidates")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/candidates/bulk", data={"candidates": [candidate_data]}, description="Bulk create candidates")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates/search?q=python", description="Search candidates")
        self.test_endpoint("PUT", f"{GATEWAY_BASE}/v1/candidates/1", data=candidate_data, description="Update candidate")
        self.test_endpoint("DELETE", f"{GATEWAY_BASE}/v1/candidates/1", description="Delete candidate")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates/stats", description="Candidate statistics")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/candidates/import", data={"file_url": "test.csv"}, description="Import candidates")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates/export", description="Export candidates")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/candidates/merge", data={"primary_id": 1, "duplicate_id": 2}, description="Merge candidates")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates/duplicates", description="Find duplicates")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/candidates/validate", data=candidate_data, description="Validate candidate")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/candidates/analytics", description="Candidate analytics")
        
        # AI Matching (8 endpoints)
        print("\n--- AI Matching (8) ---")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/match/1/top", description="Top matches for job")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/match/performance-test", description="Performance test")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/match/cache-status", description="Cache status")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/match/batch", data={"job_ids": [1, 2]}, description="Batch matching")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/match/history", description="Match history")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/match/feedback", data={"match_id": 1, "rating": 5}, description="Match feedback")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/match/analytics", description="Match analytics")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/match/retrain", data={"model_type": "basic"}, description="Retrain model")
        
        # Security Testing (12 endpoints)
        print("\n--- Security Testing (12) ---")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/headers", description="Security headers")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/test-xss", data={"input": "test"}, description="XSS test")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/test-sql-injection", data={"query": "test"}, description="SQL injection test")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/audit-log", description="Audit log")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/status", description="Security status")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/rotate-keys", description="Rotate keys")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/policy", description="Security policy")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/threat-detection", description="Threat detection")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/incident-report", data={"type": "test"}, description="Incident report")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/alert-monitor", description="Alert monitor")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/security/alert-config", data={"type": "email"}, description="Alert config")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/backup-status", description="Backup status")
        
        # Authentication (15 endpoints)
        print("\n--- Authentication (15) ---")
        auth_data = {"username": "test", "password": "test123"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/2fa/setup", data=auth_data, description="2FA setup")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/2fa/verify", data={"code": "123456"}, description="2FA verify")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/2fa/login", data=auth_data, description="2FA login")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/password/validate", data={"password": "test123"}, description="Password validate")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/auth/password/generate", description="Password generate")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/password/reset", data={"email": "test@example.com"}, description="Password reset")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/auth/password/history", description="Password history")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/api-key/create", data={"name": "test"}, description="Create API key")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/auth/api-key/list", description="List API keys")
        self.test_endpoint("DELETE", f"{GATEWAY_BASE}/v1/auth/api-key/revoke/test", description="Revoke API key")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/api-key/rotate", data={"key_id": "test"}, description="Rotate API key")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/password/bulk-reset", data={"user_ids": [1, 2]}, description="Bulk password reset")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/auth/sessions/active", description="Active sessions")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/auth/sessions/terminate", data={"session_id": "test"}, description="Terminate session")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/auth/sessions/history", description="Session history")
        
        # CSP Management (4 endpoints)
        print("\n--- CSP Management (4) ---")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/csp/policy", description="CSP policy")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/csp/report", data={"violation": "test"}, description="CSP report")
        self.test_endpoint("PUT", f"{GATEWAY_BASE}/v1/csp/policy", data={"policy": "default-src 'self'"}, description="Update CSP policy")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/security/csp-status", description="CSP status")
        
        # Session Management (6 endpoints)
        print("\n--- Session Management (6) ---")
        session_data = {"user_id": "test", "device": "browser"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/sessions/create", data=session_data, description="Create session")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/sessions/validate", description="Validate session")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/sessions/logout", data={"session_id": "test"}, description="Logout session")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/sessions/active", description="Active sessions")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/sessions/cleanup", description="Cleanup sessions")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/sessions/stats", description="Session stats")
        
        # Interview Management (8 endpoints)
        print("\n--- Interview Management (8) ---")
        interview_data = {"candidate_id": 1, "job_id": 1, "interviewer": "HR Team", "scheduled_time": "2025-01-20T10:00:00Z"}
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/interviews", description="List interviews")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/interviews", data=interview_data, description="Create interview")
        self.test_endpoint("PUT", f"{GATEWAY_BASE}/v1/interviews/1", data=interview_data, description="Update interview")
        self.test_endpoint("DELETE", f"{GATEWAY_BASE}/v1/interviews/1", description="Delete interview")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/interviews/1", description="Get interview")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/interviews/schedule", data=interview_data, description="Schedule interview")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/interviews/calendar", description="Interview calendar")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/interviews/feedback", data={"interview_id": 1, "rating": 5}, description="Interview feedback")
        
        # Database Management (4 endpoints)
        print("\n--- Database Management (4) ---")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/database/health", description="Database health")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/database/add-interviewer-column", description="Add interviewer column")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/database/stats", description="Database stats")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/database/migrate", data={"migration": "test"}, description="Database migrate")
        
        # Monitoring (12 endpoints)
        print("\n--- Monitoring (12) ---")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/metrics", description="Metrics")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/health/detailed", description="Detailed health")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/errors", description="Error monitoring")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/dependencies", description="Dependencies")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/performance", description="Performance")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/alerts", description="Alerts")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/logs", description="Logs")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/dashboard", description="Dashboard")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/export", description="Export")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/monitoring/config", description="Config")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/monitoring/test", data={"type": "load"}, description="Test monitoring")
        self.test_endpoint("POST", f"{GATEWAY_BASE}/monitoring/reset", description="Reset monitoring")
        
        # Analytics (6 endpoints)
        print("\n--- Analytics (6) ---")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/candidates/stats", description="Candidate stats")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/reports/summary", description="Reports summary")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/analytics/dashboard", description="Analytics dashboard")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/analytics/export", description="Analytics export")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/analytics/trends", description="Analytics trends")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/analytics/predictions", description="Analytics predictions")
        
        # Client Portal (3 endpoints)
        print("\n--- Client Portal (3) ---")
        client_data = {"username": "TECH001", "password": "demo123"}
        self.test_endpoint("POST", f"{GATEWAY_BASE}/v1/client/login", data=client_data, description="Client login")
        self.test_endpoint("GET", f"{GATEWAY_BASE}/v1/client/profile", description="Client profile")
        self.test_endpoint("PUT", f"{GATEWAY_BASE}/v1/client/profile", data={"name": "Test Client"}, description="Update client profile")

    def test_agent_endpoints(self):
        """Test all 16 Agent endpoints"""
        print("\n=== TESTING AI AGENT SERVICE (16 ENDPOINTS) ===")
        
        # Core (3 endpoints)
        print("\n--- Core (3) ---")
        self.test_endpoint("GET", f"{AGENT_BASE}/", description="Agent root")
        self.test_endpoint("GET", f"{AGENT_BASE}/health", description="Agent health")
        self.test_endpoint("GET", f"{AGENT_BASE}/status", description="Agent status")
        
        # Matching (8 endpoints)
        print("\n--- Matching (8) ---")
        match_data = {"job_id": 1, "candidate_ids": [1, 2, 3]}
        self.test_endpoint("POST", f"{AGENT_BASE}/match", data=match_data, description="Basic match")
        self.test_endpoint("POST", f"{AGENT_BASE}/match/batch", data={"jobs": [1, 2]}, description="Batch match")
        self.test_endpoint("POST", f"{AGENT_BASE}/match/semantic", data=match_data, description="Semantic match")
        self.test_endpoint("POST", f"{AGENT_BASE}/match/advanced", data=match_data, description="Advanced match")
        self.test_endpoint("POST", f"{AGENT_BASE}/match/explain", data={"match_id": 1}, description="Explain match")
        self.test_endpoint("POST", f"{AGENT_BASE}/match/feedback", data={"match_id": 1, "rating": 5}, description="Match feedback")
        self.test_endpoint("POST", f"{AGENT_BASE}/match/retrain", data={"model": "v3.2.0"}, description="Retrain model")
        self.test_endpoint("POST", f"{AGENT_BASE}/match/benchmark", data={"test_size": 100}, description="Benchmark")
        
        # Analytics (3 endpoints)
        print("\n--- Analytics (3) ---")
        self.test_endpoint("GET", f"{AGENT_BASE}/analytics", description="Agent analytics")
        self.test_endpoint("GET", f"{AGENT_BASE}/performance", description="Agent performance")
        self.test_endpoint("GET", f"{AGENT_BASE}/metrics", description="Agent metrics")
        
        # System (2 endpoints)
        print("\n--- System (2) ---")
        self.test_endpoint("GET", f"{AGENT_BASE}/version", description="Agent version")
        self.test_endpoint("GET", f"{AGENT_BASE}/diagnostics", description="Agent diagnostics")

    def generate_report(self):
        """Generate comprehensive test report"""
        print(f"\n{'='*60}")
        print("COMPREHENSIVE ENDPOINT VERIFICATION REPORT")
        print(f"{'='*60}")
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Failed tests summary
        if self.failed_tests > 0:
            print(f"\n{'='*60}")
            print("FAILED TESTS SUMMARY")
            print(f"{'='*60}")
            for result in self.results:
                if not result.get('success', False):
                    print(f"FAIL: {result['method']} {result['url']}")
                    if 'error' in result:
                        print(f"  Error: {result['error']}")
                    elif 'status_code' in result:
                        print(f"  Status: {result['status_code']}")
        
        # Performance summary
        response_times = [r.get('response_time_ms', 0) for r in self.results if r.get('success', False)]
        if response_times:
            print(f"\n{'='*60}")
            print("PERFORMANCE SUMMARY")
            print(f"{'='*60}")
            print(f"Average Response Time: {sum(response_times)/len(response_times):.2f}ms")
            print(f"Fastest Response: {min(response_times):.2f}ms")
            print(f"Slowest Response: {max(response_times):.2f}ms")
        
        # Save detailed report
        with open('endpoint_verification_report.json', 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': self.total_tests,
                    'passed': self.passed_tests,
                    'failed': self.failed_tests,
                    'success_rate': round(self.passed_tests/self.total_tests*100, 2),
                    'test_date': datetime.now().isoformat()
                },
                'results': self.results
            }, f, indent=2)
        
        print(f"\nDetailed report saved to: endpoint_verification_report.json")

def main():
    """Main test execution"""
    print("BHIV HR Platform - Comprehensive Endpoint Verification")
    print("Testing all 114 endpoints with aggressive validation")
    print(f"Gateway: {GATEWAY_BASE}")
    print(f"Agent: {AGENT_BASE}")
    
    tester = EndpointTester()
    
    # Test all endpoints
    tester.test_gateway_endpoints()
    tester.test_agent_endpoints()
    
    # Generate report
    tester.generate_report()
    
    # Exit with appropriate code
    sys.exit(0 if tester.failed_tests == 0 else 1)

if __name__ == "__main__":
    main()