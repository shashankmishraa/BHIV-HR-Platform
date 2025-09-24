-- BHIV HR Platform - Fixed Database Schema for Docker
\c bhiv_hr_nqzb;

-- Create missing tables with proper structure
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
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    interview_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    interviewer VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
    honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
    discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
    hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
    gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS client_auth (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bhiv_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bhiv_user;

-- Insert sample data
INSERT INTO candidates (name, email, technical_skills, experience_years, location) VALUES
('John Doe', 'john@example.com', 'Python, FastAPI, PostgreSQL', 5, 'New York'),
('Jane Smith', 'jane@example.com', 'JavaScript, React, Node.js', 3, 'San Francisco'),
('Bob Johnson', 'bob@example.com', 'Java, Spring Boot, AWS', 7, 'Austin')
ON CONFLICT (email) DO NOTHING;

INSERT INTO jobs (title, department, location, experience_level, requirements, description, client_id) VALUES
('Senior Python Developer', 'Engineering', 'Remote', 'Senior', 'Python, FastAPI, PostgreSQL', 'Senior Python developer position', 'TECH001'),
('Frontend Developer', 'Engineering', 'Remote', 'Mid-Level', 'React, JavaScript, HTML/CSS', 'Frontend developer position', 'TECH001'),
('DevOps Engineer', 'Infrastructure', 'Remote', 'Mid-Level', 'AWS, Docker, Kubernetes', 'DevOps engineer position', 'TECH001')
ON CONFLICT DO NOTHING;

INSERT INTO client_auth (client_id, company_name, email, password_hash) VALUES
('TECH001', 'Tech Solutions Inc', 'admin@techsolutions.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcQjyPHSS')
ON CONFLICT (client_id) DO NOTHING;

INSERT INTO interviews (candidate_id, job_id, interview_date, status, interviewer) VALUES
(1, 1, '2025-01-20 10:00:00', 'scheduled', 'John Manager'),
(2, 2, '2025-01-21 14:00:00', 'scheduled', 'Sarah Lead'),
(3, 3, '2025-01-22 11:00:00', 'scheduled', 'Mike Senior')
ON CONFLICT DO NOTHING;

INSERT INTO feedback (candidate_id, job_id, integrity, honesty, discipline, hard_work, gratitude) VALUES
(1, 1, 5, 5, 4, 5, 4),
(2, 2, 4, 5, 5, 4, 5),
(3, 3, 5, 4, 5, 5, 4)
ON CONFLICT DO NOTHING;