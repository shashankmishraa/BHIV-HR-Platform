#!/usr/bin/env python3
"""
Simple Database Connection Test
"""

import psycopg2

def test_database_connection():
    """Test database connection with new credentials"""
    database_url = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
    
    try:
        print("Testing database connection...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test basic connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("PASS: Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Test database name
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name[0]}")
        
        # Test user
        cursor.execute("SELECT current_user;")
        user = cursor.fetchone()
        print(f"Connected as user: {user[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"FAIL: Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    print(f"Database test result: {'PASS' if success else 'FAIL'}")