#!/usr/bin/env python3
"""
BHIV HR Platform - Fix Missing Tables on Render
Adds the missing tables that weren't created in the initial deployment
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Render Database Configuration
RENDER_DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def fix_missing_tables():
    """Add missing tables to the database"""
    
    missing_tables_sql = """
    -- CSP_VIOLATIONS TABLE (Content Security Policy violations)
    CREATE TABLE IF NOT EXISTS csp_violations (
        id SERIAL PRIMARY KEY,
        violated_directive VARCHAR(255) NOT NULL,
        blocked_uri TEXT NOT NULL,
        document_uri TEXT NOT NULL,
        ip_address INET,
        user_agent TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- COMPANY_SCORING_PREFERENCES TABLE (Phase 3 learning engine)
    CREATE TABLE IF NOT EXISTS company_scoring_preferences (
        id SERIAL PRIMARY KEY,
        client_id VARCHAR(100) REFERENCES clients(client_id),
        scoring_weights JSONB,
        avg_satisfaction DECIMAL(3,2),
        feedback_count INTEGER,
        preferred_experience DECIMAL(5,2),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- SCHEMA_VERSION TABLE (Version tracking)
    CREATE TABLE IF NOT EXISTS schema_version (
        version VARCHAR(20) PRIMARY KEY,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        description TEXT
    );

    -- Add missing indexes
    CREATE INDEX IF NOT EXISTS idx_csp_violations_timestamp ON csp_violations(timestamp);
    CREATE INDEX IF NOT EXISTS idx_csp_violations_ip ON csp_violations(ip_address);
    CREATE INDEX IF NOT EXISTS idx_company_scoring_client ON company_scoring_preferences(client_id);

    -- Insert schema version
    INSERT INTO schema_version (version, description) VALUES 
    ('4.1.0', 'Production consolidated schema with Phase 3 learning engine'),
    ('4.0.1', 'Fixed schema - removed invalid generated column update'),
    ('3.0.0', 'Phase 3 - Learning engine and enhanced batch processing')
    ON CONFLICT (version) DO UPDATE SET applied_at = CURRENT_TIMESTAMP;

    -- Update matching cache with learning version
    ALTER TABLE matching_cache ADD COLUMN IF NOT EXISTS learning_version VARCHAR(50) DEFAULT 'v3.0';
    """
    
    try:
        conn = psycopg2.connect(RENDER_DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        logger.info("🔧 Adding missing tables to Render database...")
        
        # Execute the SQL
        cursor.execute(missing_tables_sql)
        
        logger.info("✅ Missing tables added successfully!")
        
        # Verify the tables were created
        verification_queries = [
            ("CSP Violations", "SELECT COUNT(*) FROM csp_violations;"),
            ("Company Scoring", "SELECT COUNT(*) FROM company_scoring_preferences;"),
            ("Schema Version", "SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1;"),
            ("Matching Cache Learning", "SELECT COUNT(*) FROM matching_cache WHERE learning_version IS NOT NULL;")
        ]
        
        for test_name, query in verification_queries:
            try:
                cursor.execute(query)
                result = cursor.fetchone()
                logger.info(f"✅ {test_name}: {result[0] if result else 'N/A'}")
            except Exception as e:
                logger.warning(f"⚠️ {test_name}: {e}")
        
        cursor.close()
        conn.close()
        
        logger.info("🎉 All missing tables have been successfully added to Render database!")
        
    except Exception as e:
        logger.error(f"❌ Error adding missing tables: {e}")

if __name__ == "__main__":
    fix_missing_tables()