-- BHIV HR Platform - Database Schema Creation Script
-- Run this script in Render PostgreSQL console to create missing tables

-- Create candidates table
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
);

-- Create jobs table
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
);

-- Create interviews table
CREATE TABLE IF NOT EXISTS interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    interview_date TIMESTAMP,
    interviewer VARCHAR(255) DEFAULT 'HR Team',
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Create feedback table
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
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);
CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_interviews_candidate_job ON interviews(candidate_id, job_id);
CREATE INDEX IF NOT EXISTS idx_feedback_candidate_job ON feedback(candidate_id, job_id);

-- Insert sample data for testing
INSERT INTO jobs (title, department, location, experience_level, requirements, description) VALUES
('Software Engineer', 'Engineering', 'Remote', 'Mid-level', 'Python, FastAPI, PostgreSQL', 'Full-stack development role'),
('Data Scientist', 'Analytics', 'New York', 'Senior', 'Python, Machine Learning, SQL', 'Data analysis and ML model development'),
('Frontend Developer', 'Engineering', 'San Francisco', 'Junior', 'React, JavaScript, CSS', 'User interface development')
ON CONFLICT DO NOTHING;

INSERT INTO candidates (name, email, phone, location, technical_skills, experience_years, seniority_level, education_level) VALUES
('John Doe', 'john.doe@example.com', '+1-555-0101', 'New York', 'Python, FastAPI, PostgreSQL, React', 3, 'Mid-level', 'Bachelor''s'),
('Jane Smith', 'jane.smith@example.com', '+1-555-0102', 'San Francisco', 'JavaScript, React, Node.js, MongoDB', 2, 'Junior', 'Bachelor''s'),
('Mike Johnson', 'mike.johnson@example.com', '+1-555-0103', 'Remote', 'Python, Machine Learning, TensorFlow, SQL', 5, 'Senior', 'Master''s')
ON CONFLICT (email) DO NOTHING;

-- Verify table creation
SELECT 'candidates' as table_name, COUNT(*) as record_count FROM candidates
UNION ALL
SELECT 'jobs' as table_name, COUNT(*) as record_count FROM jobs
UNION ALL
SELECT 'interviews' as table_name, COUNT(*) as record_count FROM interviews
UNION ALL
SELECT 'feedback' as table_name, COUNT(*) as record_count FROM feedback;