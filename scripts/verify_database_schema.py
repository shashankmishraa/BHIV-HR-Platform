#!/usr/bin/env python3
"""
BHIV HR Platform - Database Schema Verification
Checks actual database tables and columns vs expected schema
"""

import psycopg2
from datetime import datetime

DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def verify_database_schema():
    print("BHIV HR Platform - Database Schema Verification")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"TOTAL TABLES FOUND: {len(tables)}")
        print("=" * 40)
        
        expected_tables = {
            'candidates': ['id', 'name', 'email', 'phone', 'location', 'experience_years', 'technical_skills', 'seniority_level', 'education_level', 'resume_path', 'average_score', 'status', 'created_at', 'updated_at'],
            'jobs': ['id', 'title', 'department', 'location', 'experience_level', 'requirements', 'description', 'status', 'client_id', 'created_at', 'updated_at'],
            'feedback': ['id', 'candidate_id', 'job_id', 'integrity', 'honesty', 'discipline', 'hard_work', 'gratitude', 'average_score', 'comments', 'created_at'],
            'interviews': ['id', 'candidate_id', 'job_id', 'interview_date', 'interviewer', 'interview_type', 'notes', 'status', 'created_at'],
            'offers': ['id', 'candidate_id', 'job_id', 'salary', 'start_date', 'terms', 'status', 'created_at', 'updated_at'],
            'users': ['id', 'username', 'email', 'password_hash', 'totp_secret', 'is_2fa_enabled', 'role', 'created_at', 'last_login'],
            'clients': ['id', 'client_id', 'client_name', 'company_name', 'password_hash', 'email', 'phone', 'status', 'totp_secret', 'two_factor_enabled', 'backup_codes', 'password_changed_at', 'password_history', 'failed_login_attempts', 'locked_until', 'created_at', 'updated_at'],
            'audit_logs': ['id', 'user_id', 'client_id', 'action', 'resource', 'ip_address', 'user_agent', 'timestamp', 'details', 'success'],
            'matching_cache': ['id', 'job_id', 'candidate_id', 'match_score', 'algorithm_version', 'created_at'],
            'rate_limits': ['id', 'ip_address', 'endpoint', 'request_count', 'window_start', 'blocked_until']
        }
        
        for table in tables:
            print(f"TABLE: {table}")
            
            # Get columns for this table
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position
            """, (table,))
            
            columns = cursor.fetchall()
            
            if table in expected_tables:
                expected_cols = expected_tables[table]
                actual_cols = [col[0] for col in columns]
                
                missing_cols = set(expected_cols) - set(actual_cols)
                extra_cols = set(actual_cols) - set(expected_cols)
                
                if missing_cols:
                    print(f"  MISSING COLUMNS: {', '.join(missing_cols)}")
                if extra_cols:
                    print(f"  EXTRA COLUMNS: {', '.join(extra_cols)}")
                if not missing_cols and not extra_cols:
                    print(f"  STATUS: COMPLETE ({len(actual_cols)} columns)")
            else:
                print(f"  STATUS: UNEXPECTED TABLE")
            
            print(f"  COLUMNS ({len(columns)}):")
            for col_name, data_type, nullable, default in columns:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                default_str = f" DEFAULT {default}" if default else ""
                print(f"    - {col_name}: {data_type} {null_str}{default_str}")
            
            # Get row count
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  ROWS: {count}")
            except:
                print(f"  ROWS: Unable to count")
            
            print()
        
        # Check for missing expected tables
        missing_tables = set(expected_tables.keys()) - set(tables)
        if missing_tables:
            print("MISSING EXPECTED TABLES:")
            for table in missing_tables:
                print(f"  - {table}")
            print()
        
        # Summary
        print("SCHEMA VERIFICATION SUMMARY:")
        print("=" * 40)
        print(f"Expected tables: {len(expected_tables)}")
        print(f"Actual tables: {len(tables)}")
        print(f"Missing tables: {len(missing_tables)}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    verify_database_schema()