#!/usr/bin/env python3
"""
Database Schema Creator
Creates missing database tables and resolves Priority 1 issue
"""

import os
import psycopg2
from datetime import datetime


def create_database_schema():
    """Create database schema with all required tables"""

    # Database connection
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb",
    )

    try:
        print("Connecting to database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Create candidates table
        print("Creating candidates table...")
        cursor.execute(
            """
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
        """
        )

        # Create jobs table
        print("Creating jobs table...")
        cursor.execute(
            """
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
        """
        )

        # Create interviews table
        print("Creating interviews table...")
        cursor.execute(
            """
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
        """
        )

        # Create feedback table
        print("Creating feedback table...")
        cursor.execute(
            """
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
        """
        )

        # Create indexes
        print("Creating indexes...")
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status)",
            "CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email)",
            "CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)",
            "CREATE INDEX IF NOT EXISTS idx_interviews_candidate_job ON interviews(candidate_id, job_id)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_candidate_job ON feedback(candidate_id, job_id)",
        ]

        for index_sql in indexes:
            cursor.execute(index_sql)

        # Insert sample data
        print("Inserting sample data...")

        # Sample jobs
        cursor.execute(
            """
            INSERT INTO jobs (title, department, location, experience_level, requirements, description) VALUES
            ('Software Engineer', 'Engineering', 'Remote', 'Mid-level', 'Python, FastAPI, PostgreSQL', 'Full-stack development role'),
            ('Data Scientist', 'Analytics', 'New York', 'Senior', 'Python, Machine Learning, SQL', 'Data analysis and ML model development'),
            ('Frontend Developer', 'Engineering', 'San Francisco', 'Junior', 'React, JavaScript, CSS', 'User interface development')
            ON CONFLICT DO NOTHING
        """
        )

        # Sample candidates
        cursor.execute(
            """
            INSERT INTO candidates (name, email, phone, location, technical_skills, experience_years, seniority_level, education_level) VALUES
            ('John Doe', 'john.doe@example.com', '+1-555-0101', 'New York', 'Python, FastAPI, PostgreSQL, React', 3, 'Mid-level', 'Bachelor''s'),
            ('Jane Smith', 'jane.smith@example.com', '+1-555-0102', 'San Francisco', 'JavaScript, React, Node.js, MongoDB', 2, 'Junior', 'Bachelor''s'),
            ('Mike Johnson', 'mike.johnson@example.com', '+1-555-0103', 'Remote', 'Python, Machine Learning, TensorFlow, SQL', 5, 'Senior', 'Master''s')
            ON CONFLICT (email) DO NOTHING
        """
        )

        # Commit changes
        conn.commit()

        # Verify table creation
        print("\nVerifying table creation...")
        cursor.execute(
            """
            SELECT 'candidates' as table_name, COUNT(*) as record_count FROM candidates
            UNION ALL
            SELECT 'jobs' as table_name, COUNT(*) as record_count FROM jobs
            UNION ALL
            SELECT 'interviews' as table_name, COUNT(*) as record_count FROM interviews
            UNION ALL
            SELECT 'feedback' as table_name, COUNT(*) as record_count FROM feedback
        """
        )

        results = cursor.fetchall()
        print("\nTable verification results:")
        for table_name, count in results:
            print(f"  {table_name}: {count} records")

        print(f"\n✅ Database schema created successfully at {datetime.now()}")
        return True

    except Exception as e:
        print(f"❌ Error creating database schema: {str(e)}")
        return False

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    success = create_database_schema()
    if success:
        print("\n🎯 Next step: Test database endpoints")
    else:
        print("\n⚠️ Schema creation failed - check database connectivity")
