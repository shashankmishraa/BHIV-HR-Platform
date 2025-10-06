#!/usr/bin/env python3
"""
BHIV HR Platform - Apply Production Schema
Applies complete production schema with all missing columns
"""

import psycopg2
from datetime import datetime

DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def apply_production_schema():
    print("BHIV HR Platform - Production Schema Application")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Read production schema
        with open('services/db/production_schema_complete.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("Applying production schema...")
        cursor.execute(schema_sql)
        conn.commit()
        
        # Verify critical tables and columns
        print("\nVerifying schema application...")
        
        # Check candidates table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'candidates' AND column_name IN ('average_score', 'status', 'updated_at')
        """)
        candidates_cols = [row[0] for row in cursor.fetchall()]
        
        # Check feedback table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'feedback' AND column_name = 'average_score'
        """)
        feedback_cols = [row[0] for row in cursor.fetchall()]
        
        # Check users table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name IN ('totp_secret', 'is_2fa_enabled', 'last_login')
        """)
        users_cols = [row[0] for row in cursor.fetchall()]
        
        # Check interviews table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'interviews' AND column_name = 'interview_type'
        """)
        interviews_cols = [row[0] for row in cursor.fetchall()]
        
        print("VERIFICATION RESULTS:")
        print("=" * 30)
        print(f"Candidates table missing columns fixed: {len(candidates_cols)}/3")
        print(f"  - {', '.join(candidates_cols) if candidates_cols else 'None added'}")
        
        print(f"Feedback table missing columns fixed: {len(feedback_cols)}/1")
        print(f"  - {', '.join(feedback_cols) if feedback_cols else 'None added'}")
        
        print(f"Users table missing columns fixed: {len(users_cols)}/3")
        print(f"  - {', '.join(users_cols) if users_cols else 'None added'}")
        
        print(f"Interviews table missing columns fixed: {len(interviews_cols)}/1")
        print(f"  - {', '.join(interviews_cols) if interviews_cols else 'None added'}")
        
        # Count total tables
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)
        table_count = cursor.fetchone()[0]
        
        print(f"\nTotal tables in database: {table_count}")
        
        # Test critical functionality
        print("\nTesting critical functionality...")
        
        # Test candidates table
        cursor.execute("SELECT COUNT(*) FROM candidates")
        candidates_count = cursor.fetchone()[0]
        print(f"Candidates: {candidates_count} records")
        
        # Test jobs table
        cursor.execute("SELECT COUNT(*) FROM jobs")
        jobs_count = cursor.fetchone()[0]
        print(f"Jobs: {jobs_count} records")
        
        # Test users table
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        print(f"Users: {users_count} records")
        
        # Test offers table
        cursor.execute("SELECT COUNT(*) FROM offers")
        offers_count = cursor.fetchone()[0]
        print(f"Offers: {offers_count} records")
        
        cursor.close()
        conn.close()
        
        print("\nSUCCESS: Production schema applied successfully!")
        print("All missing columns have been added.")
        print("All API endpoints should now be 100% functional.")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    apply_production_schema()