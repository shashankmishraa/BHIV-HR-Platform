#!/usr/bin/env python3
"""
BHIV HR Platform - Final Functionality Validation
Comprehensive validation of all working features and capabilities
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class FinalValidator:
    def __init__(self):
        self.base_urls = {
            "gateway": "https://bhiv-hr-gateway.onrender.com",
            "agent": "https://bhiv-hr-agent.onrender.com", 
            "portal": "https://bhiv-hr-portal.onrender.com",
            "client_portal": "https://bhiv-hr-client-portal.onrender.com"
        }
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.validation_results = []

    def validate_result(self, test_name: str, expected: Any, actual: Any, details: str = ""):
        """Validate test results"""
        passed = expected == actual if expected is not None else actual is not None
        status = "PASS" if passed else "FAIL"
        
        result = {
            "test": test_name,
            "status": status,
            "expected": expected,
            "actual": actual,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.validation_results.append(result)
        
        status_symbol = "[PASS]" if passed else "[FAIL]"
        print(f"{status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        if not passed:
            print(f"    Expected: {expected}, Got: {actual}")

    def validate_core_services(self):
        """Validate core service availability"""
        print("\nVALIDATING CORE SERVICES")
        print("-" * 40)
        
        # Gateway service
        try:
            response = requests.get(f"{self.base_urls['gateway']}/health", timeout=10)
            self.validate_result("Gateway Service Health", 200, response.status_code, 
                               "Core API Gateway must be operational")
        except Exception as e:
            self.validate_result("Gateway Service Health", 200, "ERROR", str(e))
        
        # AI Agent service
        try:
            response = requests.get(f"{self.base_urls['agent']}/health", timeout=10)
            self.validate_result("AI Agent Service Health", 200, response.status_code, 
                               "AI matching engine must be operational")
        except Exception as e:
            self.validate_result("AI Agent Service Health", 200, "ERROR", str(e))
        
        # Portal accessibility
        try:
            response = requests.get(f"{self.base_urls['portal']}/", timeout=10)
            self.validate_result("HR Portal Accessibility", 200, response.status_code, 
                               "HR dashboard must be accessible")
        except Exception as e:
            self.validate_result("HR Portal Accessibility", 200, "ERROR", str(e))
        
        try:
            response = requests.get(f"{self.base_urls['client_portal']}/", timeout=10)
            self.validate_result("Client Portal Accessibility", 200, response.status_code, 
                               "Client interface must be accessible")
        except Exception as e:
            self.validate_result("Client Portal Accessibility", 200, "ERROR", str(e))

    def validate_authentication_system(self):
        """Validate authentication and security"""
        print("\nVALIDATING AUTHENTICATION SYSTEM")
        print("-" * 40)
        
        # Test unauthorized access protection
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", timeout=10)
            self.validate_result("Unauthorized Access Protection", 403, response.status_code, 
                               "Must block access without authentication")
        except Exception as e:
            self.validate_result("Unauthorized Access Protection", 403, "ERROR", str(e))
        
        # Test invalid API key
        try:
            invalid_headers = {"Authorization": "Bearer invalid_key"}
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=invalid_headers, timeout=10)
            self.validate_result("Invalid API Key Protection", 401, response.status_code, 
                               "Must reject invalid API keys")
        except Exception as e:
            self.validate_result("Invalid API Key Protection", 401, "ERROR", str(e))
        
        # Test valid API key access
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            self.validate_result("Valid API Key Access", 200, response.status_code, 
                               "Must allow access with valid API key")
        except Exception as e:
            self.validate_result("Valid API Key Access", 200, "ERROR", str(e))

    def validate_job_management(self):
        """Validate job management functionality"""
        print("\nVALIDATING JOB MANAGEMENT")
        print("-" * 40)
        
        # Test job retrieval
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                self.validate_result("Job Data Retrieval", True, len(jobs) > 0, 
                                   f"Retrieved {len(jobs)} jobs")
                
                # Validate job structure
                if jobs:
                    job = jobs[0]
                    required_fields = ['id', 'title', 'department', 'requirements']
                    has_required_fields = all(field in job for field in required_fields)
                    self.validate_result("Job Data Structure", True, has_required_fields, 
                                       f"Job fields: {list(job.keys())}")
            else:
                self.validate_result("Job Data Retrieval", 200, response.status_code)
        except Exception as e:
            self.validate_result("Job Data Retrieval", True, False, str(e))

    def validate_ai_matching_engine(self):
        """Validate AI matching functionality"""
        print("\nVALIDATING AI MATCHING ENGINE")
        print("-" * 40)
        
        # Test AI matching endpoint
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/match/1/top", 
                                  headers=self.headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                self.validate_result("AI Matching Generation", True, len(matches) > 0, 
                                   f"Generated {len(matches)} candidate matches")
                
                # Validate match structure
                if matches:
                    match = matches[0]
                    required_fields = ['candidate_id', 'name', 'score', 'skills_match']
                    has_required_fields = all(field in match for field in required_fields)
                    self.validate_result("AI Match Data Structure", True, has_required_fields, 
                                       f"Match fields: {list(match.keys())}")
                    
                    # Validate scoring system
                    score = match.get('score', 0)
                    valid_score = isinstance(score, (int, float)) and 0 <= score <= 100
                    self.validate_result("AI Scoring System", True, valid_score, 
                                       f"Score: {score}")
            else:
                self.validate_result("AI Matching Generation", 200, response.status_code)
        except Exception as e:
            self.validate_result("AI Matching Generation", True, False, str(e))

    def validate_security_features(self):
        """Validate security features"""
        print("\nVALIDATING SECURITY FEATURES")
        print("-" * 40)
        
        # Test rate limiting status
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/security/rate-limit-status", 
                                  headers=self.headers, timeout=10)
            self.validate_result("Rate Limiting System", 200, response.status_code, 
                               "Rate limiting must be operational")
            
            if response.status_code == 200:
                data = response.json()
                has_rate_info = 'current_requests' in data
                self.validate_result("Rate Limit Data", True, has_rate_info, 
                                   f"Rate limit info: {data}")
        except Exception as e:
            self.validate_result("Rate Limiting System", 200, "ERROR", str(e))
        
        # Test password validation
        try:
            password_data = {"password": "TestPassword123!"}
            response = requests.post(f"{self.base_urls['gateway']}/v1/password/validate", 
                                   headers=self.headers, json=password_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                has_strength = 'password_strength' in data and 'score' in data
                self.validate_result("Password Validation", True, has_strength, 
                                   f"Strength: {data.get('password_strength')}, Score: {data.get('score')}")
            else:
                self.validate_result("Password Validation", 200, response.status_code)
        except Exception as e:
            self.validate_result("Password Validation", True, False, str(e))
        
        # Test CORS configuration
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/security/cors-config", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                has_cors_config = 'cors_config' in data
                self.validate_result("CORS Configuration", True, has_cors_config, 
                                   f"CORS environment: {data.get('environment')}")
            else:
                self.validate_result("CORS Configuration", 200, response.status_code)
        except Exception as e:
            self.validate_result("CORS Configuration", True, False, str(e))

    def validate_monitoring_system(self):
        """Validate monitoring and observability"""
        print("\nVALIDATING MONITORING SYSTEM")
        print("-" * 40)
        
        # Test detailed health check
        try:
            response = requests.get(f"{self.base_urls['gateway']}/health/detailed", timeout=10)
            if response.status_code == 200:
                data = response.json()
                is_healthy = data.get('status') == 'healthy'
                self.validate_result("Detailed Health Check", True, is_healthy, 
                                   f"System status: {data.get('status')}")
            else:
                self.validate_result("Detailed Health Check", 200, response.status_code)
        except Exception as e:
            self.validate_result("Detailed Health Check", True, False, str(e))
        
        # Test metrics endpoint
        try:
            response = requests.get(f"{self.base_urls['gateway']}/metrics", timeout=10)
            if response.status_code == 200:
                metrics_text = response.text
                has_metrics = len(metrics_text) > 100  # Should have substantial metrics
                self.validate_result("Prometheus Metrics", True, has_metrics, 
                                   f"Metrics size: {len(metrics_text)} characters")
            else:
                self.validate_result("Prometheus Metrics", 200, response.status_code)
        except Exception as e:
            self.validate_result("Prometheus Metrics", True, False, str(e))
        
        # Test error monitoring
        try:
            response = requests.get(f"{self.base_urls['gateway']}/monitoring/errors", 
                                  headers=self.headers, timeout=10)
            self.validate_result("Error Monitoring", 200, response.status_code, 
                               "Error tracking must be operational")
        except Exception as e:
            self.validate_result("Error Monitoring", 200, "ERROR", str(e))

    def validate_performance_requirements(self):
        """Validate performance requirements"""
        print("\nVALIDATING PERFORMANCE REQUIREMENTS")
        print("-" * 40)
        
        # Test response times for critical endpoints
        critical_endpoints = [
            ("/health", "Health Check", 1.0),
            ("/v1/jobs", "Job Retrieval", 2.0),
            ("/v1/match/1/top", "AI Matching", 3.0)
        ]
        
        for endpoint, name, max_time in critical_endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_urls['gateway']}{endpoint}", 
                                      headers=self.headers, timeout=10)
                response_time = time.time() - start_time
                
                meets_performance = response_time <= max_time
                self.validate_result(f"{name} Performance", True, meets_performance, 
                                   f"Response time: {response_time:.3f}s (max: {max_time}s)")
            except Exception as e:
                self.validate_result(f"{name} Performance", True, False, str(e))

    def validate_data_consistency(self):
        """Validate data consistency and integrity"""
        print("\nVALIDATING DATA CONSISTENCY")
        print("-" * 40)
        
        # Test candidate data from test endpoint
        try:
            response = requests.get(f"{self.base_urls['gateway']}/test-candidates", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                has_candidates = 'candidates' in data and len(data['candidates']) > 0
                self.validate_result("Test Candidate Data", True, has_candidates, 
                                   f"Test candidates available: {len(data.get('candidates', []))}")
            else:
                self.validate_result("Test Candidate Data", 200, response.status_code)
        except Exception as e:
            self.validate_result("Test Candidate Data", True, False, str(e))
        
        # Test candidate statistics
        try:
            response = requests.get(f"{self.base_urls['gateway']}/candidates/stats", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                has_stats = 'total_candidates' in data
                self.validate_result("Candidate Statistics", True, has_stats, 
                                   f"Stats: {data}")
            else:
                self.validate_result("Candidate Statistics", 200, response.status_code)
        except Exception as e:
            self.validate_result("Candidate Statistics", True, False, str(e))

    def run_final_validation(self):
        """Run complete final validation"""
        print("BHIV HR PLATFORM - FINAL FUNCTIONALITY VALIDATION")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all validation suites
        self.validate_core_services()
        self.validate_authentication_system()
        self.validate_job_management()
        self.validate_ai_matching_engine()
        self.validate_security_features()
        self.validate_monitoring_system()
        self.validate_performance_requirements()
        self.validate_data_consistency()
        
        total_time = time.time() - start_time
        
        # Generate final report
        self.generate_final_report(total_time)

    def generate_final_report(self, total_time: float):
        """Generate final validation report"""
        print("\n" + "=" * 60)
        print("FINAL VALIDATION REPORT")
        print("=" * 60)
        
        total_tests = len(self.validation_results)
        passed_tests = len([t for t in self.validation_results if t['status'] == 'PASS'])
        failed_tests = len([t for t in self.validation_results if t['status'] == 'FAIL'])
        
        print(f"\nVALIDATION SUMMARY:")
        print(f"  Total Validations: {total_tests}")
        print(f"  Passed: {passed_tests}")
        print(f"  Failed: {failed_tests}")
        print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"  Validation Time: {total_time:.2f}s")
        
        # Core functionality status
        core_functions = [
            "Gateway Service Health",
            "AI Agent Service Health", 
            "Valid API Key Access",
            "Job Data Retrieval",
            "AI Matching Generation"
        ]
        
        core_passed = sum(1 for t in self.validation_results 
                         if t['test'] in core_functions and t['status'] == 'PASS')
        
        print(f"\nCORE FUNCTIONALITY STATUS:")
        print(f"  Core Functions Operational: {core_passed}/{len(core_functions)}")
        
        if core_passed == len(core_functions):
            print("  [OK] All core functions are operational")
        else:
            print("  [WARNING] Some core functions have issues")
        
        # Failed validations
        failed_validations = [t for t in self.validation_results if t['status'] == 'FAIL']
        if failed_validations:
            print(f"\nFAILED VALIDATIONS ({len(failed_validations)}):")
            for validation in failed_validations:
                print(f"  - {validation['test']}: {validation['details']}")
        
        # Platform readiness assessment
        readiness_score = (passed_tests / total_tests) * 100
        
        print(f"\nPLATFORM READINESS ASSESSMENT:")
        if readiness_score >= 90:
            print(f"  [EXCELLENT] Platform is production-ready ({readiness_score:.1f}%)")
        elif readiness_score >= 80:
            print(f"  [GOOD] Platform is mostly ready ({readiness_score:.1f}%)")
        elif readiness_score >= 70:
            print(f"  [ACCEPTABLE] Platform has minor issues ({readiness_score:.1f}%)")
        else:
            print(f"  [NEEDS WORK] Platform requires attention ({readiness_score:.1f}%)")
        
        print("\n" + "=" * 60)
        print("FINAL VALIDATION COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    validator = FinalValidator()
    validator.run_final_validation()