#!/usr/bin/env python3
"""Check Deployment Status and Force Update"""

import requests
import json
import time

def check_production_deployment():
    """Check if production deployment has updated"""
    base_url = "https://bhiv-hr-gateway-901a.onrender.com"
    
    print("=== PRODUCTION DEPLOYMENT STATUS ===")
    
    # Check health endpoint for version info
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Service: {data.get('service', 'Unknown')}")
            print(f"Version: {data.get('version', 'Unknown')}")
            print(f"Mode: {data.get('mode', 'Unknown')}")
            print(f"Timestamp: {data.get('timestamp', 'Unknown')}")
            
            # Check if it's still in fallback mode
            if data.get('mode') == 'fallback':
                print("WARNING: Service is still in fallback mode!")
                return False
            elif data.get('mode') == 'production':
                print("SUCCESS: Service is in production mode!")
                return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error checking health: {str(e)}")
        return False

def test_critical_endpoints():
    """Test critical endpoints that HR portal needs"""
    base_url = "https://bhiv-hr-gateway-901a.onrender.com"
    
    critical_endpoints = [
        "/v1/candidates",
        "/v1/jobs", 
        "/v1/interviews",
        "/v1/analytics/dashboard"
    ]
    
    print("\n=== CRITICAL ENDPOINT TEST ===")
    
    working_count = 0
    
    for endpoint in critical_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"OK {endpoint} - Working")
                working_count += 1
            elif response.status_code == 404:
                print(f"FAIL {endpoint} - 404 Not Found")
            else:
                print(f"FAIL {endpoint} - {response.status_code}")
                
        except Exception as e:
            print(f"ERROR {endpoint} - {str(e)}")
    
    success_rate = (working_count / len(critical_endpoints)) * 100
    print(f"\nCritical endpoints working: {working_count}/{len(critical_endpoints)} ({success_rate:.1f}%)")
    
    return success_rate >= 75

def check_openapi_schema():
    """Check OpenAPI schema to see registered endpoints"""
    base_url = "https://bhiv-hr-gateway-901a.onrender.com"
    
    print("\n=== OPENAPI SCHEMA CHECK ===")
    
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=10)
        if response.status_code == 200:
            schema = response.json()
            paths = list(schema.get('paths', {}).keys())
            print(f"Registered endpoints: {len(paths)}")
            
            # Check for critical paths
            critical_paths = ['/v1/candidates', '/v1/jobs', '/v1/interviews']
            missing_paths = [p for p in critical_paths if p not in paths]
            
            if missing_paths:
                print(f"Missing critical paths: {missing_paths}")
                print("This confirms the deployment hasn't updated with the new routes.")
                return False
            else:
                print("All critical paths are registered!")
                return True
        else:
            print(f"Failed to get OpenAPI schema: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error checking OpenAPI schema: {str(e)}")
        return False

def deployment_recommendations():
    """Provide deployment recommendations"""
    print("\n=== DEPLOYMENT RECOMMENDATIONS ===")
    print("1. RENDER DEPLOYMENT ISSUE DETECTED:")
    print("   - Local testing shows 100% success rate")
    print("   - Production still showing fallback mode")
    print("   - New routes not registered in OpenAPI schema")
    print("")
    print("2. SOLUTIONS TO TRY:")
    print("   a) Manual Redeploy:")
    print("      - Go to Render dashboard")
    print("      - Find BHIV HR Gateway service")
    print("      - Click 'Manual Deploy' -> 'Deploy latest commit'")
    print("")
    print("   b) Check Build Logs:")
    print("      - Verify build completed successfully")
    print("      - Check for import errors or deployment failures")
    print("")
    print("   c) Environment Variables:")
    print("      - Ensure all required environment variables are set")
    print("      - Check DATABASE_URL is correctly configured")
    print("")
    print("3. VERIFICATION STEPS:")
    print("   - Wait 2-3 minutes after redeploy")
    print("   - Test /health endpoint for mode='production'")
    print("   - Test /v1/candidates endpoint for 200 response")
    print("   - Check /openapi.json for all registered routes")

if __name__ == "__main__":
    print("Checking production deployment status...")
    
    # Check deployment status
    is_updated = check_production_deployment()
    
    # Test critical endpoints
    endpoints_working = test_critical_endpoints()
    
    # Check OpenAPI schema
    schema_updated = check_openapi_schema()
    
    # Provide recommendations
    if not (is_updated and endpoints_working and schema_updated):
        deployment_recommendations()
    else:
        print("\nSUCCESS: Production deployment is working correctly!")
        print("HR Portal should now be able to access all endpoints.")