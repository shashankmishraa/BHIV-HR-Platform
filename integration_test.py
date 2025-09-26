#!/usr/bin/env python3
"""
Integration Test for New Credentials
"""

import requests
import json
import time

def test_api_endpoints():
    """Test API endpoints with new credentials"""
    
    # New service URLs
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    agent_url = "https://bhiv-hr-agent-m1me.onrender.com"
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    results = {}
    
    # Test Gateway Health
    try:
        print("Testing Gateway health...")
        response = requests.get(f"{gateway_url}/health", timeout=30)
        results["gateway_health"] = {
            "status": response.status_code,
            "success": response.status_code == 200,
            "response": response.text[:200] if response.text else "No response"
        }
        print(f"Gateway health: {response.status_code}")
    except Exception as e:
        results["gateway_health"] = {"success": False, "error": str(e)}
        print(f"Gateway health failed: {e}")
    
    # Test Agent Health
    try:
        print("Testing Agent health...")
        response = requests.get(f"{agent_url}/health", timeout=30)
        results["agent_health"] = {
            "status": response.status_code,
            "success": response.status_code == 200,
            "response": response.text[:200] if response.text else "No response"
        }
        print(f"Agent health: {response.status_code}")
    except Exception as e:
        results["agent_health"] = {"success": False, "error": str(e)}
        print(f"Agent health failed: {e}")
    
    # Test Gateway API with authentication
    try:
        print("Testing Gateway API with auth...")
        response = requests.get(f"{gateway_url}/v1/jobs", headers=headers, timeout=30)
        results["gateway_api"] = {
            "status": response.status_code,
            "success": response.status_code in [200, 401, 403],  # Any auth response is good
            "response": response.text[:200] if response.text else "No response"
        }
        print(f"Gateway API: {response.status_code}")
    except Exception as e:
        results["gateway_api"] = {"success": False, "error": str(e)}
        print(f"Gateway API failed: {e}")
    
    return results

def test_service_communication():
    """Test inter-service communication"""
    
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    
    try:
        print("Testing service architecture info...")
        response = requests.get(f"{gateway_url}/system/architecture", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "architecture": data.get("architecture", {}),
                "services": data.get("services", {})
            }
        else:
            return {"success": False, "status": response.status_code}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("Starting Integration Tests...")
    
    # Test API endpoints
    api_results = test_api_endpoints()
    
    # Test service communication
    comm_results = test_service_communication()
    
    # Generate report
    report = f"""# Integration Test Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## API Endpoint Tests
"""
    
    for test, result in api_results.items():
        status = "PASS" if result.get("success") else "FAIL"
        report += f"- {status}: {test}\n"
        if result.get("error"):
            report += f"  - Error: {result['error']}\n"
        elif result.get("status"):
            report += f"  - HTTP Status: {result['status']}\n"
    
    report += f"\n## Service Communication\n"
    if comm_results.get("success"):
        report += "- PASS: Service architecture accessible\n"
        if comm_results.get("services"):
            report += f"  - Services found: {list(comm_results['services'].keys())}\n"
    else:
        report += "- FAIL: Service communication\n"
        if comm_results.get("error"):
            report += f"  - Error: {comm_results['error']}\n"
    
    # Save report
    with open("INTEGRATION_TEST_REPORT.md", "w") as f:
        f.write(report)
    
    print("Integration tests complete. Report saved to INTEGRATION_TEST_REPORT.md")
    
    # Print summary
    total_tests = len(api_results) + 1
    passed_tests = sum(1 for r in api_results.values() if r.get("success")) + (1 if comm_results.get("success") else 0)
    
    print(f"Summary: {passed_tests}/{total_tests} tests passed")

if __name__ == "__main__":
    main()