#!/usr/bin/env python3
"""
Test Enhanced Authentication System
Comprehensive testing of the new authentication system with all methods and fallbacks
"""

import sys
import os
import asyncio
import requests
import json
from datetime import datetime

# Add the services directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services', 'gateway', 'app'))

def test_enhanced_authentication_system():
    """Test the enhanced authentication system"""
    
    print("🔐 Testing Enhanced Authentication System")
    print("=" * 60)
    
    # Test configuration
    base_url = "http://localhost:8000"  # Local development
    production_url = "https://bhiv-hr-gateway.onrender.com"  # Production
    
    # Test both local and production if available
    test_urls = [base_url, production_url]
    
    for url in test_urls:
        print(f"\n🌐 Testing URL: {url}")
        print("-" * 40)
        
        try:
            # Test 1: Enhanced Authentication Test Endpoint (No Auth Required)
            print("1️⃣ Testing Enhanced Authentication System...")
            response = requests.get(f"{url}/v1/auth/test-enhanced", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Enhanced Auth Available: {result.get('enhanced_auth_available', False)}")
                
                if result.get('enhanced_auth_available'):
                    test_summary = result.get('test_summary', {})
                    print(f"   📊 Test Results: {test_summary.get('passed_tests', 0)}/{test_summary.get('total_tests', 0)} passed")
                    
                    # Show detailed test results
                    test_results = result.get('test_results', {})
                    for test_name, test_data in test_results.items():
                        status = "✅" if test_data.get('success') else "❌"
                        print(f"      {status} {test_name}: {test_data.get('method', 'N/A')} - {test_data.get('level', 'N/A')}")
                else:
                    print(f"   ⚠️ Fallback Mode: {result.get('message', 'Unknown')}")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text[:100]}")
        
        except requests.exceptions.RequestException as e:
            print(f"   🔌 Connection Error: {str(e)}")
            continue
        
        try:
            # Test 2: Authentication Status with Production API Key
            print("\n2️⃣ Testing Authentication Status with Production Key...")
            headers = {
                "Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
            }
            response = requests.get(f"{url}/v1/auth/status", headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                auth_system = result.get('authentication_system', 'unknown')
                print(f"   ✅ Authentication System: {auth_system}")
                
                if 'current_authentication' in result:
                    current_auth = result['current_authentication']
                    print(f"   🔑 Method: {current_auth.get('method', 'unknown')}")
                    print(f"   📊 Level: {current_auth.get('level', 'unknown')}")
                    print(f"   👤 User: {current_auth.get('user_id', 'unknown')}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"   🔌 Connection Error: {str(e)}")
        
        try:
            # Test 3: Authentication Status with Demo API Key
            print("\n3️⃣ Testing Authentication Status with Demo Key...")
            headers = {
                "Authorization": "Bearer myverysecureapikey123"
            }
            response = requests.get(f"{url}/v1/auth/status", headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                auth_system = result.get('authentication_system', 'unknown')
                print(f"   ✅ Authentication System: {auth_system}")
                
                if 'current_authentication' in result:
                    current_auth = result['current_authentication']
                    print(f"   🔑 Method: {current_auth.get('method', 'unknown')}")
                    print(f"   📊 Level: {current_auth.get('level', 'unknown')}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"   🔌 Connection Error: {str(e)}")
        
        try:
            # Test 4: Authentication Status without API Key (Fallback Test)
            print("\n4️⃣ Testing Fallback Authentication...")
            response = requests.get(f"{url}/v1/auth/status", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Fallback Success: {result.get('authentication_system', 'unknown')}")
            elif response.status_code == 401:
                print(f"   ✅ Proper Authentication Required (Expected in Production)")
            else:
                print(f"   ⚠️ Unexpected Response: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"   🔌 Connection Error: {str(e)}")
        
        try:
            # Test 5: JWT Token Generation and Validation
            print("\n5️⃣ Testing JWT Token Generation...")
            headers = {
                "Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
            }
            
            # Generate JWT token
            response = requests.post(
                f"{url}/v1/auth/tokens/generate",
                headers=headers,
                params={"user_id": "test_user", "permissions": ["read", "write"]},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                jwt_token = result.get('access_token')
                print(f"   ✅ JWT Generated: {jwt_token[:20]}..." if jwt_token else "   ❌ No token in response")
                
                if jwt_token:
                    # Validate the generated JWT token
                    validate_response = requests.get(
                        f"{url}/v1/auth/tokens/validate",
                        headers=headers,
                        params={"token": jwt_token},
                        timeout=10
                    )
                    
                    if validate_response.status_code == 200:
                        validate_result = validate_response.json()
                        print(f"   ✅ JWT Validation: {validate_result.get('token_valid', False)}")
                        if validate_result.get('enhanced_validation'):
                            print(f"   🚀 Enhanced Validation Active")
                    else:
                        print(f"   ❌ JWT Validation Failed: {validate_response.status_code}")
            else:
                print(f"   ❌ JWT Generation Failed: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"   🔌 Connection Error: {str(e)}")
        
        try:
            # Test 6: User Info with Enhanced Authentication
            print("\n6️⃣ Testing User Info with Enhanced Authentication...")
            headers = {
                "Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
            }
            response = requests.get(f"{url}/v1/auth/user/info", headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                enhanced_auth = result.get('enhanced_auth', False)
                print(f"   ✅ Enhanced Auth: {enhanced_auth}")
                
                if enhanced_auth and 'authentication_details' in result:
                    auth_details = result['authentication_details']
                    print(f"   🔑 Method: {auth_details.get('method', 'unknown')}")
                    print(f"   📊 Level: {auth_details.get('level', 'unknown')}")
                    print(f"   🌍 Environment: {auth_details.get('environment', 'unknown')}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"   🔌 Connection Error: {str(e)}")
        
        print(f"\n✅ Completed testing for {url}")

def test_authentication_methods():
    """Test different authentication methods"""
    
    print("\n🔐 Testing Authentication Methods")
    print("=" * 60)
    
    # Import the enhanced authentication system for direct testing
    try:
        from enhanced_auth_system import enhanced_auth_system, AuthenticationMethod, AuthenticationLevel
        
        print("1️⃣ Testing API Key Validation...")
        
        # Test production API key
        prod_result = enhanced_auth_system.validate_api_key("prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
        print(f"   Production Key: {prod_result.success} - {prod_result.method.value} - {prod_result.level.name}")
        
        # Test demo API key
        demo_result = enhanced_auth_system.validate_api_key("myverysecureapikey123")
        print(f"   Demo Key: {demo_result.success} - {demo_result.method.value} - {demo_result.level.name}")
        
        # Test invalid API key (should trigger fallback)
        invalid_result = enhanced_auth_system.validate_api_key("invalid_key")
        print(f"   Invalid Key: {invalid_result.success} - {invalid_result.method.value} - {invalid_result.level.name}")
        
        print("\n2️⃣ Testing JWT Token Generation and Validation...")
        
        # Generate JWT token
        jwt_token = enhanced_auth_system.generate_jwt_token("test_user", ["read", "write"])
        print(f"   JWT Generated: {jwt_token[:30]}...")
        
        # Validate JWT token
        jwt_result = enhanced_auth_system.validate_jwt_token(jwt_token)
        print(f"   JWT Validation: {jwt_result.success} - {jwt_result.method.value} - {jwt_result.level.name}")
        
        print("\n3️⃣ Testing System Status...")
        
        # Get system status
        status = enhanced_auth_system.get_system_status()
        print(f"   Environment: {status['environment']}")
        print(f"   Fallback Enabled: {status['fallback_enabled']}")
        print(f"   Active Sessions: {status['active_sessions']}")
        print(f"   Production Keys: {status['production_keys_count']}")
        print(f"   Development Keys: {status['development_keys_count']}")
        
        print("\n✅ Direct testing completed successfully!")
        
    except ImportError as e:
        print(f"❌ Could not import enhanced authentication system: {e}")
        print("   This is expected if running outside the application context")

if __name__ == "__main__":
    print("🚀 Enhanced Authentication System Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    
    # Test the authentication system via HTTP endpoints
    test_enhanced_authentication_system()
    
    # Test the authentication system directly (if possible)
    test_authentication_methods()
    
    print("\n" + "=" * 60)
    print("🎉 Test Suite Completed!")
    print(f"Test completed at: {datetime.now()}")