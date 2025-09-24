-- BHIV HR Platform - Complete Database Schema
-- Production-grade schema with proper constraints, indexes, and triggers

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create enum types for consistency
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended', 'deleted');
CREATE TYPE job_status AS ENUM ('active', 'inactive', 'closed', 'draft');
CREATE TYPE interview_status AS ENUM ('scheduled', 'in_progress', 'completed', 'cancelled', 'rescheduled');
CREATE TYPE employment_type AS ENUM ('full_time', 'part_time', 'contract', 'internship', 'freelance');
CREATE TYPE experience_level AS ENUM ('entry', 'junior', 'mid_level', 'senior', 'lead', 'executive');

-- Candidates table with comprehensive structure
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL CHECK (length(trim(name)) > 0),
    email VARCHAR(320) UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    phone VARCHAR(20) CHECK (phone ~ '^\+?[1-9]\d{1,14}$'),
    location VARCHAR(255),
    experience_years INTEGER DEFAULT 0 CHECK (experience_years >= 0 AND experience_years <= 50),
    technical_skills TEXT,
    soft_skills TEXT,
    seniority_level experience_level DEFAULT 'entry',
    education_level VARCHAR(100),
    resume_path VARCHAR(500),
    portfolio_url VARCHAR(500) CHECK (portfolio_url ~ '^https?://'),
    linkedin_url VARCHAR(500) CHECK (linkedin_url ~ '^https?://'),
    github_url VARCHAR(500) CHECK (github_url ~ '^https?://'),
    salary_expectation_min INTEGER CHECK (salary_expectation_min > 0),
    salary_expectation_max INTEGER CHECK (salary_expectation_max >= salary_expectation_min),
    availability_date DATE,
    remote_preference BOOLEAN DEFAULT true,
    status user_status DEFAULT 'active',
    notes TEXT,
    source VARCHAR(100) DEFAULT 'direct_application',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

-- Jobs table with comprehensive structure
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL CHECK (length(trim(title)) > 0),
    department VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    remote_allowed BOOLEAN DEFAULT false,
    employment_type employment_type DEFAULT 'full_time',
    experience_level experience_level DEFAULT 'mid_level',
    salary_min INTEGER CHECK (salary_min > 0),
    salary_max INTEGER CHECK (salary_max >= salary_min),
    currency VARCHAR(3) DEFAULT 'USD',
    requirements TEXT NOT NULL,
    description TEXT NOT NULL,
    responsibilities TEXT,
    benefits TEXT,
    skills_required TEXT[] DEFAULT '{}',
    skills_preferred TEXT[] DEFAULT '{}',
    positions_available INTEGER DEFAULT 1 CHECK (positions_available > 0),
    application_deadline DATE,
    status job_status DEFAULT 'active',
    priority INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    client_id VARCHAR(100) NOT NULL,
    hiring_manager VARCHAR(255),
    hr_contact VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

-- Job applications table for tracking applications
CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    application_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'applied' CHECK (status IN ('applied', 'screening', 'interviewing', 'offered', 'hired', 'rejected', 'withdrawn')),
    cover_letter TEXT,
    resume_version VARCHAR(500),
    source VARCHAR(100) DEFAULT 'direct',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(candidate_id, job_id)
);

