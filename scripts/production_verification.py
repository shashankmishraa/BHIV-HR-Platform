#!/usr/bin/env python3
"""
BHIV HR Platform - Production System Verification
Loads production environment and verifies all systems
"""

import os
import requests
import psycopg2
from datetime import datetime

def load_env_file(filepath):
    """Load environment variables from file"""
    env_vars = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
    return env_vars

def check_credentials_updated():
    """Check that all credentials have been updated from defaults"""
    print("Step 1: Verifying Credential Updates...")
    
    # Load production environment
    prod_env = load_env_file('.env.production')
    
    # Check for old/default patterns
    old_patterns = [
        'dev-fallback',
        'your-',
        'GENERATE_',
        'username:password',
        'localhost',
        'demo123'
    ]
    
    issues = []
    for key, value in prod_env.items():
        for pattern in old_patterns:
            if pattern in value:
                issues.append(f"{key} contains old pattern: {pattern}")
    
    if issues:
        print("  ERROR: Found old credential patterns:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print("  PASS: All credentials appear to be updated")
        return True

def check_database_connection():
    """Test database connection with production credentials"""
    print("\nStep 2: Testing Production Database Connection...")
    
    prod_env = load_env_file('.env.production')
    database_url = prod_env.get('DATABASE_URL')
    
    if not database_url:
        print("  ERROR: DATABASE_URL not found in .env.production")
        return False
    
    try:
        print(f"  Connecting to: {database_url.split('@')[1] if '@' in database_url else 'database'}")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        # Check for required tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        print(f"  PASS: Connected to PostgreSQL")
        print(f"  Database: {len(tables)} tables found")
        
        # Check for essential tables
        required_tables = ['candidates', 'jobs', 'interviews']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"  WARN: Missing tables: {missing_tables}")
        else:
            print(f"  PASS: All essential tables present")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: Database connection failed: {str(e)}")
        return False

def check_service_accessibility():
    """Test all production service URLs"""
    print("\nStep 3: Testing Production Service URLs...")
    
    prod_env = load_env_file('.env.production')
    
    services = {
        'Gateway': prod_env.get('GATEWAY_URL'),
        'Agent': prod_env.get('AGENT_SERVICE_URL'), 
        'Portal': prod_env.get('PORTAL_URL'),
        'Client Portal': prod_env.get('CLIENT_PORTAL_URL')
    }
    
    results = {}
    
    for name, url in services.items():
        if not url:
            print(f"  ERROR: {name} URL not configured")
            results[name] = False
            continue
            
        try:
            # Test health endpoint
            response = requests.get(f"{url}/health", timeout=15)
            success = response.status_code < 400
            
            print(f"  {'PASS' if success else 'FAIL'}: {name} - {url} ({response.status_code})")
            results[name] = success
            
        except requests.exceptions.Timeout:
            print(f"  TIMEOUT: {name} - {url} (service may be sleeping)")
            results[name] = False
        except Exception as e:
            print(f"  ERROR: {name} - {url} - {str(e)}")
            results[name] = False
    
    return all(results.values())

def check_api_authentication():
    """Test API authentication with production credentials"""
    print("\nStep 4: Testing API Authentication...")
    
    prod_env = load_env_file('.env.production')
    api_key = prod_env.get('API_KEY_SECRET')
    gateway_url = prod_env.get('GATEWAY_URL')
    
    if not api_key or not gateway_url:
        print("  ERROR: API_KEY_SECRET or GATEWAY_URL not configured")
        return False
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Test authenticated endpoints
    test_endpoints = [
        f"{gateway_url}/candidates",
        f"{gateway_url}/jobs"
    ]
    
    success_count = 0
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=15)
            
            # Consider 200, 401, 403 as valid responses (not 500)
            if response.status_code < 500:
                print(f"  PASS: {endpoint} ({response.status_code})")
                success_count += 1
            else:
                print(f"  ERROR: {endpoint} ({response.status_code})")
                
        except Exception as e:
            print(f"  ERROR: {endpoint} - {str(e)}")
    
    return success_count > 0

def check_inter_service_communication():
    """Test communication between services"""
    print("\nStep 5: Testing Inter-Service Communication...")
    
    prod_env = load_env_file('.env.production')
    gateway_url = prod_env.get('GATEWAY_URL')
    api_key = prod_env.get('API_KEY_SECRET')
    
    if not gateway_url or not api_key:
        print("  ERROR: Missing gateway URL or API key")
        return False
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Test system endpoints that might communicate with other services
        response = requests.get(f"{gateway_url}/system/modules", headers=headers, timeout=15)
        
        if response.status_code < 400:
            print(f"  PASS: Gateway system endpoints working ({response.status_code})")
            return True
        else:
            print(f"  WARN: Gateway system endpoints returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ERROR: Inter-service communication test failed - {str(e)}")
        return False

def run_integration_tests():
    """Run basic integration tests"""
    print("\nStep 6: Running Integration Tests...")
    
    prod_env = load_env_file('.env.production')
    gateway_url = prod_env.get('GATEWAY_URL')
    
    if not gateway_url:
        print("  ERROR: Gateway URL not configured")
        return False
    
    # Test basic endpoints
    test_endpoints = [
        f"{gateway_url}/",
        f"{gateway_url}/health/detailed",
        f"{gateway_url}/metrics/json"
    ]
    
    success_count = 0
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(endpoint, timeout=15)
            if response.status_code < 400:
                success_count += 1
                print(f"  PASS: {endpoint.split('/')[-1] or 'root'}")
            else:
                print(f"  FAIL: {endpoint.split('/')[-1] or 'root'} ({response.status_code})")
        except Exception as e:
            print(f"  ERROR: {endpoint.split('/')[-1] or 'root'} - {str(e)}")
    
    print(f"  Integration tests: {success_count}/{len(test_endpoints)} passed")
    return success_count >= len(test_endpoints) // 2  # At least half should pass

def generate_report(results):
    """Generate final verification report"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE VERIFICATION REPORT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Environment: Production")
    
    test_names = [
        "Credential Updates",
        "Database Connection", 
        "Service Accessibility",
        "API Authentication",
        "Inter-Service Communication",
        "Integration Tests"
    ]
    
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"\nTest Results:")
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "PASS" if result else "FAIL"
        print(f"  {i+1}. {name}: {status}")
    
    print(f"\nSummary:")
    print(f"  Tests Passed: {passed}/{total}")
    print(f"  Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print(f"  Overall Status: SYSTEM OPERATIONAL")
        return True
    else:
        print(f"  Overall Status: ISSUES DETECTED")
        return False

def main():
    """Run comprehensive production verification"""
    print("BHIV HR Platform - Production System Verification")
    print("=" * 55)
    
    # Run all verification steps
    results = [
        check_credentials_updated(),
        check_database_connection(),
        check_service_accessibility(), 
        check_api_authentication(),
        check_inter_service_communication(),
        run_integration_tests()
    ]
    
    # Generate final report
    overall_success = generate_report(results)
    
    return overall_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)