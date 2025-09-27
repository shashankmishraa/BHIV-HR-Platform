#!/usr/bin/env python3
"""Simple Database Schema Creator"""

import os
import psycopg2

def create_schema():
    # Use the exact DATABASE_URL from .env.production
    database_url = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
    
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Create candidates table
        print("Creating candidates table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20),
                location VARCHAR(255),
                technical_skills TEXT,
                experience_years INTEGER DEFAULT 0,
                seniority_level VARCHAR(100),
                education_level VARCHAR(100),
                resume_path VARCHAR(500),
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create jobs table
        print("Creating jobs table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                department VARCHAR(100) NOT NULL,
                location VARCHAR(255) NOT NULL,
                experience_level VARCHAR(50) NOT NULL,
                requirements TEXT NOT NULL,
                description TEXT NOT NULL,
                client_id INTEGER DEFAULT 1,
                employment_type VARCHAR(50) DEFAULT 'Full-time',
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create interviews table
        print("Creating interviews table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                id SERIAL PRIMARY KEY,
                candidate_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                interview_date TIMESTAMP,
                interviewer VARCHAR(255) DEFAULT 'HR Team',
                status VARCHAR(50) DEFAULT 'scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create feedback table
        print("Creating feedback table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                candidate_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                integrity INTEGER NOT NULL CHECK (integrity >= 1 AND integrity <= 5),
                honesty INTEGER NOT NULL CHECK (honesty >= 1 AND honesty <= 5),
                discipline INTEGER NOT NULL CHECK (discipline >= 1 AND discipline <= 5),
                hard_work INTEGER NOT NULL CHECK (hard_work >= 1 AND hard_work <= 5),
                gratitude INTEGER NOT NULL CHECK (gratitude >= 1 AND gratitude <= 5),
                comments TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Insert sample data
        print("Inserting sample data...")
        cursor.execute("""
            INSERT INTO jobs (title, department, location, experience_level, requirements, description) VALUES
            ('Software Engineer', 'Engineering', 'Remote', 'Mid-level', 'Python, FastAPI, PostgreSQL', 'Full-stack development role'),
            ('Data Scientist', 'Analytics', 'New York', 'Senior', 'Python, Machine Learning, SQL', 'Data analysis and ML model development'),
            ('Frontend Developer', 'Engineering', 'San Francisco', 'Junior', 'React, JavaScript, CSS', 'User interface development')
            ON CONFLICT DO NOTHING
        """)
        
        cursor.execute("""
            INSERT INTO candidates (name, email, phone, location, technical_skills, experience_years, seniority_level, education_level) VALUES
            ('John Doe', 'john.doe@example.com', '+1-555-0101', 'New York', 'Python, FastAPI, PostgreSQL, React', 3, 'Mid-level', 'Bachelor''s'),
            ('Jane Smith', 'jane.smith@example.com', '+1-555-0102', 'San Francisco', 'JavaScript, React, Node.js, MongoDB', 2, 'Junior', 'Bachelor''s'),
            ('Mike Johnson', 'mike.johnson@example.com', '+1-555-0103', 'Remote', 'Python, Machine Learning, TensorFlow, SQL', 5, 'Senior', 'Master''s')
            ON CONFLICT (email) DO NOTHING
        """)
        
        # Commit changes
        conn.commit()
        
        # Verify tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"SUCCESS: Created {len(tables)} tables")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count} records")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_schema()
    exit(0 if success else 1)