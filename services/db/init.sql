CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO clients (name, api_key) 
VALUES ('Default Client', 'myverysecureapikey123') 
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    location VARCHAR(255),
    cv_url TEXT,
    experience_years INTEGER,
    education_level VARCHAR(100),
    technical_skills TEXT,
    seniority_level VARCHAR(50),
    skill_categories JSONB,
    values_prediction JSONB,
    ai_score FLOAT,
    status VARCHAR(50) DEFAULT 'applied',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    reviewer VARCHAR(255),
    free_text TEXT,
    values_scores JSONB,
    overall_recommendation VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    interview_date TIMESTAMP,
    interviewer VARCHAR(255),
    interview_type VARCHAR(50) DEFAULT 'technical',
    status VARCHAR(50) DEFAULT 'scheduled',
    feedback TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    salary INTEGER,
    status VARCHAR(50) DEFAULT 'draft',
    offer_date TIMESTAMP DEFAULT NOW(),
    response_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bhiv_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO bhiv_user;
