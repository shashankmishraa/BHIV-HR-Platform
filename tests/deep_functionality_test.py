#!/usr/bin/env python3
"""
Deep Functionality Testing - Verify specific features work correctly
"""

import requests
import json
import time

class DeepFunctionalityTester:
    def __init__(self):
        self.base_url = "https://bhiv-hr-gateway.onrender.com"
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def test_ai_matching_quality(self):
        """Test AI matching quality and data structure"""
        print("\n=== AI MATCHING QUALITY TEST ===")
        
        response = requests.get(f"{self.base_url}/v1/match/1/top", 
                              headers=self.headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            print(f"[PASS] Generated {len(matches)} matches")
            
            if matches:
                match = matches[0]
                required_fields = ['candidate_id', 'name', 'email', 'score', 'skills_match']
                missing_fields = [f for f in required_fields if f not in match]
                
                if not missing_fields:
                    print(f"[PASS] Match data structure complete")
                    print(f"       Top candidate: {match.get('name')} (Score: {match.get('score')})")
                    print(f"       Algorithm: {data.get('algorithm_version')}")
                else:
                    print(f"[FAIL] Missing fields: {missing_fields}")
            
            # Check performance metrics
            processing_time = data.get('processing_time', '0s')
            print(f"       Processing time: {processing_time}")
            
        else:
            print(f"[FAIL] AI matching failed: {response.status_code}")

    def test_candidate_data_integrity(self):
        """Test candidate data integrity"""
        print("\n=== CANDIDATE DATA INTEGRITY ===")
        
        response = requests.get(f"{self.base_url}/v1/candidates", 
                              headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            
            print(f"[PASS] Retrieved {len(candidates)} candidates")
            
            if candidates:
                candidate = candidates[0]
                required_fields = ['id', 'name', 'email']
                has_required = all(f in candidate for f in required_fields)
                
                if has_required:
                    print(f"[PASS] Candidate data structure valid")
                    print(f"       Sample: {candidate.get('name')} ({candidate.get('email')})")
                else:
                    print(f"[FAIL] Missing required candidate fields")
        else:
            print(f"[FAIL] Candidate retrieval failed: {response.status_code}")

    def test_job_data_completeness(self):
        """Test job data completeness"""
        print("\n=== JOB DATA COMPLETENESS ===")
        
        response = requests.get(f"{self.base_url}/v1/jobs", 
                              headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            
            print(f"[PASS] Retrieved {len(jobs)} jobs")
            
            if jobs:
                job = jobs[0]
                required_fields = ['id', 'title', 'department', 'requirements']
                has_required = all(f in job for f in required_fields)
                
                if has_required:
                    print(f"[PASS] Job data structure complete")
                    print(f"       Sample: {job.get('title')} in {job.get('department')}")
                else:
                    print(f"[FAIL] Missing required job fields")
        else:
            print(f"[FAIL] Job retrieval failed: {response.status_code}")

    def test_security_implementation(self):
        """Test security implementation details"""
        print("\n=== SECURITY IMPLEMENTATION ===")
        
        # Test CORS configuration
        response = requests.get(f"{self.base_url}/v1/security/cors-config", 
                              headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            cors_config = data.get('cors_config', {})
            
            print(f"[PASS] CORS configuration retrieved")
            print(f"       Environment: {data.get('environment')}")
            print(f"       Origins: {len(cors_config.get('allowed_origins', []))}")
            print(f"       Methods: {cors_config.get('allowed_methods', [])}")
        else:
            print(f"[FAIL] CORS config failed: {response.status_code}")
        
        # Test rate limiting
        response = requests.get(f"{self.base_url}/v1/security/rate-limit-status", 
                              headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Rate limiting active")
            print(f"       Limit: {data.get('requests_per_minute', 'N/A')}/min")
            print(f"       Current: {data.get('current_requests', 'N/A')}")
        else:
            print(f"[FAIL] Rate limit status failed: {response.status_code}")

    def test_monitoring_capabilities(self):
        """Test monitoring system capabilities"""
        print("\n=== MONITORING CAPABILITIES ===")
        
        # Test detailed health check
        response = requests.get(f"{self.base_url}/health/detailed", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Detailed health check working")
            print(f"       Status: {data.get('status')}")
            print(f"       Services: {len(data.get('services', {}))}")
        else:
            print(f"[FAIL] Detailed health failed: {response.status_code}")
        
        # Test metrics
        response = requests.get(f"{self.base_url}/metrics", timeout=10)
        
        if response.status_code == 200:
            metrics_text = response.text
            print(f"[PASS] Prometheus metrics available")
            print(f"       Size: {len(metrics_text)} characters")
        else:
            print(f"[FAIL] Metrics failed: {response.status_code}")

    def test_database_connectivity(self):
        """Test database connectivity and operations"""
        print("\n=== DATABASE CONNECTIVITY ===")
        
        # Test database health
        response = requests.get(f"{self.base_url}/v1/database/health", 
                              headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            tables = data.get('tables', {})
            
            print(f"[PASS] Database health check passed")
            print(f"       Tables monitored: {len(tables)}")
            
            for table, info in tables.items():
                status = info.get('status', 'unknown')
                count = info.get('count', 0)
                print(f"       {table}: {count} records ({status})")
        else:
            print(f"[FAIL] Database health failed: {response.status_code}")

    def test_api_documentation(self):
        """Test API documentation availability"""
        print("\n=== API DOCUMENTATION ===")
        
        # Test OpenAPI docs
        response = requests.get(f"{self.base_url}/docs", timeout=10)
        
        if response.status_code == 200:
            print(f"[PASS] API documentation accessible")
        else:
            print(f"[FAIL] API docs failed: {response.status_code}")
        
        # Test OpenAPI JSON
        response = requests.get(f"{self.base_url}/openapi.json", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            paths = data.get('paths', {})
            print(f"[PASS] OpenAPI spec available")
            print(f"       Documented endpoints: {len(paths)}")
        else:
            print(f"[FAIL] OpenAPI spec failed: {response.status_code}")

    def test_error_responses(self):
        """Test error response quality"""
        print("\n=== ERROR RESPONSE QUALITY ===")
        
        # Test 404 error
        response = requests.get(f"{self.base_url}/nonexistent", 
                              headers=self.headers, timeout=10)
        
        if response.status_code == 404:
            print(f"[PASS] 404 errors handled correctly")
        else:
            print(f"[FAIL] Expected 404, got {response.status_code}")
        
        # Test validation error
        response = requests.post(f"{self.base_url}/v1/jobs", 
                               headers=self.headers, json={}, timeout=10)
        
        if response.status_code == 422:
            print(f"[PASS] Validation errors handled correctly")
        else:
            print(f"[FAIL] Expected 422, got {response.status_code}")

    def run_deep_tests(self):
        """Run all deep functionality tests"""
        print("BHIV HR PLATFORM - DEEP FUNCTIONALITY TESTING")
        print("=" * 60)
        
        self.test_ai_matching_quality()
        self.test_candidate_data_integrity()
        self.test_job_data_completeness()
        self.test_security_implementation()
        self.test_monitoring_capabilities()
        self.test_database_connectivity()
        self.test_api_documentation()
        self.test_error_responses()
        
        print("\n" + "=" * 60)
        print("DEEP FUNCTIONALITY TESTING COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    tester = DeepFunctionalityTester()
    tester.run_deep_tests()