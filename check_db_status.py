#!/usr/bin/env python3
"""
Quick Database Status Checker
Checks what tables and data currently exist in PostgreSQL
"""

import os
import psycopg2
from datetime import datetime

def check_database_status():
    """Check current database status and contents"""
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL", 
        "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
    
    try:
        print("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if tables exist
        print("\nChecking existing tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        if tables:
            print("Found tables:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("No tables found")
            return
        
        # Check table contents
        print("\nChecking table contents...")
        
        expected_tables = ['candidates', 'jobs', 'interviews', 'feedback']
        
        for table_name in expected_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   {table_name}: {count} records")
                
                # Show sample data for non-empty tables
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    print(f"     Columns: {', '.join(columns)}")
                    for i, row in enumerate(rows, 1):
                        print(f"     Sample {i}: {dict(zip(columns, row))}")
                    
            except Exception as e:
                print(f"   {table_name}: Error - {str(e)}")
        
        # Check database info
        print(f"\nDatabase Info:")
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"   PostgreSQL Version: {version}")
        
        cursor.execute("SELECT current_database()")
        db_name = cursor.fetchone()[0]
        print(f"   Database Name: {db_name}")
        
        cursor.execute("SELECT current_user")
        user = cursor.fetchone()[0]
        print(f"   Current User: {user}")
        
        print(f"\nDatabase check completed at {datetime.now()}")
        
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        print("   This likely means tables haven't been created yet")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database_status()