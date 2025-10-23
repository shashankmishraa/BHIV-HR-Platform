#!/usr/bin/env python3
"""
Direct test of client login bypassing auth service to isolate timezone issue
"""

import psycopg2
import bcrypt
import jwt
from datetime import datetime, timedelta

# Database connection
DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def test_direct_client_login():
    """Test client login directly with database"""
    print("Direct Client Login Test")
    print("=" * 30)
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check clients table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'clients'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print(f"Clients table has {len(columns)} columns:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        # Get client data
        cursor.execute("""
            SELECT client_id, company_name, password_hash, status, failed_login_attempts, locked_until
            FROM clients WHERE client_id = %s
        """, ("TECH001",))
        
        client = cursor.fetchone()
        
        if client:
            print(f"\nClient found: {client[0]} - {client[1]}")
            print(f"Status: {client[3]}")
            print(f"Failed attempts: {client[4]}")
            print(f"Locked until: {client[5]} (type: {type(client[5])})")
            
            # Test timezone comparison
            if client[5]:
                print(f"Locked until timezone info: {client[5].tzinfo}")
                current_time = datetime.utcnow()
                print(f"Current time: {current_time} (type: {type(current_time)})")
                print(f"Current time timezone info: {current_time.tzinfo}")
                
                try:
                    is_locked = client[5] > current_time
                    print(f"Is locked: {is_locked}")
                except Exception as e:
                    print(f"Timezone comparison error: {e}")
            
            # Test password verification
            if client[2]:  # password_hash exists
                test_password = "demo123"
                try:
                    password_valid = bcrypt.checkpw(test_password.encode('utf-8'), client[2].encode('utf-8'))
                    print(f"Password valid: {password_valid}")
                except Exception as e:
                    print(f"Password verification error: {e}")
            else:
                print("No password hash found - using demo password")
            
            # Generate JWT token
            jwt_secret = "fallback_jwt_secret_key_for_client_auth_2025"
            token_payload = {
                "client_id": client[0],
                "company_name": client[1],
                "exp": int(datetime.utcnow().timestamp()) + 86400  # 24 hours
            }
            access_token = jwt.encode(token_payload, jwt_secret, algorithm="HS256")
            print(f"JWT token generated: {access_token[:50]}...")
            
            print("\nSUCCESS: Direct client login working")
            return True
        else:
            print("FAIL: Client not found")
            return False
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"FAIL: Direct login test error: {e}")
        return False

if __name__ == "__main__":
    test_direct_client_login()