-- BHIV HR Platform - Complete Fixed Database Schema
-- Addresses all database issues for Docker and Render deployments

-- Connect to the database
\c bhiv_hr_nqzb;

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS interviews CASCADE;
DROP TABLE IF EXISTS client_sessions CASCADE;
DROP TABLE IF EXISTS client_auth CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS candidates CASCADE;

-- Candidates table (FIXED)
CREATE TABLE candidates (
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
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table (FIXED)
CREATE TABLE jobs (
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

-- Interviews table (MISSING - NOW ADDED)
CREATE TABLE interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    interview_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    interviewer VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feedback table (MISSING - NOW ADDED)
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
    honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
    discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
    hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
    gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
    overall_score DECIMAL(3,2) GENERATED ALWAYS AS ((integrity + honesty + discipline + hard_work + gratitude) / 5.0) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Client authentication table
CREATE TABLE client_auth (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP
);

-- Client sessions table
CREATE TABLE client_sessions (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (client_id) REFERENCES client_auth(client_id) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidates_status ON candidates(status);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_interviews_candidate_id ON interviews(candidate_id);
CREATE INDEX idx_interviews_job_id ON interviews(job_id);
CREATE INDEX idx_feedback_candidate_id ON feedback(candidate_id);
CREATE INDEX idx_feedback_job_id ON feedback(job_id);

-- Grant all permissions to bhiv_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bhiv_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bhiv_user;

-- Insert sample data
INSERT INTO candidates (name, email, phone, location, experience_years, technical_skills, seniority_level, education_level) VALUES
('John Doe', 'john.doe@example.com', '+1-555-0101', 'New York, NY', 5, 'Python, Django, PostgreSQL, Docker', 'Senior', 'Bachelor of Computer Science'),
('Jane Smith', 'jane.smith@example.com', '+1-555-0102', 'San Francisco, CA', 3, 'JavaScript, React, Node.js, MongoDB', 'Mid-Level', 'Master of Software Engineering'),
('Bob Johnson', 'bob.johnson@example.com', '+1-555-0103', 'Austin, TX', 7, 'Java, Spring Boot, MySQL, AWS', 'Senior', 'Bachelor of Information Technology'),
('Alice Brown', 'alice.brown@example.com', '+1-555-0104', 'Remote', 2, 'Python, FastAPI, Machine Learning', 'Junior', 'Bachelor of Data Science'),
('Charlie Wilson', 'charlie.wilson@example.com', '+1-555-0105', 'Seattle, WA', 4, 'Go, Kubernetes, Docker, DevOps', 'Mid-Level', 'Bachelor of Computer Engineering')
ON CONFLICT (email) DO NOTHING;

INSERT INTO jobs (title, department, location, experience_level, requirements, description, client_id) VALUES
('Senior Python Developer', 'Engineering', 'Remote', 'Senior', 'Python, Django, PostgreSQL, 5+ years experience', 'We are looking for a senior Python developer to join our team and build scalable web applications.', 'TECH001'),
('Data Scientist', 'Analytics', 'New York, NY', 'Mid-Level', 'Python, Machine Learning, SQL, 3+ years experience', 'Join our data science team to build predictive models and extract insights from large datasets.', 'TECH001'),
('Frontend Developer', 'Engineering', 'San Francisco, CA', 'Junior', 'React, JavaScript, HTML/CSS, 2+ years experience', 'Build amazing user interfaces with React and modern frontend technologies.', 'TECH001'),
('DevOps Engineer', 'Infrastructure', 'Austin, TX', 'Mid-Level', 'AWS, Docker, Kubernetes, CI/CD, 3+ years experience', 'Manage our cloud infrastructure and deployment pipelines.', 'TECH001'),
('Full Stack Developer', 'Engineering', 'Remote', 'Mid-Level', 'JavaScript, Node.js, React, MongoDB, 3+ years experience', 'Work on both frontend and backend development for our web applications.', 'TECH001')
ON CONFLICT DO NOTHING;

INSERT INTO client_auth (client_id, company_name, email, password_hash) VALUES
('TECH001', 'Tech Solutions Inc', 'admin@techsolutions.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcQjyPHSS')
ON CONFLICT (client_id) DO NOTHING;

-- Insert sample interviews
INSERT INTO interviews (candidate_id, job_id, interview_date, status, notes, interviewer) VALUES
(1, 1, '2025-01-20 10:00:00', 'scheduled', 'Technical interview for Python developer position', 'John Manager'),
(2, 3, '2025-01-21 14:00:00', 'scheduled', 'Frontend skills assessment', 'Sarah Lead'),
(3, 4, '2025-01-22 11:00:00', 'scheduled', 'DevOps technical discussion', 'Mike Senior')
ON CONFLICT DO NOTHING;

-- Insert sample feedback
INSERT INTO feedback (candidate_id, job_id, integrity, honesty, discipline, hard_work, gratitude) VALUES
(1, 1, 5, 5, 4, 5, 4),
(2, 3, 4, 5, 5, 4, 5),
(3, 4, 5, 4, 5, 5, 4)
ON CONFLICT DO NOTHING;

COMMIT;