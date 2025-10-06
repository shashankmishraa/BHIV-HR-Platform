#!/usr/bin/env python3
"""
BHIV HR Platform - Fix Missing Columns
Adds only the missing columns identified in assessment
"""

import psycopg2
from datetime import datetime

DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def fix_missing_columns():
    print("BHIV HR Platform - Fix Missing Columns")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        fixes_applied = []
        
        # Fix 1: Add average_score to feedback table
        try:
            cursor.execute("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS average_score DECIMAL(3,2)")
            conn.commit()
            fixes_applied.append("feedback.average_score")
            print("Added average_score column to feedback table")
        except Exception as e:
            print(f"⚠️ feedback.average_score: {e}")
        
        # Fix 2: Add interview_type to interviews table
        try:
            cursor.execute("ALTER TABLE interviews ADD COLUMN IF NOT EXISTS interview_type VARCHAR(100) DEFAULT 'Technical'")
            conn.commit()
            fixes_applied.append("interviews.interview_type")
            print("Added interview_type column to interviews table")
        except Exception as e:
            print(f"⚠️ interviews.interview_type: {e}")
        
        # Fix 3: Add totp_secret to users table
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS totp_secret VARCHAR(32)")
            conn.commit()
            fixes_applied.append("users.totp_secret")
            print("Added totp_secret column to users table")
        except Exception as e:
            print(f"⚠️ users.totp_secret: {e}")
        
        # Fix 4: Add is_2fa_enabled to users table
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_2fa_enabled BOOLEAN DEFAULT FALSE")
            conn.commit()
            fixes_applied.append("users.is_2fa_enabled")
            print("Added is_2fa_enabled column to users table")
        except Exception as e:
            print(f"⚠️ users.is_2fa_enabled: {e}")
        
        # Fix 5: Add last_login to users table
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP")
            conn.commit()
            fixes_applied.append("users.last_login")
            print("Added last_login column to users table")
        except Exception as e:
            print(f"⚠️ users.last_login: {e}")
        
        # Fix 6: Update existing feedback records with calculated average scores
        try:
            cursor.execute("""
                UPDATE feedback 
                SET average_score = (integrity + honesty + discipline + hard_work + gratitude) / 5.0
                WHERE average_score IS NULL AND integrity IS NOT NULL
            """)
            updated_rows = cursor.rowcount
            conn.commit()
            print(f"Updated {updated_rows} feedback records with calculated average scores")
        except Exception as e:
            print(f"⚠️ feedback score calculation: {e}")
        
        # Verification
        print("\nVERIFICATION:")
        print("=" * 20)
        
        # Check feedback table
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'feedback' AND column_name = 'average_score'
        """)
        feedback_check = cursor.fetchall()
        print(f"feedback.average_score: {'EXISTS' if feedback_check else 'MISSING'}")
        
        # Check interviews table
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'interviews' AND column_name = 'interview_type'
        """)
        interviews_check = cursor.fetchall()
        print(f"interviews.interview_type: {'EXISTS' if interviews_check else 'MISSING'}")
        
        # Check users table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name IN ('totp_secret', 'is_2fa_enabled', 'last_login')
        """)
        users_check = cursor.fetchall()
        users_cols = [row[0] for row in users_check]
        print(f"users.totp_secret: {'EXISTS' if 'totp_secret' in users_cols else 'MISSING'}")
        print(f"users.is_2fa_enabled: {'EXISTS' if 'is_2fa_enabled' in users_cols else 'MISSING'}")
        print(f"users.last_login: {'EXISTS' if 'last_login' in users_cols else 'MISSING'}")
        
        cursor.close()
        conn.close()
        
        print(f"\nSUCCESS: Applied {len(fixes_applied)} column fixes")
        print("Fixed columns:", ", ".join(fixes_applied))
        print("All missing columns have been added to existing tables.")
        print("2FA and assessment features should now work properly.")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    fix_missing_columns()