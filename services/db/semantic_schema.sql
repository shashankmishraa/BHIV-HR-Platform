-- Enhanced database schema for semantic processing

-- Add semantic fields to candidates table
ALTER TABLE candidates ADD COLUMN IF NOT EXISTS semantic_skills JSONB;
ALTER TABLE candidates ADD COLUMN IF NOT EXISTS semantic_roles JSONB;
ALTER TABLE candidates ADD COLUMN IF NOT EXISTS resume_embedding VECTOR(384);
ALTER TABLE candidates ADD COLUMN IF NOT EXISTS job_similarity_scores JSONB;

-- Create semantic_matches table for job-candidate matching
CREATE TABLE IF NOT EXISTS semantic_matches (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    similarity_score FLOAT,
    skill_match_score FLOAT,
    role_match_score FLOAT,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create embeddings table for caching
CREATE TABLE IF NOT EXISTS embeddings_cache (
    id SERIAL PRIMARY KEY,
    content_hash VARCHAR(64) UNIQUE,
    content_type VARCHAR(50), -- 'resume', 'job_description'
    embedding VECTOR(384),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_candidates_semantic_skills ON candidates USING GIN (semantic_skills);
CREATE INDEX IF NOT EXISTS idx_candidates_semantic_roles ON candidates USING GIN (semantic_roles);
CREATE INDEX IF NOT EXISTS idx_semantic_matches_similarity ON semantic_matches (similarity_score DESC);
CREATE INDEX IF NOT EXISTS idx_embeddings_hash ON embeddings_cache (content_hash);