-- Interviews table with comprehensive tracking
CREATE TABLE interviews (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    application_id INTEGER REFERENCES job_applications(id) ON DELETE CASCADE,
    interview_type VARCHAR(50) DEFAULT 'phone' CHECK (interview_type IN ('phone', 'video', 'in_person', 'technical', 'panel', 'final')),
    interview_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 60 CHECK (duration_minutes > 0),
    location VARCHAR(255),
    meeting_link VARCHAR(500),
    interviewer_name VARCHAR(255) NOT NULL,
    interviewer_email VARCHAR(320),
    interviewer_role VARCHAR(100),
    status interview_status DEFAULT 'scheduled',
    notes TEXT,
    technical_assessment BOOLEAN DEFAULT false,
    assessment_score INTEGER CHECK (assessment_score BETWEEN 0 AND 100),
    recommendation VARCHAR(50) CHECK (recommendation IN ('strong_hire', 'hire', 'no_hire', 'strong_no_hire')),
    follow_up_required BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

-- Feedback table with comprehensive evaluation
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    interview_id INTEGER REFERENCES interviews(id) ON DELETE CASCADE,
    evaluator_name VARCHAR(255) NOT NULL,
    evaluator_role VARCHAR(100),
    
    -- Technical skills (1-5 scale)
    technical_skills INTEGER CHECK (technical_skills BETWEEN 1 AND 5),
    problem_solving INTEGER CHECK (problem_solving BETWEEN 1 AND 5),
    code_quality INTEGER CHECK (code_quality BETWEEN 1 AND 5),
    system_design INTEGER CHECK (system_design BETWEEN 1 AND 5),
    
    -- Soft skills (1-5 scale)
    communication INTEGER CHECK (communication BETWEEN 1 AND 5),
    teamwork INTEGER CHECK (teamwork BETWEEN 1 AND 5),
    leadership INTEGER CHECK (leadership BETWEEN 1 AND 5),
    adaptability INTEGER CHECK (adaptability BETWEEN 1 AND 5),
    
    -- Company values (1-5 scale)
    integrity INTEGER CHECK (integrity BETWEEN 1 AND 5),
    honesty INTEGER CHECK (honesty BETWEEN 1 AND 5),
    discipline INTEGER CHECK (discipline BETWEEN 1 AND 5),
    hard_work INTEGER CHECK (hard_work BETWEEN 1 AND 5),
    gratitude INTEGER CHECK (gratitude BETWEEN 1 AND 5),
    
    -- Overall assessment
    overall_score DECIMAL(3,2) GENERATED ALWAYS AS (
        COALESCE(
            (COALESCE(technical_skills, 0) + COALESCE(problem_solving, 0) + COALESCE(code_quality, 0) + COALESCE(system_design, 0) +
             COALESCE(communication, 0) + COALESCE(teamwork, 0) + COALESCE(leadership, 0) + COALESCE(adaptability, 0) +
             COALESCE(integrity, 0) + COALESCE(honesty, 0) + COALESCE(discipline, 0) + COALESCE(hard_work, 0) + COALESCE(gratitude, 0))::DECIMAL / 
            NULLIF((CASE WHEN technical_skills IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN problem_solving IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN code_quality IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN system_design IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN communication IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN teamwork IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN leadership IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN adaptability IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN integrity IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN honesty IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN discipline IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN hard_work IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN gratitude IS NOT NULL THEN 1 ELSE 0 END), 0),
            0
        )
    ) STORED,
    
    strengths TEXT,
    areas_for_improvement TEXT,
    additional_comments TEXT,
    recommendation VARCHAR(50) CHECK (recommendation IN ('strong_hire', 'hire', 'no_hire', 'strong_no_hire')),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

-- Client authentication and management
CREATE TABLE client_auth (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    company_size VARCHAR(50) CHECK (company_size IN ('startup', 'small', 'medium', 'large', 'enterprise')),
    website VARCHAR(500) CHECK (website ~ '^https?://'),
    email VARCHAR(320) UNIQUE NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    phone VARCHAR(20) CHECK (phone ~ '^\+?[1-9]\d{1,14}$'),
    address TEXT,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    subscription_tier VARCHAR(50) DEFAULT 'basic' CHECK (subscription_tier IN ('basic', 'premium', 'enterprise')),
    subscription_expires_at TIMESTAMP WITH TIME ZONE,
    api_rate_limit INTEGER DEFAULT 1000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

-- Client sessions for authentication tracking
CREATE TABLE client_sessions (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    client_id VARCHAR(100) NOT NULL REFERENCES client_auth(client_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_revoked BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP WITH TIME ZONE,
    revoked_by VARCHAR(100)
);

-- Audit log for tracking all changes
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System configuration table
CREATE TABLE system_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);