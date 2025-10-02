#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Service Routing & Connection Audit
Verifies all internal/external endpoints, routing logic, and integration points
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
import os
import re

class ServiceRoutingAuditor:
    def __init__(self):
        # Production URLs
        self.services = {
            "gateway": "https://bhiv-hr-gateway-46pz.onrender.com",
            "agent": "https://bhiv-hr-agent-m1me.onrender.com", 
            "portal": "https://bhiv-hr-portal-cead.onrender.com",
            "client_portal": "https://bhiv-hr-client-portal-5g33.onrender.com"
        }
        
        # Local development URLs
        self.local_services = {
            "gateway": "http://localhost:8000",
            "agent": "http://localhost:9000",
            "portal": "http://localhost:8501", 
            "client_portal": "http://localhost:8502"
        }
        
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Audit results
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "service_connectivity": {},
            "routing_validation": {},
            "integration_points": {},
            "misconfigurations": [],
            "broken_links": [],
            "missing_routes": [],
            "recommendations": []
        }

    def log_finding(self, category: str, service: str, status: str, details: str):
        """Log audit finding"""
        if category not in self.audit_results:
            self.audit_results[category] = {}
        
        if service not in self.audit_results[category]:
            self.audit_results[category][service] = []
            
        self.audit_results[category][service].append({
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"[{status}] {category}/{service}: {details}")

    def test_service_connectivity(self, environment="production"):
        """Test connectivity to all services"""
        print(f"\n=== TESTING {environment.upper()} SERVICE CONNECTIVITY ===")
        
        services = self.services if environment == "production" else self.local_services
        
        for service_name, base_url in services.items():
            print(f"\n--- Testing {service_name} at {base_url} ---")
            
            # Test basic connectivity
            try:
                if service_name in ["portal", "client_portal"]:
                    # Streamlit health endpoint
                    health_url = f"{base_url}/_stcore/health"
                else:
                    # FastAPI health endpoint
                    health_url = f"{base_url}/health"
                
                response = requests.get(health_url, timeout=10)
                if response.status_code == 200:
                    self.log_finding("service_connectivity", service_name, "CONNECTED", 
                                   f"Service accessible at {base_url}")
                else:
                    self.log_finding("service_connectivity", service_name, "FAILED", 
                                   f"HTTP {response.status_code} at {health_url}")
                    
            except requests.exceptions.ConnectionError:
                self.log_finding("service_connectivity", service_name, "UNREACHABLE", 
                               f"Cannot connect to {base_url}")
            except requests.exceptions.Timeout:
                self.log_finding("service_connectivity", service_name, "TIMEOUT", 
                               f"Timeout connecting to {base_url}")
            except Exception as e:
                self.log_finding("service_connectivity", service_name, "ERROR", 
                               f"Error: {str(e)}")

    def audit_gateway_routes(self):
        """Audit all Gateway API routes"""
        print("\n=== AUDITING GATEWAY ROUTES ===")
        
        gateway_url = self.services["gateway"]
        
        # Expected route categories with endpoints
        expected_routes = {
            "core": ["/", "/health", "/test-candidates"],
            "jobs": ["/v1/jobs"],
            "candidates": ["/v1/candidates/job/1", "/v1/candidates/search", "/v1/candidates/bulk"],
            "matching": ["/v1/match/1/top"],
            "assessment": ["/v1/feedback", "/v1/interviews"],
            "analytics": ["/candidates/stats", "/v1/reports/job/1/export.csv"],
            "client": ["/v1/client/login"],
            "security": ["/v1/security/rate-limit-status", "/v1/security/blocked-ips"],
            "2fa": ["/v1/2fa/setup", "/v1/2fa/status/TECH001"],
            "password": ["/v1/password/validate", "/v1/password/policy"],
            "monitoring": ["/metrics", "/health/detailed", "/metrics/dashboard"]
        }
        
        for category, routes in expected_routes.items():
            print(f"\n--- Testing {category} routes ---")
            for route in routes:
                self.test_route_accessibility(gateway_url, route, category)

    def test_route_accessibility(self, base_url: str, route: str, category: str):
        """Test if a specific route is accessible"""
        url = f"{base_url}{route}"
        
        try:
            # Use GET for most routes, POST for specific ones
            if route in ["/v1/jobs", "/v1/candidates/bulk", "/v1/feedback", "/v1/interviews"]:
                # Test with minimal valid data
                test_data = self.get_test_data_for_route(route)
                response = requests.post(url, json=test_data, headers=self.headers, timeout=10)
            else:
                response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code in [200, 201]:
                self.log_finding("routing_validation", category, "✅ ACCESSIBLE", 
                               f"{route} returns {response.status_code}")
            elif response.status_code == 401:
                self.log_finding("routing_validation", category, "🔒 AUTH_REQUIRED", 
                               f"{route} requires authentication (expected)")
            elif response.status_code == 404:
                self.log_finding("routing_validation", category, "❌ NOT_FOUND", 
                               f"{route} returns 404 - route may be missing")
                self.audit_results["missing_routes"].append(route)
            else:
                self.log_finding("routing_validation", category, "⚠️ UNEXPECTED", 
                               f"{route} returns {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_finding("routing_validation", category, "❌ CONNECTION_FAILED", 
                           f"Cannot reach {url}")
            self.audit_results["broken_links"].append(url)
        except Exception as e:
            self.log_finding("routing_validation", category, "❌ ERROR", 
                           f"{route}: {str(e)}")

    def get_test_data_for_route(self, route: str) -> dict:
        """Get minimal test data for POST routes"""
        if route == "/v1/jobs":
            return {
                "title": "Test Job",
                "department": "Engineering", 
                "location": "Remote",
                "experience_level": "Mid",
                "requirements": "Python",
                "description": "Test"
            }
        elif route == "/v1/candidates/bulk":
            return {
                "candidates": [{
                    "name": "Test Candidate",
                    "email": "test@example.com",
                    "skills": ["Python"]
                }]
            }
        elif route == "/v1/feedback":
            return {
                "candidate_id": 1,
                "job_id": 1,
                "integrity": 4,
                "honesty": 4,
                "discipline": 4,
                "hard_work": 4,
                "gratitude": 4
            }
        elif route == "/v1/interviews":
            return {
                "candidate_id": 1,
                "job_id": 1,
                "interview_date": "2025-01-15T10:00:00",
                "interviewer": "Test"
            }
        return {}

    def audit_agent_routes(self):
        """Audit AI Agent service routes"""
        print("\n=== AUDITING AI AGENT ROUTES ===")
        
        agent_url = self.services["agent"]
        agent_routes = ["/", "/health", "/test-db", "/match", "/analyze/1"]
        
        for route in agent_routes:
            if route == "/match":
                # POST route
                try:
                    response = requests.post(f"{agent_url}{route}", 
                                           json={"job_id": 1}, timeout=15)
                    if response.status_code == 200:
                        self.log_finding("routing_validation", "agent", "✅ ACCESSIBLE", 
                                       f"{route} working correctly")
                    else:
                        self.log_finding("routing_validation", "agent", "⚠️ ISSUE", 
                                       f"{route} returns {response.status_code}")
                except Exception as e:
                    self.log_finding("routing_validation", "agent", "❌ ERROR", 
                                   f"{route}: {str(e)}")
            else:
                # GET route
                self.test_route_accessibility(agent_url, route, "agent")

    def audit_portal_integration(self):
        """Audit portal integration and internal routing"""
        print("\n=== AUDITING PORTAL INTEGRATION ===")
        
        # Test portal accessibility
        for portal_name in ["portal", "client_portal"]:
            portal_url = self.services[portal_name]
            
            # Test Streamlit health endpoint
            try:
                response = requests.get(f"{portal_url}/_stcore/health", timeout=10)
                if response.status_code == 200:
                    self.log_finding("integration_points", portal_name, "✅ ACCESSIBLE", 
                                   "Portal health endpoint working")
                else:
                    self.log_finding("integration_points", portal_name, "❌ FAILED", 
                                   f"Health check failed: {response.status_code}")
            except Exception as e:
                self.log_finding("integration_points", portal_name, "❌ ERROR", 
                               f"Portal connection error: {str(e)}")

    def test_cross_service_integration(self):
        """Test integration between services"""
        print("\n=== TESTING CROSS-SERVICE INTEGRATION ===")
        
        # Test Gateway -> Agent communication
        try:
            gateway_to_agent = requests.get(f"{self.services['gateway']}/v1/match/1/top", 
                                          headers=self.headers, timeout=15)
            if gateway_to_agent.status_code == 200:
                self.log_finding("integration_points", "gateway_to_agent", "✅ WORKING", 
                               "Gateway successfully communicates with AI Agent")
            else:
                self.log_finding("integration_points", "gateway_to_agent", "❌ FAILED", 
                               f"Gateway->Agent communication failed: {gateway_to_agent.status_code}")
        except Exception as e:
            self.log_finding("integration_points", "gateway_to_agent", "❌ ERROR", 
                           f"Integration error: {str(e)}")
        
        # Test Database connectivity through Gateway
        try:
            db_test = requests.get(f"{self.services['gateway']}/test-candidates", 
                                 headers=self.headers, timeout=10)
            if db_test.status_code == 200:
                data = db_test.json()
                candidate_count = data.get("total_candidates", 0)
                self.log_finding("integration_points", "gateway_to_database", "✅ WORKING", 
                               f"Database accessible, {candidate_count} candidates")
            else:
                self.log_finding("integration_points", "gateway_to_database", "❌ FAILED", 
                               f"Database connection failed: {db_test.status_code}")
        except Exception as e:
            self.log_finding("integration_points", "gateway_to_database", "❌ ERROR", 
                           f"Database integration error: {str(e)}")

    def check_environment_consistency(self):
        """Check consistency between development and production"""
        print("\n=== CHECKING ENVIRONMENT CONSISTENCY ===")
        
        # Test both environments
        print("Testing production environment...")
        self.test_service_connectivity("production")
        
        print("\nTesting local development environment...")
        self.test_service_connectivity("development")
        
        # Compare results
        prod_results = self.audit_results["service_connectivity"]
        
        # Reset for dev testing
        dev_audit = ServiceRoutingAuditor()
        dev_audit.test_service_connectivity("development")
        dev_results = dev_audit.audit_results["service_connectivity"]
        
        # Compare connectivity
        for service in self.services.keys():
            prod_status = "UNKNOWN"
            dev_status = "UNKNOWN"
            
            if service in prod_results and prod_results[service]:
                prod_status = prod_results[service][0]["status"]
            
            if service in dev_results and dev_results[service]:
                dev_status = dev_results[service][0]["status"]
            
            if prod_status == dev_status:
                self.log_finding("integration_points", "environment_consistency", "✅ CONSISTENT", 
                               f"{service}: Both environments have same status")
            else:
                self.log_finding("integration_points", "environment_consistency", "⚠️ INCONSISTENT", 
                               f"{service}: Prod={prod_status}, Dev={dev_status}")

    def identify_misconfigurations(self):
        """Identify potential misconfigurations"""
        print("\n=== IDENTIFYING MISCONFIGURATIONS ===")
        
        # Check for common misconfigurations
        misconfigs = []
        
        # Check if all services are using HTTPS in production
        for service_name, url in self.services.items():
            if not url.startswith("https://"):
                misconfigs.append(f"{service_name}: Not using HTTPS in production")
        
        # Check for consistent port usage in development
        expected_ports = {
            "gateway": "8000",
            "agent": "9000", 
            "portal": "8501",
            "client_portal": "8502"
        }
        
        for service_name, expected_port in expected_ports.items():
            local_url = self.local_services[service_name]
            if f":{expected_port}" not in local_url:
                misconfigs.append(f"{service_name}: Unexpected port in local development")
        
        # Check for missing authentication on sensitive endpoints
        sensitive_endpoints = ["/v1/jobs", "/v1/candidates/bulk", "/v1/feedback"]
        for endpoint in sensitive_endpoints:
            try:
                # Test without authentication
                response = requests.get(f"{self.services['gateway']}{endpoint}", timeout=5)
                if response.status_code != 401:
                    misconfigs.append(f"{endpoint}: May not require authentication (got {response.status_code})")
            except:
                pass  # Connection errors are expected
        
        self.audit_results["misconfigurations"] = misconfigs
        
        for config in misconfigs:
            self.log_finding("integration_points", "misconfigurations", "⚠️ FOUND", config)

    def generate_recommendations(self):
        """Generate recommendations based on audit findings"""
        print("\n=== GENERATING RECOMMENDATIONS ===")
        
        recommendations = []
        
        # Check for broken links
        if self.audit_results["broken_links"]:
            recommendations.append(f"Fix {len(self.audit_results['broken_links'])} broken service links")
        
        # Check for missing routes
        if self.audit_results["missing_routes"]:
            recommendations.append(f"Implement {len(self.audit_results['missing_routes'])} missing routes")
        
        # Check for misconfigurations
        if self.audit_results["misconfigurations"]:
            recommendations.append(f"Address {len(self.audit_results['misconfigurations'])} configuration issues")
        
        # Performance recommendations
        recommendations.extend([
            "Implement health check endpoints for all services",
            "Add request/response logging for debugging",
            "Set up monitoring for cross-service communication",
            "Implement circuit breakers for service resilience",
            "Add API versioning for backward compatibility"
        ])
        
        self.audit_results["recommendations"] = recommendations
        
        for rec in recommendations:
            print(f"RECOMMENDATION: {rec}")

    def run_comprehensive_audit(self):
        """Run complete routing and connection audit"""
        print("BHIV HR Platform - Service Routing & Connection Audit")
        print("=" * 70)
        
        # Test service connectivity
        self.test_service_connectivity("production")
        
        # Audit routing for each service
        self.audit_gateway_routes()
        self.audit_agent_routes()
        self.audit_portal_integration()
        
        # Test integration points
        self.test_cross_service_integration()
        
        # Check environment consistency
        self.check_environment_consistency()
        
        # Identify issues
        self.identify_misconfigurations()
        
        # Generate recommendations
        self.generate_recommendations()
        
        return self.audit_results

    def save_audit_report(self, filename: str = "service_routing_audit_report.json"):
        """Save audit report to file"""
        with open(filename, 'w') as f:
            json.dump(self.audit_results, f, indent=2)
        print(f"\nAudit report saved to: {filename}")

if __name__ == "__main__":
    auditor = ServiceRoutingAuditor()
    results = auditor.run_comprehensive_audit()
    
    print("\n" + "=" * 70)
    print("AUDIT SUMMARY")
    print("=" * 70)
    
    # Count findings
    total_issues = len(results["broken_links"]) + len(results["missing_routes"]) + len(results["misconfigurations"])
    
    print(f"Broken Links: {len(results['broken_links'])}")
    print(f"Missing Routes: {len(results['missing_routes'])}")
    print(f"Misconfigurations: {len(results['misconfigurations'])}")
    print(f"Total Issues: {total_issues}")
    print(f"Recommendations: {len(results['recommendations'])}")
    
    if total_issues == 0:
        print("\n✅ No critical routing or connection issues found!")
    else:
        print(f"\n⚠️ Found {total_issues} issues that need attention")
    
    auditor.save_audit_report()