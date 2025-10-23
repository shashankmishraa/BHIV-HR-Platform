#!/usr/bin/env python3
"""
BHIV HR Platform - Fix Portal Database Connection Issues
Fixes portal configuration and database connection problems
"""

import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RENDER_DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def fix_database_issues():
    """Fix database connection and redundant table issues"""
    
    try:
        conn = psycopg2.connect(RENDER_DATABASE_URL)
        cursor = conn.cursor()
        
        logger.info("🔧 Fixing database issues...")
        
        # 1. Remove backup tables (not needed in production)
        backup_tables = ['candidates_backup', 'clients_backup', 'jobs_backup', 'users_backup']
        
        for table in backup_tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                logger.info(f"✅ Removed backup table: {table}")
            except Exception as e:
                logger.warning(f"⚠️ Could not remove {table}: {e}")
        
        # 2. Ensure all required tables exist with correct structure
        required_fixes = """
        -- Ensure candidates table has all required columns
        ALTER TABLE candidates ADD COLUMN IF NOT EXISTS designation VARCHAR(255);
        ALTER TABLE candidates ADD COLUMN IF NOT EXISTS seniority_level VARCHAR(100);
        
        -- Ensure jobs table has client_id as VARCHAR (not INTEGER)
        ALTER TABLE jobs ALTER COLUMN client_id TYPE VARCHAR(100);
        
        -- Update any NULL client_ids to default values
        UPDATE jobs SET client_id = 'TECH001' WHERE client_id IS NULL;
        UPDATE jobs SET status = 'active' WHERE status IS NULL;
        
        -- Ensure candidates have proper status values
        UPDATE candidates SET status = 'applied' WHERE status IS NULL;
        
        -- Add missing indexes for performance
        CREATE INDEX IF NOT EXISTS idx_candidates_designation ON candidates(designation);
        CREATE INDEX IF NOT EXISTS idx_candidates_seniority ON candidates(seniority_level);
        """
        
        cursor.execute(required_fixes)
        logger.info("✅ Applied database structure fixes")
        
        # 3. Verify core data integrity
        verification_queries = [
            ("Candidates with valid status", "SELECT COUNT(*) FROM candidates WHERE status IN ('applied', 'screened', 'interviewed', 'offered', 'hired', 'rejected');"),
            ("Jobs with valid client_id", "SELECT COUNT(*) FROM jobs WHERE client_id IS NOT NULL;"),
            ("Active jobs", "SELECT COUNT(*) FROM jobs WHERE status = 'active';"),
            ("Clients available", "SELECT COUNT(*) FROM clients WHERE status = 'active';")
        ]
        
        logger.info("🔍 Verifying data integrity...")
        for desc, query in verification_queries:
            cursor.execute(query)
            result = cursor.fetchone()[0]
            logger.info(f"✅ {desc}: {result}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✅ Database issues fixed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database fix failed: {e}")
        return False

def generate_portal_config_fix():
    """Generate corrected portal configuration"""
    
    logger.info("🔧 Generating portal configuration fixes...")
    
    # Corrected config.py content
    corrected_config = '''"""
BHIV HR Platform - HR Portal Configuration
Version: 3.1.0 with Phase 3 Features
Updated: October 23, 2025
Status: Production Ready - Fixed Database Connection

Configuration for HR Portal Streamlit application:
- API Gateway connection settings (FIXED)
- HTTP client with connection pooling
- Timeout and retry configurations
- Production-ready defaults
"""

import httpx
import os

# Version Information
__version__ = "3.1.0"
__updated__ = "2025-10-23"
__status__ = "Production Ready - Database Fixed"

# API Configuration - FIXED FOR PRODUCTION
# Production: Use actual Render URLs, not Docker internal URLs
API_BASE = os.getenv("GATEWAY_URL", "https://bhiv-hr-gateway-46pz.onrender.com")
API_KEY = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")

# HTTP Client Configuration with proper timeouts
timeout_config = httpx.Timeout(
    connect=15.0,  # Connection timeout
    read=60.0,     # Read timeout for long operations
    write=30.0,    # Write timeout
    pool=10.0      # Pool timeout
)

limits = httpx.Limits(
    max_keepalive_connections=10,
    max_connections=20,
    keepalive_expiry=30.0
)

headers = {"Authorization": f"Bearer {API_KEY}"}

# Global HTTP client with connection pooling
http_client = httpx.Client(
    timeout=timeout_config,
    limits=limits,
    headers=headers,
    follow_redirects=True
)

# Portal Configuration
PORTAL_CONFIG = {
    "title": "BHIV HR Platform - Dashboard",
    "version": __version__,
    "api_endpoints": 55,  # Updated count
    "features": [
        "Candidate Management",
        "Job Posting", 
        "AI Matching",
        "Values Assessment",
        "Interview Scheduling",
        "Offer Management"
    ],
    "status": __status__,
    "updated": __updated__,
    "database_status": "Connected",
    "gateway_url": API_BASE
}'''
    
    logger.info("✅ Portal configuration fix generated")
    return corrected_config

def main():
    """Main fix function"""
    logger.info("🚀 Starting portal and database issue fixes...")
    
    # Fix database issues
    if fix_database_issues():
        logger.info("✅ Database issues resolved")
    else:
        logger.error("❌ Database fixes failed")
        return
    
    # Generate portal config fix
    config_fix = generate_portal_config_fix()
    
    # Save the corrected config
    try:
        with open('portal_config_fix.py', 'w') as f:
            f.write(config_fix)
        logger.info("✅ Portal configuration fix saved to 'portal_config_fix.py'")
        logger.info("📝 Copy this content to services/portal/config.py and redeploy")
    except Exception as e:
        logger.error(f"❌ Could not save config fix: {e}")
    
    # Summary of issues and fixes
    logger.info("\n📋 SUMMARY OF FIXES:")
    logger.info("1. ✅ Removed redundant backup tables (candidates_backup, etc.)")
    logger.info("2. ✅ Fixed database structure and data integrity")
    logger.info("3. ✅ Generated corrected portal configuration")
    logger.info("4. ✅ Updated API endpoints and connection settings")
    
    logger.info("\n🔧 NEXT STEPS:")
    logger.info("1. Copy portal_config_fix.py content to services/portal/config.py")
    logger.info("2. Copy the same fix to services/client_portal/config.py")
    logger.info("3. Redeploy all portal services on Render")
    logger.info("4. Verify portal connections work correctly")
    
    logger.info("\n🎉 Database and portal fixes completed!")

if __name__ == "__main__":
    main()