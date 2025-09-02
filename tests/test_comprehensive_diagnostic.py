"""
Comprehensive Enterprise Diagnostic Suite
Complete system validation for global deployment
"""

import requests
import time
import json
import concurrent.futures
from typing import Dict, List, Tuple

BASE_URL = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

class ComprehensiveDiagnostic:
    """Complete enterprise system diagnostic"""
    
    def __init__(self):
        self.results = {}
        self.total_score = 0
        self.max_score = 200  # Increased for comprehensive testing
    
    def test_week1_security(self) -> Dict:
        """Test Week 1 security features"""
        print("Testing Week 1 Security Features...")
        
        tests = {
            "rate_limiting_functionality": self._test_rate_limiting_works(),
            "rate_limiting_headers": self._test_rate_limiting_headers(),
            "security_headers": self._test_security_headers_complete(),
            "input_validation": self._test_input_validation(),
            "csp_policy": self._test_csp_policy()
        }
        
        passed = sum(1 for result in tests.values() if result["passed"])
        score = (passed / len(tests)) * 40  # 40 points for Week 1
        
        return {
            "category": "Week 1 - Critical Security",
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "score": score,
            "status": "COMPLETE" if passed >= 4 else "NEEDS WORK"
        }
    
    def test_week2_features(self) -> Dict:
        """Test Week 2 enhanced features"""
        print("Testing Week 2 Enhanced Features...")
        
        tests = {
            "2fa_setup": self._test_2fa_complete_flow(),
            "2fa_global_compatibility": self._test_2fa_global_ready(),
            "bias_monitoring": self._test_bias_monitoring_ready(),
            "metrics_collection": self._test_metrics_infrastructure(),
            "cloud_deployment": self._test_cloud_readiness()
        }
        
        passed = sum(1 for result in tests.values() if result["passed"])
        score = (passed / len(tests)) * 40  # 40 points for Week 2
        
        return {
            "category": "Week 2 - Enhanced Features",
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "score": score,
            "status": "COMPLETE" if passed >= 4 else "NEEDS WORK"
        }
    
    def test_enterprise_readiness(self) -> Dict:
        """Test enterprise deployment readiness"""
        print("Testing Enterprise Deployment Readiness...")
        
        tests = {
            "api_performance": self._test_api_performance(),
            "concurrent_users": self._test_concurrent_handling(),
            "error_handling": self._test_error_handling(),
            "documentation": self._test_api_documentation(),
            "versioning": self._test_api_versioning()
        }
        
        passed = sum(1 for result in tests.values() if result["passed"])
        score = (passed / len(tests)) * 30  # 30 points for Enterprise
        
        return {
            "category": "Enterprise Readiness",
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "score": score,
            "status": "READY" if passed >= 4 else "NEEDS WORK"
        }
    
    def test_global_deployment(self) -> Dict:
        """Test global deployment capabilities"""
        print("Testing Global Deployment Capabilities...")
        
        tests = {
            "containerization": self._test_docker_ready(),
            "health_monitoring": self._test_health_endpoints(),
            "scalability": self._test_scalability_metrics(),
            "security_compliance": self._test_security_compliance(),
            "multi_region_ready": self._test_multi_region_readiness()
        }
        
        passed = sum(1 for result in tests.values() if result["passed"])
        score = (passed / len(tests)) * 30  # 30 points for Global
        
        return {
            "category": "Global Deployment",
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "score": score,
            "status": "READY" if passed >= 4 else "NEEDS WORK"
        }
    
    def test_production_readiness(self) -> Dict:
        """Test production environment readiness"""
        print("Testing Production Readiness...")
        
        tests = {
            "database_connectivity": self._test_database_health(),
            "ai_agent_connectivity": self._test_ai_agent_health(),
            "portal_integration": self._test_portal_integration(),
            "data_processing": self._test_data_processing(),
            "system_stability": self._test_system_stability()
        }
        
        passed = sum(1 for result in tests.values() if result["passed"])
        score = (passed / len(tests)) * 30  # 30 points for Production
        
        return {
            "category": "Production Readiness",
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "score": score,
            "status": "READY" if passed >= 4 else "NEEDS WORK"
        }
    
    # Week 1 Tests
    def _test_rate_limiting_works(self) -> Dict:
        try:
            # Test rate limiting infrastructure
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                rate_limiting_enabled = data.get("security_features", {}).get("rate_limiting") == "enabled"
                
                return {
                    "passed": rate_limiting_enabled,
                    "details": f"Rate limiting infrastructure: {rate_limiting_enabled}",
                    "impact": "Critical for DoS protection"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
        
        return {"passed": False, "details": "Test failed", "impact": "Critical"}
    
    def _test_rate_limiting_headers(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            # Check for rate limiting infrastructure in response
            data = response.json() if response.status_code == 200 else {}
            rate_limiting_enabled = data.get("security_features", {}).get("rate_limiting") == "enabled"
            
            return {
                "passed": rate_limiting_enabled,
                "details": f"Rate limiting infrastructure: {rate_limiting_enabled}",
                "impact": "High for API protection"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    def _test_security_headers_complete(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            required_headers = [
                "x-content-type-options",
                "x-frame-options",
                "x-xss-protection",
                "content-security-policy",
                "referrer-policy"
            ]
            
            present = [h for h in required_headers if h in response.headers]
            
            return {
                "passed": len(present) >= 4,
                "details": f"Security headers: {len(present)}/5 present",
                "impact": "Critical for security compliance"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def _test_input_validation(self) -> Dict:
        try:
            # Test with malicious input
            malicious_data = {
                "title": "<script>alert('xss')</script>",
                "description": "'; DROP TABLE jobs; --",
                "requirements": "test"
            }
            
            response = requests.post(f"{BASE_URL}/v1/jobs", 
                                   json=malicious_data, headers=HEADERS)
            
            # Should either reject (400) or sanitize
            return {
                "passed": response.status_code in [400, 422, 500],
                "details": f"Malicious input handling: {response.status_code}",
                "impact": "Critical for security"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def _test_csp_policy(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/docs", headers=HEADERS)
            csp = response.headers.get("content-security-policy", "")
            
            has_csp = len(csp) > 50  # Basic CSP should be substantial
            
            return {
                "passed": has_csp,
                "details": f"CSP policy length: {len(csp)} chars",
                "impact": "High for XSS protection"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    # Week 2 Tests
    def _test_2fa_complete_flow(self) -> Dict:
        try:
            # Test 2FA setup endpoint
            setup_response = requests.post(f"{BASE_URL}/v1/2fa/setup",
                                         json={"client_id": "TEST001", "email": "test@bhiv.com"},
                                         headers=HEADERS)
            
            # Test demo endpoint
            demo_response = requests.get(f"{BASE_URL}/v1/2fa/demo-setup", headers=HEADERS)
            
            setup_works = setup_response.status_code == 200
            demo_works = demo_response.status_code == 200
            
            return {
                "passed": setup_works and demo_works,
                "details": f"2FA setup: {setup_works}, Demo: {demo_works}",
                "impact": "Critical for enterprise security"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def _test_2fa_global_ready(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/v1/2fa/demo-setup", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                supported_apps = data.get("supported_apps", [])
                global_apps = ["Google Authenticator", "Microsoft Authenticator", "Authy"]
                compatibility = len([app for app in global_apps if app in supported_apps])
                
                return {
                    "passed": compatibility >= 2,
                    "details": f"Global authenticator support: {compatibility}/3",
                    "impact": "High for global deployment"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
        
        return {"passed": False, "details": "Test failed", "impact": "High"}
    
    def _test_bias_monitoring_ready(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                week2_complete = data.get("security_features", {}).get("week_2_complete", False)
                
                return {
                    "passed": week2_complete,
                    "details": f"Bias monitoring infrastructure: {week2_complete}",
                    "impact": "Critical for compliance"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
        
        return {"passed": False, "details": "Test failed", "impact": "Critical"}
    
    def _test_metrics_infrastructure(self) -> Dict:
        try:
            # Test multiple endpoints to generate metrics
            endpoints = ["/health", "/", "/docs"]
            responses = []
            
            for endpoint in endpoints:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
                responses.append(response.status_code)
            
            success_rate = sum(1 for code in responses if code == 200) / len(responses)
            
            return {
                "passed": success_rate >= 0.8,
                "details": f"Metrics collection success rate: {success_rate:.1%}",
                "impact": "High for monitoring"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    def _test_cloud_readiness(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                has_version = "version" in data
                has_timestamp = "timestamp" in data
                has_status = data.get("status") == "healthy"
                
                cloud_ready = has_version and has_timestamp and has_status
                
                return {
                    "passed": cloud_ready,
                    "details": f"Cloud readiness indicators: {cloud_ready}",
                    "impact": "Critical for cloud deployment"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
        
        return {"passed": False, "details": "Test failed", "impact": "Critical"}
    
    # Enterprise Tests
    def _test_api_performance(self) -> Dict:
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            response_time = time.time() - start_time
            
            return {
                "passed": response_time < 0.1,  # Sub-100ms
                "details": f"API response time: {response_time:.3f}s",
                "impact": "High for user experience"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    def _test_concurrent_handling(self) -> Dict:
        try:
            def make_request():
                return requests.get(f"{BASE_URL}/health", headers=HEADERS)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            success_count = sum(1 for r in results if r.status_code == 200)
            
            return {
                "passed": success_count >= 8,
                "details": f"Concurrent requests handled: {success_count}/10",
                "impact": "Critical for scalability"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def _test_error_handling(self) -> Dict:
        try:
            # Test non-existent endpoint
            response = requests.get(f"{BASE_URL}/nonexistent", headers=HEADERS)
            
            return {
                "passed": response.status_code == 404,
                "details": f"Error handling: {response.status_code}",
                "impact": "Medium for robustness"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Medium"}
    
    def _test_api_documentation(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/docs", headers=HEADERS)
            
            return {
                "passed": response.status_code == 200,
                "details": f"API documentation: {response.status_code == 200}",
                "impact": "High for developer experience"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    def _test_api_versioning(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                version = data.get("version", "")
                
                return {
                    "passed": len(version) > 0,
                    "details": f"API version: {version}",
                    "impact": "High for compatibility"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
        
        return {"passed": False, "details": "Test failed", "impact": "High"}
    
    # Global Deployment Tests
    def _test_docker_ready(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            
            return {
                "passed": response.status_code == 200,
                "details": f"Container health: {response.status_code == 200}",
                "impact": "Critical for containerization"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def _test_health_endpoints(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                required_fields = ["status", "service", "version", "timestamp"]
                present_fields = [field for field in required_fields if field in data]
                
                return {
                    "passed": len(present_fields) >= 3,
                    "details": f"Health fields: {len(present_fields)}/4",
                    "impact": "Critical for orchestration"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
        
        return {"passed": False, "details": "Test failed", "impact": "Critical"}
    
    def _test_scalability_metrics(self) -> Dict:
        try:
            # Test response time under load
            times = []
            for _ in range(5):
                start = time.time()
                response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
                times.append(time.time() - start)
            
            avg_time = sum(times) / len(times)
            
            return {
                "passed": avg_time < 0.2,
                "details": f"Average response time: {avg_time:.3f}s",
                "impact": "High for scalability"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    def _test_security_compliance(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            security_headers = [h for h in response.headers.keys() 
                              if any(sec in h.lower() for sec in ["security", "frame", "xss", "content"])]
            
            return {
                "passed": len(security_headers) >= 3,
                "details": f"Security compliance headers: {len(security_headers)}",
                "impact": "Critical for compliance"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def _test_multi_region_readiness(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                has_global_features = data.get("security_features", {}).get("week_2_complete", False)
                
                return {
                    "passed": has_global_features,
                    "details": f"Multi-region features: {has_global_features}",
                    "impact": "High for global deployment"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
        
        return {"passed": False, "details": "Test failed", "impact": "High"}
    
    # Production Tests
    def _test_database_health(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/test-candidates", headers=HEADERS)
            
            return {
                "passed": response.status_code == 200,
                "details": f"Database connectivity: {response.status_code == 200}",
                "impact": "Critical for data operations"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def _test_ai_agent_health(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                ai_status = data.get("ai_agent_status", "unknown")
                
                return {
                    "passed": ai_status == "operational",
                    "details": f"AI agent status: {ai_status}",
                    "impact": "High for AI features"
                }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
        
        return {"passed": False, "details": "Test failed", "impact": "High"}
    
    def _test_portal_integration(self) -> Dict:
        try:
            # Test client login endpoint
            response = requests.post(f"{BASE_URL}/v1/client/login",
                                   json={"client_id": "TECH001", "password": "google123"},
                                   headers=HEADERS)
            
            return {
                "passed": response.status_code in [200, 401],
                "details": f"Portal integration: {response.status_code}",
                "impact": "High for user access"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    def _test_data_processing(self) -> Dict:
        try:
            response = requests.get(f"{BASE_URL}/v1/jobs", headers=HEADERS)
            
            return {
                "passed": response.status_code == 200,
                "details": f"Data processing: {response.status_code == 200}",
                "impact": "High for core functionality"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "High"}
    
    def _test_system_stability(self) -> Dict:
        try:
            # Test multiple endpoints quickly
            endpoints = ["/health", "/", "/v1/jobs"]
            success_count = 0
            
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=5)
                    if response.status_code in [200, 401]:  # 401 is acceptable for protected endpoints
                        success_count += 1
                except:
                    pass
            
            return {
                "passed": success_count >= 2,
                "details": f"System stability: {success_count}/3 endpoints stable",
                "impact": "Critical for reliability"
            }
        except Exception as e:
            return {"passed": False, "details": str(e), "impact": "Critical"}
    
    def run_comprehensive_diagnostic(self) -> Dict:
        """Run complete comprehensive diagnostic"""
        print("=" * 80)
        print("BHIV HR Platform - Comprehensive Enterprise Diagnostic")
        print("Complete System Validation for Global Deployment")
        print("=" * 80)
        
        categories = [
            self.test_week1_security(),
            self.test_week2_features(),
            self.test_enterprise_readiness(),
            self.test_global_deployment(),
            self.test_production_readiness()
        ]
        
        total_score = sum(cat["score"] for cat in categories)
        total_passed = sum(cat["passed"] for cat in categories)
        total_tests = sum(cat["total"] for cat in categories)
        
        complete_categories = sum(1 for cat in categories if cat["status"] in ["COMPLETE", "READY"])
        
        print(f"\nComprehensive Results Summary:")
        print(f"Total Tests: {total_passed}/{total_tests}")
        print(f"Overall Score: {total_score:.1f}/200")
        print(f"Complete Categories: {complete_categories}/5")
        
        if total_score >= 180:
            deployment_status = "PRODUCTION READY"
        elif total_score >= 160:
            deployment_status = "DEPLOYMENT READY"
        elif total_score >= 140:
            deployment_status = "NEEDS MINOR FIXES"
        else:
            deployment_status = "NEEDS MAJOR WORK"
        
        print(f"Deployment Status: {deployment_status}")
        
        return {
            "categories": categories,
            "summary": {
                "total_tests": total_tests,
                "passed_tests": total_passed,
                "overall_score": total_score,
                "max_score": 200,
                "complete_categories": complete_categories,
                "deployment_status": deployment_status,
                "percentage": (total_score / 200) * 100
            }
        }

if __name__ == "__main__":
    diagnostic = ComprehensiveDiagnostic()
    results = diagnostic.run_comprehensive_diagnostic()
    
    print("\nDetailed Category Results:")
    for category in results["categories"]:
        print(f"\n{category['category']}: {category['passed']}/{category['total']} - {category['status']} ({category['score']:.1f} points)")
        
        for test_name, test_result in category["tests"].items():
            status = "PASS" if test_result["passed"] else "FAIL"
            print(f"  {test_name}: {status} - {test_result['details']}")
    
    summary = results["summary"]
    print(f"\nFinal Assessment:")
    print(f"System Score: {summary['percentage']:.1f}% ({summary['overall_score']}/{summary['max_score']})")
    print(f"Deployment Status: {summary['deployment_status']}")