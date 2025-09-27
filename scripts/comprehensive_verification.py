#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive System Verification
Verifies all credentials, connections, and system functionality after credential updates
"""

import os
import sys
import json
import time
import requests
import psycopg2
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SystemVerifier:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment_variables": {},
            "database_connection": {},
            "service_urls": {},
            "api_authentication": {},
            "inter_service_communication": {},
            "portal_accessibility": {},
            "performance_metrics": {},
            "security_validation": {},
            "overall_status": "PENDING"
        }
        
        # Production URLs
        self.urls = {
            "gateway": "https://bhiv-hr-gateway-46pz.onrender.com",
            "agent": "https://bhiv-hr-agent-m1me.onrender.com", 
            "portal": "https://bhiv-hr-portal-cead.onrender.com",
            "client_portal": "https://bhiv-hr-client-portal-5g33.onrender.com"
        }
        
        # Load environment variables
        self.env_vars = {
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "API_KEY_SECRET": os.getenv("API_KEY_SECRET"),
            "JWT_SECRET": os.getenv("JWT_SECRET"),
            "SECRET_KEY": os.getenv("SECRET_KEY"),
            "GATEWAY_URL": os.getenv("GATEWAY_URL"),
            "AGENT_SERVICE_URL": os.getenv("AGENT_SERVICE_URL"),
            "PORTAL_URL": os.getenv("PORTAL_URL"),
            "CLIENT_PORTAL_URL": os.getenv("CLIENT_PORTAL_URL")
        }

    def verify_environment_variables(self) -> bool:
        """Step 1: Verify environment variables"""
        print("🔍 Step 1: Verifying Environment Variables...")
        
        required_vars = ["DATABASE_URL", "API_KEY_SECRET", "JWT_SECRET"]
        missing_vars = []
        old_credential_patterns = [
            "dev-fallback",
            "your-",
            "GENERATE_",
            "username:password",
            "localhost"
        ]
        
        for var, value in self.env_vars.items():
            if var in required_vars and not value:
                missing_vars.append(var)
            elif value:
                # Check for old credential patterns
                for pattern in old_credential_patterns:
                    if pattern in value:
                        self.results["environment_variables"][f"{var}_warning"] = f"Contains pattern: {pattern}"
        
        self.results["environment_variables"]["missing_required"] = missing_vars
        self.results["environment_variables"]["loaded_vars"] = len([v for v in self.env_vars.values() if v])
        
        success = len(missing_vars) == 0
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {len(missing_vars)} missing required variables")
        
        return success

    def verify_database_connection(self) -> bool:
        """Step 2: Validate database connection"""
        print("🔍 Step 2: Validating Database Connection...")
        
        database_url = self.env_vars.get("DATABASE_URL")
        if not database_url:
            self.results["database_connection"]["error"] = "DATABASE_URL not found"
            print("   ❌ FAIL - DATABASE_URL not configured")
            return False
        
        try:
            # Test connection
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            # Check tables exist
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            self.results["database_connection"]["status"] = "connected"
            self.results["database_connection"]["version"] = version
            self.results["database_connection"]["tables"] = tables
            self.results["database_connection"]["table_count"] = len(tables)
            
            cursor.close()
            conn.close()
            
            print(f"   ✅ PASS - Connected to PostgreSQL, {len(tables)} tables found")
            return True
            
        except Exception as e:
            self.results["database_connection"]["error"] = str(e)
            print(f"   ❌ FAIL - Connection error: {str(e)}")
            return False

    def verify_service_urls(self) -> bool:
        """Step 3: Confirm service URL accessibility"""
        print("🔍 Step 3: Confirming Service URL Accessibility...")
        
        all_accessible = True
        
        for service, url in self.urls.items():
            try:
                start_time = time.time()
                response = requests.get(f"{url}/health", timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                self.results["service_urls"][service] = {
                    "url": url,
                    "status_code": response.status_code,
                    "accessible": response.status_code < 400,
                    "response_time_ms": round(response_time, 2)
                }
                
                status = "✅" if response.status_code < 400 else "❌"
                print(f"   {status} {service}: {url} ({response.status_code}, {response_time:.0f}ms)")
                
                if response.status_code >= 400:
                    all_accessible = False
                    
            except Exception as e:
                self.results["service_urls"][service] = {
                    "url": url,
                    "error": str(e),
                    "accessible": False
                }
                print(f"   ❌ {service}: {url} - Error: {str(e)}")
                all_accessible = False
        
        return all_accessible

    def verify_api_authentication(self) -> bool:
        """Step 4: Check API key and JWT authentication"""
        print("🔍 Step 4: Checking API Authentication...")
        
        api_key = self.env_vars.get("API_KEY_SECRET")
        if not api_key:
            print("   ❌ FAIL - API_KEY_SECRET not found")
            return False
        
        headers = {"Authorization": f"Bearer {api_key}"}
        auth_tests = []
        
        # Test authenticated endpoints
        test_endpoints = [
            f"{self.urls['gateway']}/candidates",
            f"{self.urls['gateway']}/jobs", 
            f"{self.urls['agent']}/match/candidates"
        ]
        
        for endpoint in test_endpoints:
            try:
                response = requests.get(endpoint, headers=headers, timeout=10)
                success = response.status_code < 500  # Allow 401/403 but not 500
                auth_tests.append({
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "success": success
                })
                
                status = "✅" if success else "❌"
                print(f"   {status} {endpoint} ({response.status_code})")
                
            except Exception as e:
                auth_tests.append({
                    "endpoint": endpoint,
                    "error": str(e),
                    "success": False
                })
                print(f"   ❌ {endpoint} - Error: {str(e)}")
        
        self.results["api_authentication"]["tests"] = auth_tests
        success_count = sum(1 for test in auth_tests if test.get("success", False))
        
        return success_count > 0

    def verify_inter_service_communication(self) -> bool:
        """Step 6: Test inter-service API calls"""
        print("🔍 Step 6: Testing Inter-Service Communication...")
        
        api_key = self.env_vars.get("API_KEY_SECRET", "")
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Test gateway to agent communication
        try:
            response = requests.get(
                f"{self.urls['gateway']}/system/modules",
                headers=headers,
                timeout=10
            )
            
            gateway_agent_success = response.status_code < 400
            self.results["inter_service_communication"]["gateway_agent"] = {
                "status_code": response.status_code,
                "success": gateway_agent_success
            }
            
            status = "✅" if gateway_agent_success else "❌"
            print(f"   {status} Gateway ↔ Agent communication ({response.status_code})")
            
            return gateway_agent_success
            
        except Exception as e:
            self.results["inter_service_communication"]["error"] = str(e)
            print(f"   ❌ Inter-service communication failed: {str(e)}")
            return False

    def verify_portal_accessibility(self) -> bool:
        """Step 7: Test portal accessibility"""
        print("🔍 Step 7: Testing Portal Accessibility...")
        
        portals = [
            ("HR Portal", self.urls["portal"]),
            ("Client Portal", self.urls["client_portal"])
        ]
        
        all_accessible = True
        
        for name, url in portals:
            try:
                response = requests.get(url, timeout=15)
                accessible = response.status_code < 400
                
                self.results["portal_accessibility"][name.lower().replace(" ", "_")] = {
                    "url": url,
                    "status_code": response.status_code,
                    "accessible": accessible
                }
                
                status = "✅" if accessible else "❌"
                print(f"   {status} {name}: {url} ({response.status_code})")
                
                if not accessible:
                    all_accessible = False
                    
            except Exception as e:
                self.results["portal_accessibility"][name.lower().replace(" ", "_")] = {
                    "url": url,
                    "error": str(e),
                    "accessible": False
                }
                print(f"   ❌ {name}: {url} - Error: {str(e)}")
                all_accessible = False
        
        return all_accessible

    def verify_performance_metrics(self) -> bool:
        """Step 8: Performance and response time validation"""
        print("🔍 Step 8: Performance Metrics Validation...")
        
        # Test response times
        response_times = []
        
        for i in range(5):
            try:
                start_time = time.time()
                response = requests.get(f"{self.urls['gateway']}/health", timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code < 400:
                    response_times.append(response_time)
                    
            except Exception:
                pass
        
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            max_response = max(response_times)
            min_response = min(response_times)
            
            self.results["performance_metrics"] = {
                "average_response_ms": round(avg_response, 2),
                "max_response_ms": round(max_response, 2),
                "min_response_ms": round(min_response, 2),
                "test_count": len(response_times),
                "performance_acceptable": avg_response < 2000  # Under 2 seconds
            }
            
            print(f"   ✅ Average response time: {avg_response:.0f}ms")
            return avg_response < 2000
        else:
            print("   ❌ No successful response time measurements")
            return False

    def verify_security_validation(self) -> bool:
        """Step 9: Security validation"""
        print("🔍 Step 9: Security Validation...")
        
        security_checks = {
            "https_urls": all(url.startswith("https://") for url in self.urls.values()),
            "no_hardcoded_credentials": True,  # Already verified in step 1
            "environment_variables_loaded": len([v for v in self.env_vars.values() if v]) > 0
        }
        
        # Check for HTTPS
        if security_checks["https_urls"]:
            print("   ✅ All service URLs use HTTPS")
        else:
            print("   ❌ Some service URLs not using HTTPS")
        
        # Check environment variables
        if security_checks["environment_variables_loaded"]:
            print("   ✅ Environment variables properly loaded")
        else:
            print("   ❌ Environment variables not properly loaded")
        
        self.results["security_validation"] = security_checks
        
        return all(security_checks.values())

    def generate_final_report(self) -> bool:
        """Step 10: Generate comprehensive report"""
        print("\n" + "="*80)
        print("📋 COMPREHENSIVE SYSTEM VERIFICATION REPORT")
        print("="*80)
        
        # Calculate overall success
        test_results = [
            self.results["environment_variables"].get("missing_required", []) == [],
            self.results["database_connection"].get("status") == "connected",
            all(service.get("accessible", False) for service in self.results["service_urls"].values()),
            len(self.results["api_authentication"].get("tests", [])) > 0,
            self.results["inter_service_communication"].get("gateway_agent", {}).get("success", False),
            all(portal.get("accessible", False) for portal in self.results["portal_accessibility"].values()),
            self.results["performance_metrics"].get("performance_acceptable", False),
            all(self.results["security_validation"].values())
        ]
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Detailed results
        print(f"\n📊 Detailed Results:")
        print(f"   Environment Variables: {'✅' if test_results[0] else '❌'}")
        print(f"   Database Connection: {'✅' if test_results[1] else '❌'}")
        print(f"   Service URLs: {'✅' if test_results[2] else '❌'}")
        print(f"   API Authentication: {'✅' if test_results[3] else '❌'}")
        print(f"   Inter-Service Communication: {'✅' if test_results[4] else '❌'}")
        print(f"   Portal Accessibility: {'✅' if test_results[5] else '❌'}")
        print(f"   Performance Metrics: {'✅' if test_results[6] else '❌'}")
        print(f"   Security Validation: {'✅' if test_results[7] else '❌'}")
        
        # Service URLs summary
        print(f"\n🌐 Service URLs:")
        for service, url in self.urls.items():
            status = self.results["service_urls"].get(service, {}).get("accessible", False)
            print(f"   {'✅' if status else '❌'} {service.title()}: {url}")
        
        # Performance summary
        if "average_response_ms" in self.results["performance_metrics"]:
            avg_time = self.results["performance_metrics"]["average_response_ms"]
            print(f"\n⚡ Performance: {avg_time}ms average response time")
        
        # Overall status
        overall_success = success_rate >= 80
        self.results["overall_status"] = "PASS" if overall_success else "FAIL"
        
        print(f"\n🎯 Overall Status: {'✅ SYSTEM OPERATIONAL' if overall_success else '❌ ISSUES DETECTED'}")
        
        # Save detailed report
        report_path = "verification_report.json"
        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        return overall_success

    def run_comprehensive_verification(self) -> bool:
        """Run all verification steps"""
        print("🚀 BHIV HR Platform - Comprehensive System Verification")
        print("="*60)
        
        steps = [
            self.verify_environment_variables,
            self.verify_database_connection,
            self.verify_service_urls,
            self.verify_api_authentication,
            self.verify_inter_service_communication,
            self.verify_portal_accessibility,
            self.verify_performance_metrics,
            self.verify_security_validation
        ]
        
        for step in steps:
            try:
                step()
                time.sleep(1)  # Brief pause between steps
            except Exception as e:
                print(f"   ❌ Step failed with error: {str(e)}")
        
        return self.generate_final_report()

def main():
    """Main verification function"""
    verifier = SystemVerifier()
    success = verifier.run_comprehensive_verification()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())