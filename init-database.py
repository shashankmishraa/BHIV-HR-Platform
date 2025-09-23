#!/usr/bin/env python3
"""
Database Initialization Script
Creates all required tables for BHIV HR Platform
"""

import os
import sys
from sqlalchemy import create_engine, text

def create_database_tables():
    """Create all required database tables"""
    
    # Use production database URL
    database_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            print("Connected to database successfully")
            
            # Create candidates table
            print("Creating candidates table...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255) UNIQUE,
                    phone VARCHAR(50),
                    location VARCHAR(255),
                    experience_years INTEGER DEFAULT 0,
                    technical_skills TEXT,
                    seniority_level VARCHAR(100),
                    education_level VARCHAR(100),
                    resume_path VARCHAR(500),
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create jobs table
            print("Creating jobs table...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    department VARCHAR(255),
                    location VARCHAR(255),
                    experience_level VARCHAR(100),
                    requirements TEXT,
                    description TEXT,
                    client_id INTEGER DEFAULT 1,
                    employment_type VARCHAR(50) DEFAULT 'Full-time',
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create interviews table
            print("Creating interviews table...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS interviews (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER REFERENCES candidates(id),
                    job_id INTEGER REFERENCES jobs(id),
                    interview_date TIMESTAMP,
                    interviewer VARCHAR(255) DEFAULT 'HR Team',
                    status VARCHAR(50) DEFAULT 'scheduled',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create feedback table
            print("Creating feedback table...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER REFERENCES candidates(id),
                    job_id INTEGER REFERENCES jobs(id),
                    integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
                    honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
                    discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
                    hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
                    gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create client_auth table for client portal
            print("Creating client_auth table...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS client_auth (
                    id SERIAL PRIMARY KEY,
                    client_id VARCHAR(100) UNIQUE NOT NULL,
                    company_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    last_login TIMESTAMP,
                    login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP
                )
            """))
            
            # Create client_sessions table
            print("Creating client_sessions table...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS client_sessions (
                    id SERIAL PRIMARY KEY,
                    client_id VARCHAR(100) NOT NULL,
                    token_hash VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    is_revoked BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (client_id) REFERENCES client_auth(client_id) ON DELETE CASCADE
                )
            """))
            
            # Insert sample data
            print("Inserting sample data...")
            
            # Insert sample jobs
            connection.execute(text("""
                INSERT INTO jobs (title, department, location, experience_level, requirements, description, client_id)
                VALUES 
                    ('Senior Software Engineer', 'Engineering', 'Remote', 'Senior', 'Python, React, AWS', 'Senior software engineer position', 1),
                    ('Data Analyst', 'Analytics', 'New York', 'Mid', 'SQL, Python, Tableau', 'Data analyst role', 1),
                    ('Frontend Developer', 'Engineering', 'San Francisco', 'Mid', 'React, JavaScript, CSS', 'Frontend developer position', 1),
                    ('DevOps Engineer', 'Engineering', 'Remote', 'Senior', 'AWS, Docker, Kubernetes', 'DevOps engineer role', 1)
                ON CONFLICT DO NOTHING
            """))
            
            # Insert sample candidates
            connection.execute(text("""
                INSERT INTO candidates (name, email, phone, location, experience_years, technical_skills, seniority_level, education_level)
                VALUES 
                    ('John Smith', 'john.smith@example.com', '+1-555-0101', 'New York', 5, 'Python, JavaScript, React, AWS', 'Senior Developer', 'Masters'),
                    ('Jane Doe', 'jane.doe@example.com', '+1-555-0102', 'San Francisco', 3, 'React, JavaScript, CSS, HTML', 'Frontend Developer', 'Bachelors'),
                    ('Mike Johnson', 'mike.johnson@example.com', '+1-555-0103', 'Remote', 7, 'Python, SQL, Tableau, Data Analysis', 'Senior Data Analyst', 'Masters'),
                    ('Sarah Wilson', 'sarah.wilson@example.com', '+1-555-0104', 'Boston', 4, 'AWS, Docker, Kubernetes, Python', 'DevOps Engineer', 'Bachelors'),
                    ('David Brown', 'david.brown@example.com', '+1-555-0105', 'Chicago', 6, 'Java, Spring Boot, MySQL, AWS', 'Senior Backend Developer', 'Masters')
                ON CONFLICT (email) DO NOTHING
            """))
            
            # Insert default client
            connection.execute(text("""
                INSERT INTO client_auth (client_id, company_name, email, password_hash)
                VALUES ('TECH001', 'TechCorp Solutions', 'admin@techcorp.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/SJx/6vflO')
                ON CONFLICT (client_id) DO NOTHING
            """))
            
            connection.commit()
            print("All tables created and sample data inserted successfully!")
            
            # Verify tables
            print("\nVerifying tables...")
            result = connection.execute(text("SELECT COUNT(*) FROM candidates"))
            candidate_count = result.fetchone()[0]
            print(f"Candidates table: {candidate_count} records")
            
            result = connection.execute(text("SELECT COUNT(*) FROM jobs"))
            job_count = result.fetchone()[0]
            print(f"Jobs table: {job_count} records")
            
            result = connection.execute(text("SELECT COUNT(*) FROM client_auth"))
            client_count = result.fetchone()[0]
            print(f"Client auth table: {client_count} records")
            
            print(f"\nDatabase initialization complete!")
            print(f"Ready for production use with {candidate_count} candidates and {job_count} jobs")
            
    except Exception as e:
        print(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Initializing BHIV HR Platform Database...")
    print("=" * 50)
    create_database_tables()