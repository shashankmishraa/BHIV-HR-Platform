-- BHIV HR Platform - Complete Database Schema
-- Supports all API endpoints and enterprise features

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Candidates table (existing, enhanced)
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    location VARCHAR(255),
    experience_years INTEGER DEFAULT 0,
    technical_skills TEXT,
    seniority_level VARCHAR(100),
    education_level VARCHAR(255),
    resume_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table (enhanced)
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    location VARCHAR(255),
    experience_level VARCHAR(100),
    requirements TEXT,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    client_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feedback/Values Assessment table
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
    honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
    discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
    hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
    gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
    average_score DECIMAL(3,2),
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interviews table
CREATE TABLE IF NOT EXISTS interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    interview_date TIMESTAMP,
    interview_type VARCHAR(100),
    notes TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job Offers table
CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    salary DECIMAL(12,2),
    start_date DATE,
    terms TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Client authentication table (enhanced for Week 2)
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    client_name VARCHAR(255),
    password_hash VARCHAR(255),
    email VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    -- Week 2: 2FA fields
    totp_secret VARCHAR(255),
    two_factor_enabled BOOLEAN DEFAULT false,
    backup_codes TEXT,
    -- Week 2: Password policy fields
    password_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password_history TEXT,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Matching results cache (optional)
CREATE TABLE IF NOT EXISTS matching_cache (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id),
    candidate_id INTEGER REFERENCES candidates(id),
    match_score DECIMAL(5,2),
    algorithm_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email);
CREATE INDEX IF NOT EXISTS idx_candidates_skills ON candidates USING gin(to_tsvector('english', technical_skills));
CREATE INDEX IF NOT EXISTS idx_candidates_location ON candidates(location);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_client ON jobs(client_id);
CREATE INDEX IF NOT EXISTS idx_feedback_candidate ON feedback(candidate_id);
CREATE INDEX IF NOT EXISTS idx_feedback_job ON feedback(job_id);
CREATE INDEX IF NOT EXISTS idx_interviews_date ON interviews(interview_date);
CREATE INDEX IF NOT EXISTS idx_offers_status ON offers(status);

-- Insert sample data for testing
INSERT INTO jobs (title, department, location, experience_level, requirements, description, status) VALUES
('Senior Python Developer', 'Engineering', 'Remote', 'Senior', 'Python, Django, PostgreSQL, 5+ years experience', 'We are looking for a senior Python developer to join our team...', 'active'),
('Data Scientist', 'Analytics', 'New York', 'Mid-Level', 'Python, Machine Learning, SQL, 3+ years experience', 'Join our data science team to build predictive models...', 'active'),
('Frontend Developer', 'Engineering', 'San Francisco', 'Junior', 'React, JavaScript, HTML/CSS, 2+ years experience', 'Build amazing user interfaces with React...', 'active')
ON CONFLICT DO NOTHING;

-- Insert sample clients (enhanced for Week 2)
INSERT INTO clients (client_id, client_name, password_hash, email, status, password_changed_at) VALUES
('TECH001', 'Tech Innovations Inc', 'hashed_google123', 'contact@techinnovations.com', 'active', NOW()),
('STARTUP01', 'Startup Ventures', 'hashed_startup123', 'hello@startupventures.com', 'active', NOW()),
('ENTERPRISE01', 'Enterprise Solutions', 'hashed_enterprise123', 'admin@enterprisesolutions.com', 'active', NOW())
ON CONFLICT DO NOTHING;

-- Update trigger for updated_at columns
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON candidates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();