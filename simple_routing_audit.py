#!/usr/bin/env python3
"""
BHIV HR Platform - Service Routing & Connection Audit (Simple Version)
"""

import requests
import json
from datetime import datetime

def test_service_connectivity():
    """Test all service connections"""
    print("=== TESTING SERVICE CONNECTIVITY ===")
    
    services = {
        "Gateway": "https://bhiv-hr-gateway-46pz.onrender.com/health",
        "AI Agent": "https://bhiv-hr-agent-m1me.onrender.com/health",
        "HR Portal": "https://bhiv-hr-portal-cead.onrender.com/_stcore/health",
        "Client Portal": "https://bhiv-hr-client-portal-5g33.onrender.com/_stcore/health"
    }
    
    results = {}
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                results[service] = "CONNECTED"
                print(f"[PASS] {service}: Connected successfully")
            else:
                results[service] = f"FAILED - HTTP {response.status_code}"
                print(f"[FAIL] {service}: HTTP {response.status_code}")
        except Exception as e:
            results[service] = f"ERROR - {str(e)}"
            print(f"[ERROR] {service}: {str(e)}")
    
    return results

def test_gateway_routes():
    """Test Gateway API routes"""
    print("\n=== TESTING GATEWAY ROUTES ===")
    
    base_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    routes = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/test-candidates", "Database test"),
        ("/v1/jobs", "Jobs endpoint"),
        ("/v1/candidates/search", "Candidate search"),
        ("/metrics", "Prometheus metrics"),
        ("/health/detailed", "Detailed health")
    ]
    
    results = {}
    
    for route, description in routes:
        try:
            response = requests.get(f"{base_url}{route}", headers=headers, timeout=10)
            if response.status_code == 200:
                results[route] = "ACCESSIBLE"
                print(f"[PASS] {route}: {description} - Accessible")
            elif response.status_code == 401:
                results[route] = "AUTH_REQUIRED"
                print(f"[AUTH] {route}: {description} - Authentication required")
            else:
                results[route] = f"HTTP_{response.status_code}"
                print(f"[WARN] {route}: {description} - HTTP {response.status_code}")
        except Exception as e:
            results[route] = f"ERROR"
            print(f"[ERROR] {route}: {description} - {str(e)}")
    
    return results

def test_ai_agent_routes():
    """Test AI Agent routes"""
    print("\n=== TESTING AI AGENT ROUTES ===")
    
    base_url = "https://bhiv-hr-agent-m1me.onrender.com"
    
    routes = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/test-db", "Database test")
    ]
    
    results = {}
    
    for route, description in routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=10)
            if response.status_code == 200:
                results[route] = "ACCESSIBLE"
                print(f"[PASS] {route}: {description} - Accessible")
            else:
                results[route] = f"HTTP_{response.status_code}"
                print(f"[WARN] {route}: {description} - HTTP {response.status_code}")
        except Exception as e:
            results[route] = "ERROR"
            print(f"[ERROR] {route}: {description} - {str(e)}")
    
    # Test AI matching endpoint
    try:
        response = requests.post(f"{base_url}/match", json={"job_id": 1}, timeout=15)
        if response.status_code == 200:
            results["/match"] = "WORKING"
            print("[PASS] /match: AI matching - Working")
        else:
            results["/match"] = f"HTTP_{response.status_code}"
            print(f"[WARN] /match: AI matching - HTTP {response.status_code}")
    except Exception as e:
        results["/match"] = "ERROR"
        print(f"[ERROR] /match: AI matching - {str(e)}")
    
    return results

