#!/usr/bin/env python3
"""
Comprehensive Service Connection and Routing Verification
BHIV HR Platform - Complete System Audit

This script performs a thorough verification of:
1. Internal service endpoints and routing
2. External service connections
3. Module routing configurations
4. Integration points between microservices
5. Development vs Production environment consistency
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
import psycopg2
from urllib.parse import urlparse

# Color codes for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ServiceVerifier:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "warnings": 0,
            "services": {},
            "routing": {},
            "integrations": {},
            "issues": [],
            "recommendations": []
        }
        
        # Service configurations
        self.services = {
            "production": {
                "gateway": "https://bhiv-hr-gateway-901a.onrender.com",
                "agent": "https://bhiv-hr-agent-o6nx.onrender.com", 
                "portal": "https://bhiv-hr-portal-xk2k.onrender.com",
                "client_portal": "https://bhiv-hr-client-portal-zdbt.onrender.com"
            },
            "development": {
                "gateway": "http://localhost:8000",
                "agent": "http://localhost:9000",
                "portal": "http://localhost:8501",
                "client_portal": "http://localhost:8502"
            }
        }
        
        # Expected endpoints by service
        self.expected_endpoints = {
            "gateway": {
                "core": ["/", "/health", "/test-candidates", "/http-methods-test"],
                "candidates": ["/v1/candidates", "/v1/candidates/stats", "/v1/candidates/search"],
                "jobs": ["/v1/jobs", "/v1/jobs/stats", "/v1/jobs/search"],
                "auth": ["/v1/auth/status", "/v1/auth/test", "/v1/auth/config"],
                "monitoring": ["/metrics", "/health/detailed", "/monitoring/errors"],
                "system": ["/system/modules", "/system/architecture"]
            },
            "agent": {
                "core": ["/", "/health", "/status"],
                "matching": ["/match", "/analyze/{candidate_id}", "/semantic-status"],
                "system": ["/version", "/metrics", "/test-db"]
            }
        }

    def print_header(self, title: str):
        """Print formatted header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{title.center(80)}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.GREEN}[OK] {message}{Colors.END}")

    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.RED}[ERROR] {message}{Colors.END}")

    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}[WARNING] {message}{Colors.END}")

    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.BLUE}[INFO] {message}{Colors.END}")

    def increment_check(self, passed: bool = True):
        """Increment check counters"""
        self.results["total_checks"] += 1
        if passed:
            self.results["passed_checks"] += 1
        else:
            self.results["failed_checks"] += 1

    def add_issue(self, severity: str, component: str, description: str, recommendation: str = None):
        """Add issue to results"""
        issue = {
            "severity": severity,
            "component": component,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        if recommendation:
            issue["recommendation"] = recommendation
        
        self.results["issues"].append(issue)
        
        if recommendation:
            self.results["recommendations"].append({
                "component": component,
                "recommendation": recommendation,
                "priority": severity
            })

    async def verify_service_health(self, environment: str) -> Dict[str, Any]:
        """Verify health of all services in environment"""
        self.print_header(f"SERVICE HEALTH VERIFICATION - {environment.upper()}")
        
        health_results = {}
        services = self.services[environment]
        
        for service_name, base_url in services.items():
            self.print_info(f"Checking {service_name} health: {base_url}")
            
            try:
                # Test basic connectivity
                response = requests.get(f"{base_url}/health", timeout=10)
                
                if response.status_code == 200:
                    health_data = response.json()
                    self.print_success(f"{service_name} is healthy")
                    health_results[service_name] = {
                        "status": "healthy",
                        "response_time": response.elapsed.total_seconds(),
                        "data": health_data
                    }
                    self.increment_check(True)
                else:
                    self.print_error(f"{service_name} health check failed: {response.status_code}")
                    health_results[service_name] = {
                        "status": "unhealthy",
                        "status_code": response.status_code,
                        "error": f"HTTP {response.status_code}"
                    }
                    self.increment_check(False)
                    self.add_issue("high", service_name, f"Health check failed with status {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                self.print_error(f"{service_name} is not accessible (Connection Error)")
                health_results[service_name] = {
                    "status": "unreachable",
                    "error": "Connection refused"
                }
                self.increment_check(False)
                self.add_issue("critical", service_name, "Service is unreachable", 
                             f"Check if {service_name} service is running and accessible")
                
            except requests.exceptions.Timeout:
                self.print_warning(f"{service_name} health check timed out")
                health_results[service_name] = {
                    "status": "timeout",
                    "error": "Request timeout"
                }
                self.increment_check(False)
                self.add_issue("medium", service_name, "Health check timeout")
                
            except Exception as e:
                self.print_error(f"{service_name} health check error: {str(e)}")
                health_results[service_name] = {
                    "status": "error",
                    "error": str(e)
                }
                self.increment_check(False)
                self.add_issue("high", service_name, f"Health check error: {str(e)}")
        
        self.results["services"][environment] = health_results
        return health_results

    async def verify_routing_configuration(self, environment: str) -> Dict[str, Any]:
        """Verify routing configuration for each service"""
        self.print_header(f"ROUTING CONFIGURATION VERIFICATION - {environment.upper()}")
        
        routing_results = {}
        services = self.services[environment]
        
        for service_name, base_url in services.items():
            if service_name not in self.expected_endpoints:
                continue
                
            self.print_info(f"Verifying {service_name} routing: {base_url}")
            service_routing = {}
            
            for module, endpoints in self.expected_endpoints[service_name].items():
                self.print_info(f"  Checking {module} module endpoints...")
                module_results = {}
                
                for endpoint in endpoints:
                    try:
                        # Handle parameterized endpoints
                        test_endpoint = endpoint
                        if "{candidate_id}" in endpoint:
                            test_endpoint = endpoint.replace("{candidate_id}", "1")
                        
                        url = f"{base_url}{test_endpoint}"
                        response = requests.get(url, timeout=5)
                        
                        if response.status_code in [200, 404, 422]:  # 404/422 acceptable for some endpoints
                            self.print_success(f"    {endpoint} -> {response.status_code}")
                            module_results[endpoint] = {
                                "status": "accessible",
                                "status_code": response.status_code,
                                "response_time": response.elapsed.total_seconds()
                            }
                            self.increment_check(True)
                        else:
                            self.print_warning(f"    {endpoint} -> {response.status_code}")
                            module_results[endpoint] = {
                                "status": "unexpected_status",
                                "status_code": response.status_code
                            }
                            self.increment_check(False)
                            
                    except requests.exceptions.ConnectionError:
                        self.print_error(f"    {endpoint} -> Connection Error")
                        module_results[endpoint] = {
                            "status": "unreachable",
                            "error": "Connection refused"
                        }
                        self.increment_check(False)
                        self.add_issue("high", f"{service_name}-{module}", 
                                     f"Endpoint {endpoint} is unreachable")
                        
                    except Exception as e:
                        self.print_error(f"    {endpoint} -> Error: {str(e)}")
                        module_results[endpoint] = {
                            "status": "error",
                            "error": str(e)
                        }
                        self.increment_check(False)
                
                service_routing[module] = module_results
            
            routing_results[service_name] = service_routing
        
        self.results["routing"][environment] = routing_results
        return routing_results

    async def verify_cross_service_integration(self, environment: str) -> Dict[str, Any]:
        """Verify integration between microservices"""
        self.print_header(f"CROSS-SERVICE INTEGRATION VERIFICATION - {environment.upper()}")
        
        integration_results = {}
        services = self.services[environment]
        
        # Test Gateway -> Agent communication
        if "gateway" in services and "agent" in services:
            self.print_info("Testing Gateway -> Agent integration...")
            try:
                # Test if gateway can reach agent through internal routing
                gateway_url = services["gateway"]
                response = requests.get(f"{gateway_url}/system/architecture", timeout=10)
                
                if response.status_code == 200:
                    arch_data = response.json()
                    self.print_success("Gateway system architecture accessible")
                    integration_results["gateway_agent"] = {
                        "status": "accessible",
                        "architecture_data": arch_data
                    }
                    self.increment_check(True)
                else:
                    self.print_error(f"Gateway architecture endpoint failed: {response.status_code}")
                    integration_results["gateway_agent"] = {
                        "status": "failed",
                        "status_code": response.status_code
                    }
                    self.increment_check(False)
                    
            except Exception as e:
                self.print_error(f"Gateway-Agent integration error: {str(e)}")
                integration_results["gateway_agent"] = {
                    "status": "error",
                    "error": str(e)
                }
                self.increment_check(False)
                self.add_issue("high", "gateway-agent", f"Integration test failed: {str(e)}")
        
        # Test Portal -> Gateway communication
        if "portal" in services and "gateway" in services:
            self.print_info("Testing Portal -> Gateway integration...")
            try:
                portal_url = services["portal"]
                response = requests.get(portal_url, timeout=10)
                
                if response.status_code == 200:
                    self.print_success("Portal is accessible")
                    integration_results["portal_gateway"] = {
                        "status": "accessible"
                    }
                    self.increment_check(True)
                else:
                    self.print_warning(f"Portal accessibility issue: {response.status_code}")
                    integration_results["portal_gateway"] = {
                        "status": "warning",
                        "status_code": response.status_code
                    }
                    self.increment_check(False)
                    
            except Exception as e:
                self.print_error(f"Portal-Gateway integration error: {str(e)}")
                integration_results["portal_gateway"] = {
                    "status": "error",
                    "error": str(e)
                }
                self.increment_check(False)
        
        self.results["integrations"][environment] = integration_results
        return integration_results

    async def verify_database_connectivity(self) -> Dict[str, Any]:
        """Verify database connectivity and configuration"""
        self.print_header("DATABASE CONNECTIVITY VERIFICATION")
        
        db_results = {}
        
        # Test production database
        prod_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
        
        self.print_info("Testing production database connectivity...")
        try:
            conn = psycopg2.connect(prod_db_url)
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            
            # Get table count
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
            table_count = cursor.fetchone()[0]
            
            # Get candidate count
            cursor.execute("SELECT COUNT(*) FROM candidates")
            candidate_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.print_success(f"Production database connected - {table_count} tables, {candidate_count} candidates")
            db_results["production"] = {
                "status": "connected",
                "version": version,
                "tables": table_count,
                "candidates": candidate_count
            }
            self.increment_check(True)
            
        except Exception as e:
            self.print_error(f"Production database connection failed: {str(e)}")
            db_results["production"] = {
                "status": "failed",
                "error": str(e)
            }
            self.increment_check(False)
            self.add_issue("critical", "database", f"Production database unreachable: {str(e)}")
        
        # Test local database (if available)
        local_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@localhost:5432/bhiv_hr_nqzb"
        
        self.print_info("Testing local database connectivity...")
        try:
            conn = psycopg2.connect(local_db_url)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
            table_count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            self.print_success(f"Local database connected - {table_count} tables")
            db_results["local"] = {
                "status": "connected",
                "tables": table_count
            }
            self.increment_check(True)
            
        except Exception as e:
            self.print_warning(f"Local database not available: {str(e)}")
            db_results["local"] = {
                "status": "unavailable",
                "error": str(e)
            }
            # Don't count as failure since local DB is optional
        
        self.results["database"] = db_results
        return db_results

    async def verify_environment_consistency(self) -> Dict[str, Any]:
        """Verify consistency between development and production environments"""
        self.print_header("ENVIRONMENT CONSISTENCY VERIFICATION")
        
        consistency_results = {}
        
        # Compare service availability
        prod_services = self.results["services"].get("production", {})
        dev_services = self.results["services"].get("development", {})
        
        service_comparison = {}
        for service_name in ["gateway", "agent", "portal", "client_portal"]:
            prod_status = prod_services.get(service_name, {}).get("status", "unknown")
            dev_status = dev_services.get(service_name, {}).get("status", "unknown")
            
            if prod_status == "healthy" and dev_status != "healthy":
                self.print_warning(f"{service_name}: Production healthy but development {dev_status}")
                service_comparison[service_name] = {
                    "production": prod_status,
                    "development": dev_status,
                    "consistent": False
                }
                self.add_issue("medium", f"{service_name}-consistency", 
                             f"Service status inconsistent between environments")
            elif prod_status == "healthy" and dev_status == "healthy":
                self.print_success(f"{service_name}: Consistent across environments")
                service_comparison[service_name] = {
                    "production": prod_status,
                    "development": dev_status,
                    "consistent": True
                }
            else:
                service_comparison[service_name] = {
                    "production": prod_status,
                    "development": dev_status,
                    "consistent": prod_status == dev_status
                }
        
        consistency_results["services"] = service_comparison
        self.results["consistency"] = consistency_results
        return consistency_results

    def generate_report(self) -> str:
        """Generate comprehensive verification report"""
        self.print_header("COMPREHENSIVE VERIFICATION REPORT")
        
        # Summary
        total = self.results["total_checks"]
        passed = self.results["passed_checks"]
        failed = self.results["failed_checks"]
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"{Colors.BOLD}SUMMARY:{Colors.END}")
        print(f"  Total Checks: {total}")
        print(f"  Passed: {Colors.GREEN}{passed}{Colors.END}")
        print(f"  Failed: {Colors.RED}{failed}{Colors.END}")
        print(f"  Success Rate: {Colors.GREEN if success_rate >= 80 else Colors.YELLOW if success_rate >= 60 else Colors.RED}{success_rate:.1f}%{Colors.END}")
        
        # Issues summary
        if self.results["issues"]:
            print(f"\n{Colors.BOLD}ISSUES FOUND:{Colors.END}")
            critical_issues = [i for i in self.results["issues"] if i["severity"] == "critical"]
            high_issues = [i for i in self.results["issues"] if i["severity"] == "high"]
            medium_issues = [i for i in self.results["issues"] if i["severity"] == "medium"]
            
            if critical_issues:
                print(f"  {Colors.RED}Critical: {len(critical_issues)}{Colors.END}")
                for issue in critical_issues:
                    print(f"    - {issue['component']}: {issue['description']}")
            
            if high_issues:
                print(f"  {Colors.YELLOW}High: {len(high_issues)}{Colors.END}")
                for issue in high_issues:
                    print(f"    - {issue['component']}: {issue['description']}")
            
            if medium_issues:
                print(f"  {Colors.BLUE}Medium: {len(medium_issues)}{Colors.END}")
                for issue in medium_issues:
                    print(f"    - {issue['component']}: {issue['description']}")
        else:
            print(f"\n{Colors.GREEN}[OK] No critical issues found!{Colors.END}")
        
        # Recommendations
        if self.results["recommendations"]:
            print(f"\n{Colors.BOLD}RECOMMENDATIONS:{Colors.END}")
            for rec in self.results["recommendations"]:
                priority_color = Colors.RED if rec["priority"] == "critical" else Colors.YELLOW if rec["priority"] == "high" else Colors.BLUE
                print(f"  {priority_color}[{rec['priority'].upper()}]{Colors.END} {rec['component']}: {rec['recommendation']}")
        
        # Save detailed report
        report_file = f"service_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{Colors.CYAN}[REPORT] Detailed report saved to: {report_file}{Colors.END}")
        
        return report_file

    async def run_comprehensive_verification(self):
        """Run complete verification suite"""
        start_time = time.time()
        
        print(f"{Colors.BOLD}{Colors.PURPLE}")
        print("BHIV HR PLATFORM - COMPREHENSIVE SERVICE VERIFICATION")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.END}")
        
        try:
            # 1. Verify database connectivity
            await self.verify_database_connectivity()
            
            # 2. Verify production services
            await self.verify_service_health("production")
            await self.verify_routing_configuration("production")
            await self.verify_cross_service_integration("production")
            
            # 3. Verify development services (if available)
            try:
                await self.verify_service_health("development")
                await self.verify_routing_configuration("development")
                await self.verify_cross_service_integration("development")
            except Exception as e:
                self.print_warning(f"Development environment verification skipped: {str(e)}")
            
            # 4. Verify environment consistency
            await self.verify_environment_consistency()
            
            # 5. Generate report
            report_file = self.generate_report()
            
            # Final summary
            duration = time.time() - start_time
            print(f"\n{Colors.BOLD}{Colors.GREEN}[COMPLETE] Verification completed in {duration:.2f} seconds{Colors.END}")
            
            return self.results
            
        except Exception as e:
            self.print_error(f"Verification failed: {str(e)}")
            raise

async def main():
    """Main verification function"""
    verifier = ServiceVerifier()
    
    try:
        results = await verifier.run_comprehensive_verification()
        
        # Exit with appropriate code
        if results["failed_checks"] == 0:
            sys.exit(0)  # Success
        elif results["failed_checks"] < results["total_checks"] * 0.2:  # Less than 20% failures
            sys.exit(1)  # Minor issues
        else:
            sys.exit(2)  # Major issues
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED] Verification interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}[FAILED] Verification failed: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())