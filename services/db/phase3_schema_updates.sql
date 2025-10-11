-- Phase 3: Database Schema Updates for Learning Engine
-- Company preferences table for learning capabilities

-- Company preferences table for learning
CREATE TABLE IF NOT EXISTS company_scoring_preferences (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) REFERENCES clients(client_id),
    scoring_weights JSONB,
    avg_satisfaction DECIMAL(3,2),
    feedback_count INTEGER,
    preferred_experience DECIMAL(5,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced matching cache with learning data
ALTER TABLE matching_cache ADD COLUMN IF NOT EXISTS 
    learning_version VARCHAR(50) DEFAULT 'v3.0';

-- Index for performance
CREATE INDEX IF NOT EXISTS idx_company_scoring_client 
ON company_scoring_preferences(client_id);

-- Update schema version
INSERT INTO schema_version (version, description) VALUES 
('3.0.0', 'Phase 3 - Learning engine and enhanced batch processing')
ON CONFLICT (version) DO UPDATE SET applied_at = CURRENT_TIMESTAMP;

SELECT 'Phase 3 Schema Updates Applied Successfully' as status;