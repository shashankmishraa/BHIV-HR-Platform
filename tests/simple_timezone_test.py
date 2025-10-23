#!/usr/bin/env python3
"""
Simple test to verify timezone fix in client portal authentication
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services', 'client_portal'))

from auth_service import ClientAuthService
from datetime import datetime, timezone
import jwt

def test_timezone_fix():
    """Test that timezone fix resolves JWT token issues"""
    print("Testing Timezone Fix for Client Portal Authentication")
    print("=" * 55)
    
    try:
        # Initialize auth service
        auth_service = ClientAuthService()
        print("PASS | Auth service initialized successfully")
        
        # Test authentication with default client
        result = auth_service.authenticate_client("TECH001", "demo123")
        
        if result.get('success'):
            token = result.get('token')
            print("PASS | Authentication successful")
            print(f"PASS | JWT token generated: {token[:50]}...")
            
            # Verify token can be decoded
            try:
                payload = jwt.decode(token, auth_service.jwt_secret, algorithms=[auth_service.jwt_algorithm])
                print("PASS | JWT token decoded successfully")
                print(f"  - Client ID: {payload.get('client_id')}")
                print(f"  - Company: {payload.get('company_name')}")
                print(f"  - Issued at: {datetime.fromtimestamp(payload.get('iat'), timezone.utc)}")
                print(f"  - Expires at: {datetime.fromtimestamp(payload.get('exp'), timezone.utc)}")
                
                # Test token verification
                verify_result = auth_service.verify_token(token)
                if verify_result.get('success'):
                    print("PASS | Token verification successful")
                    print("PASS | TIMEZONE FIX WORKING CORRECTLY")
                    return True
                else:
                    print(f"FAIL | Token verification failed: {verify_result.get('error')}")
                    return False
                    
            except jwt.ExpiredSignatureError:
                print("FAIL | JWT token expired")
                return False
            except jwt.InvalidTokenError as e:
                print(f"FAIL | JWT token invalid: {e}")
                return False
                
        else:
            print(f"FAIL | Authentication failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"FAIL | Test failed with error: {e}")
        return False

def main():
    success = test_timezone_fix()
    
    print("\n" + "=" * 55)
    if success:
        print("RESULT: Timezone fix is working correctly!")
        print("Client portal authentication should now work properly.")
    else:
        print("RESULT: Timezone fix needs more work.")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()