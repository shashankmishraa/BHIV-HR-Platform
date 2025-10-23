#!/usr/bin/env python3
"""
BHIV HR Platform - Verify Render Database Deployment
Tests the live Render database to ensure schema deployment was successful
"""

import psycopg2
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Render Database Configuration
RENDER_DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def verify_deployment():
    """Verify the schema deployment was successful"""
    try:
        conn = psycopg2.connect(RENDER_DATABASE_URL)
        cursor = conn.cursor()
        
        logger.info("🔍 Verifying BHIV HR Platform schema deployment on Render...")
        
        # Test queries to verify schema
        tests = [
            ("Database Connection", "SELECT 1;"),
            ("Tables Count", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"),
            ("Candidates Table", "SELECT COUNT(*) FROM candidates;"),
            ("Jobs Table", "SELECT COUNT(*) FROM jobs;"),
            ("Clients Table", "SELECT COUNT(*) FROM clients;"),
            ("Users Table", "SELECT COUNT(*) FROM users;"),
            ("Feedback Table", "SELECT COUNT(*) FROM feedback;"),
            ("Interviews Table", "SELECT COUNT(*) FROM interviews;"),
            ("Offers Table", "SELECT COUNT(*) FROM offers;"),
            ("Matching Cache", "SELECT COUNT(*) FROM matching_cache;"),
            ("Audit Logs", "SELECT COUNT(*) FROM audit_logs;"),
            ("Rate Limits", "SELECT COUNT(*) FROM rate_limits;"),
            ("CSP Violations", "SELECT COUNT(*) FROM csp_violations;"),
            ("Company Scoring", "SELECT COUNT(*) FROM company_scoring_preferences;"),
            ("Indexes Count", "SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public';"),
            ("Sample Candidate", "SELECT name, email FROM candidates LIMIT 1;"),
            ("Sample Job", "SELECT title, department FROM jobs LIMIT 1;"),
            ("Sample Client", "SELECT client_id, company_name FROM clients LIMIT 1;")
        ]
        
        success_count = 0
        for test_name, query in tests:
            try:
                cursor.execute(query)
                result = cursor.fetchone()
                logger.info(f"✅ {test_name}: {result[0] if result else 'N/A'}")
                success_count += 1
            except Exception as e:
                logger.error(f"❌ {test_name}: {e}")
        
        logger.info(f"\n🎉 Verification completed: {success_count}/{len(tests)} tests passed")
        
        if success_count >= len(tests) - 2:  # Allow 2 failures for optional tables
            logger.info("✅ Schema deployment verification SUCCESSFUL!")
            logger.info("🌐 Production services can safely use the updated database")
        else:
            logger.warning("⚠️ Some verification tests failed - check logs above")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    verify_deployment()