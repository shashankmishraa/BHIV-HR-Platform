-- Add API Keys table for database-based key management
-- Alternative to Redis for API key storage

CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    key_id VARCHAR(16) UNIQUE NOT NULL,
    key_hash VARCHAR(64) NOT NULL,
    client_id VARCHAR(100) NOT NULL,
    permissions TEXT DEFAULT '["read"]',
    is_active BOOLEAN DEFAULT true,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_used TIMESTAMP,
    deactivated_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_client ON api_keys(client_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_active ON api_keys(is_active, expires_at);
CREATE INDEX IF NOT EXISTS idx_api_keys_expires ON api_keys(expires_at);

-- Sample API key for testing (hashed version of a test key)
INSERT INTO api_keys (key_id, key_hash, client_id, permissions, expires_at) VALUES
('TEST001', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'TECH001', '["admin"]', NOW() + INTERVAL '30 days')
ON CONFLICT (key_id) DO NOTHING;