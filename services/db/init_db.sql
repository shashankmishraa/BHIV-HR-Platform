-- BHIV HR Platform - Database Initialization
-- Create database and user if they don't exist

-- This script runs as the postgres superuser during container initialization

-- Create the database
CREATE DATABASE bhiv_hr_nqzb;

-- Create the user with password
CREATE USER bhiv_user WITH PASSWORD 'B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE bhiv_hr_nqzb TO bhiv_user;

-- Connect to the new database and set up schema
\c bhiv_hr_nqzb;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO bhiv_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bhiv_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bhiv_user;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Candidates table
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table
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

-- Client authentication table
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
);

-- Client sessions table
CREATE TABLE IF NOT EXISTS client_sessions (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_revoked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (client_id) REFERENCES client_auth(client_id) ON DELETE CASCADE
);

-- Grant permissions on all tables to bhiv_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bhiv_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bhiv_user;

-- Insert sample data
INSERT INTO jobs (title, department, location, experience_level, requirements, description, status) VALUES
('Senior Python Developer', 'Engineering', 'Remote', 'Senior', 'Python, Django, PostgreSQL, 5+ years experience', 'We are looking for a senior Python developer to join our team...', 'active'),
('Data Scientist', 'Analytics', 'New York', 'Mid-Level', 'Python, Machine Learning, SQL, 3+ years experience', 'Join our data science team to build predictive models...', 'active'),
('Frontend Developer', 'Engineering', 'San Francisco', 'Junior', 'React, JavaScript, HTML/CSS, 2+ years experience', 'Build amazing user interfaces with React...', 'active')
ON CONFLICT DO NOTHING;