#!/usr/bin/env python3
"""Initialize database tables for BHIV HR Platform"""

import psycopg2
import time
import os

def wait_for_db():
    """Wait for database to be ready"""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', '5432'))
    db_name = os.getenv('POSTGRES_DB', 'bhiv_hr')
    db_user = os.getenv('POSTGRES_USER', 'bhiv_user')
    db_pass = os.getenv('POSTGRES_PASSWORD', 'bhiv_pass')
    
    for i in range(30):
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_pass
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
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('POSTGRES_DB', 'bhiv_hr'),
            user=os.getenv('POSTGRES_USER', 'bhiv_user'),
            password=os.getenv('POSTGRES_PASSWORD', 'bhiv_pass')
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