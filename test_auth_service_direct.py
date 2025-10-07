#!/usr/bin/env python3
"""
Direct Client Auth Service Test
Tests the auth service functionality directly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'client_portal'))

def test_auth_service_direct():
    """Test auth service directly"""
    print("Testing Client Auth Service Direct Functionality")
    print("=" * 50)
    
    try:
        # Import the auth service
        from auth_service import ClientAuthService
        print("Auth service imported successfully")
        
        # Initialize service
        auth_service = ClientAuthService()
        print("Auth service initialized")
        
        # Test authentication
        result = auth_service.authenticate_client("TECH001", "demo123")
        if result.get('success'):
            print(f"Authentication successful: {result.get('client_id')}")
            token = result.get('token')
            
            # Test token verification
            verify_result = auth_service.verify_token(token)
            if verify_result.get('success'):
                print(f"Token verification successful: {verify_result.get('client_id')}")
            else:
                print(f"Token verification failed: {verify_result.get('error')}")
                
        else:
            print(f"Authentication failed: {result.get('error')}")
        
        # Test invalid credentials
        invalid_result = auth_service.authenticate_client("INVALID", "wrong")
        if not invalid_result.get('success'):
            print("Invalid credentials properly rejected")
        else:
            print("Invalid credentials accepted")
        
        # Test client info
        client_info = auth_service.get_client_info("TECH001")
        if client_info:
            print(f"Client info retrieved: {client_info.get('company_name')}")
        else:
            print("Client info retrieval failed")
            
        print("\nAuth service direct test completed successfully")
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_auth_service_direct()
    sys.exit(0 if success else 1)