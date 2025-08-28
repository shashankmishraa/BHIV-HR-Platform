#!/usr/bin/env python3
"""Initialize database tables for BHIV HR Platform"""

import psycopg2
import time
import os

def wait_for_db():
    """Wait for database to be ready"""
    for i in range(30):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="bhiv_hr",
                user="bhiv_user",
                password="bhiv_pass"
            )
            conn.close()
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            print(f"⏳ Waiting for database (attempt {i+1}/30): {e}")
            time.sleep(1)
    return False

def create_tables():
    """Create all required tables"""
    if not wait_for_db():
        print("❌ Database not available")
        return False
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="bhiv_hr",
            user="bhiv_user",
            password="bhiv_pass"
        )
        cur = conn.cursor()
        
        # Create interviews table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                id SERIAL PRIMARY KEY,
                candidate_id INTEGER REFERENCES candidates(id),
                job_id INTEGER REFERENCES jobs(id),
                interview_date TIMESTAMP,
                interviewer VARCHAR(255),
                status VARCHAR(50) DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create offers table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id SERIAL PRIMARY KEY,
                candidate_id INTEGER REFERENCES candidates(id),
                job_id INTEGER REFERENCES jobs(id),
                salary INTEGER,
                status VARCHAR(50) DEFAULT 'sent',
                offer_date TIMESTAMP DEFAULT NOW(),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    create_tables()