def test_integration_points():
    """Test service integration"""
    print("\n=== TESTING SERVICE INTEGRATION ===")
    
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    results = {}
    
    # Test Gateway -> Database
    try:
        response = requests.get(f"{gateway_url}/test-candidates", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidate_count = data.get("total_candidates", 0)
            results["gateway_to_database"] = f"WORKING - {candidate_count} candidates"
            print(f"[PASS] Gateway->Database: Working ({candidate_count} candidates)")
        else:
            results["gateway_to_database"] = f"FAILED - HTTP {response.status_code}"
            print(f"[FAIL] Gateway->Database: HTTP {response.status_code}")
    except Exception as e:
        results["gateway_to_database"] = f"ERROR - {str(e)}"
        print(f"[ERROR] Gateway->Database: {str(e)}")
    
    # Test Gateway -> AI Agent (via matching)
    try:
        response = requests.get(f"{gateway_url}/v1/match/1/top", headers=headers, timeout=15)
        if response.status_code == 200:
            results["gateway_to_agent"] = "WORKING"
            print("[PASS] Gateway->AI Agent: Working")
        else:
            results["gateway_to_agent"] = f"FAILED - HTTP {response.status_code}"
            print(f"[FAIL] Gateway->AI Agent: HTTP {response.status_code}")
    except Exception as e:
        results["gateway_to_agent"] = f"ERROR - {str(e)}"
        print(f"[ERROR] Gateway->AI Agent: {str(e)}")
    
    return results

def generate_audit_report():
    """Generate comprehensive audit report"""
    print("BHIV HR Platform - Service Routing & Connection Audit")
    print("=" * 60)
    
    # Run all tests
    service_results = test_service_connectivity()
    gateway_results = test_gateway_routes()
    agent_results = test_ai_agent_routes()
    integration_results = test_integration_points()
    
    # Generate summary
    print("\n" + "=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)
    
    # Count results
    total_services = len(service_results)
    connected_services = sum(1 for status in service_results.values() if status == "CONNECTED")
    
    total_routes = len(gateway_results) + len(agent_results)
    working_routes = sum(1 for status in list(gateway_results.values()) + list(agent_results.values()) 
                        if status in ["ACCESSIBLE", "WORKING", "AUTH_REQUIRED"])
    
    total_integrations = len(integration_results)
    working_integrations = sum(1 for status in integration_results.values() if "WORKING" in status)
    
    print(f"Service Connectivity: {connected_services}/{total_services} services connected")
    print(f"Route Accessibility: {working_routes}/{total_routes} routes working")
    print(f"Service Integration: {working_integrations}/{total_integrations} integrations working")
    
    # Detailed results
    print(f"\nSERVICE STATUS:")
    for service, status in service_results.items():
        print(f"  {service}: {status}")
    
    print(f"\nROUTE STATUS:")
    print("  Gateway Routes:")
    for route, status in gateway_results.items():
        print(f"    {route}: {status}")
    
    print("  AI Agent Routes:")
    for route, status in agent_results.items():
        print(f"    {route}: {status}")
    
    print(f"\nINTEGRATION STATUS:")
    for integration, status in integration_results.items():
        print(f"  {integration}: {status}")
    
    # Generate recommendations
    print(f"\nRECOMMENDATIONS:")
    
    if connected_services == total_services:
        print("  - All services are connected and accessible")
    else:
        print(f"  - Fix {total_services - connected_services} disconnected services")
    
    if working_routes == total_routes:
        print("  - All routes are properly configured")
    else:
        print(f"  - Review {total_routes - working_routes} non-working routes")
    
    if working_integrations == total_integrations:
        print("  - All service integrations are working")
    else:
        print(f"  - Fix {total_integrations - working_integrations} integration issues")
    
    print("  - Monitor service health regularly")
    print("  - Implement automated health checks")
    print("  - Add request/response logging for debugging")
    
    # Save results
    audit_data = {
        "timestamp": datetime.now().isoformat(),
        "service_connectivity": service_results,
        "gateway_routes": gateway_results,
        "agent_routes": agent_results,
        "integration_points": integration_results,
        "summary": {
            "services_connected": f"{connected_services}/{total_services}",
            "routes_working": f"{working_routes}/{total_routes}",
            "integrations_working": f"{working_integrations}/{total_integrations}"
        }
    }
    
    with open("service_audit_report.json", "w") as f:
        json.dump(audit_data, f, indent=2)
    
    print(f"\nAudit report saved to: service_audit_report.json")
    
    return audit_data

if __name__ == "__main__":
    generate_audit_report()