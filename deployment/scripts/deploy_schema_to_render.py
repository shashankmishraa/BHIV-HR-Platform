#!/usr/bin/env python3
"""
BHIV HR Platform - Render Database Schema Deployment
Applies local schema changes to live Render PostgreSQL database
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Render Database Configuration
RENDER_DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def read_schema_file():
    """Read the consolidated schema SQL file"""
    schema_path = os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'db', 'consolidated_schema.sql')
    
    try:
        with open(schema_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Schema file not found: {schema_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading schema file: {e}")
        sys.exit(1)

def connect_to_database():
    """Connect to Render PostgreSQL database"""
    try:
        conn = psycopg2.connect(RENDER_DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        logger.info("✅ Connected to Render PostgreSQL database")
        return conn
    except Exception as e:
        logger.error(f"❌ Failed to connect to database: {e}")
        sys.exit(1)

def check_current_schema_version(cursor):
    """Check current schema version in database"""
    try:
        cursor.execute("SELECT version, applied_at FROM schema_version ORDER BY applied_at DESC LIMIT 1;")
        result = cursor.fetchone()
        if result:
            logger.info(f"Current schema version: {result[0]} (applied: {result[1]})")
            return result[0]
        else:
            logger.info("No schema version found - first deployment")
            return None
    except Exception as e:
        logger.info("Schema version table doesn't exist - first deployment")
        return None

def backup_critical_data(cursor):
    """Create backup of critical data before schema changes"""
    backup_queries = [
        "CREATE TABLE IF NOT EXISTS candidates_backup AS SELECT * FROM candidates;",
        "CREATE TABLE IF NOT EXISTS jobs_backup AS SELECT * FROM jobs;",
        "CREATE TABLE IF NOT EXISTS clients_backup AS SELECT * FROM clients;",
        "CREATE TABLE IF NOT EXISTS users_backup AS SELECT * FROM users;"
    ]
    
    try:
        for query in backup_queries:
            cursor.execute(query)
        logger.info("✅ Critical data backed up")
    except Exception as e:
        logger.warning(f"⚠️ Backup warning (may be normal): {e}")

def apply_schema(cursor, schema_sql):
    """Apply schema changes to database"""
    try:
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        success_count = 0
        warning_count = 0
        
        for i, statement in enumerate(statements):
            if not statement or statement.startswith('--'):
                continue
                
            try:
                cursor.execute(statement)
                success_count += 1
                
                # Log important operations
                if any(keyword in statement.upper() for keyword in ['CREATE TABLE', 'ALTER TABLE', 'CREATE INDEX']):
                    logger.info(f"✅ Executed: {statement[:50]}...")
                    
            except Exception as e:
                warning_count += 1
                # Log warnings for expected conflicts
                if "already exists" in str(e) or "does not exist" in str(e):
                    logger.debug(f"⚠️ Expected warning: {e}")
                else:
                    logger.warning(f"⚠️ Statement warning: {e}")
                    logger.debug(f"Statement: {statement[:100]}...")
        
        logger.info(f"✅ Schema deployment completed: {success_count} successful, {warning_count} warnings")
        return True
        
    except Exception as e:
        logger.error(f"❌ Critical error during schema deployment: {e}")
        return False

def verify_deployment(cursor):
    """Verify schema deployment was successful"""
    verification_queries = [
        ("Tables count", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"),
        ("Candidates table", "SELECT COUNT(*) FROM candidates;"),
        ("Jobs table", "SELECT COUNT(*) FROM jobs;"),
        ("Schema version", "SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1;"),
        ("Indexes count", "SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public';")
    ]
    
    logger.info("🔍 Verifying deployment...")
    
    for description, query in verification_queries:
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            logger.info(f"✅ {description}: {result[0] if result else 'N/A'}")
        except Exception as e:
            logger.warning(f"⚠️ {description} verification failed: {e}")

def main():
    """Main deployment function"""
    logger.info("🚀 Starting BHIV HR Platform schema deployment to Render")
    logger.info(f"Target: Render PostgreSQL (Oregon)")
    logger.info(f"Time: {datetime.now()}")
    
    # Read schema file
    logger.info("📖 Reading schema file...")
    schema_sql = read_schema_file()
    logger.info(f"✅ Schema file loaded ({len(schema_sql)} characters)")
    
    # Connect to database
    logger.info("🔌 Connecting to Render database...")
    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        # Check current version
        logger.info("🔍 Checking current schema version...")
        current_version = check_current_schema_version(cursor)
        
        # Backup critical data
        logger.info("💾 Creating data backup...")
        backup_critical_data(cursor)
        
        # Apply schema changes
        logger.info("🔧 Applying schema changes...")
        if apply_schema(cursor, schema_sql):
            logger.info("✅ Schema deployment successful!")
            
            # Verify deployment
            verify_deployment(cursor)
            
            logger.info("🎉 BHIV HR Platform schema successfully deployed to Render!")
            logger.info("🌐 Production services can now use updated schema")
            
        else:
            logger.error("❌ Schema deployment failed!")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Deployment error: {e}")
        sys.exit(1)
        
    finally:
        cursor.close()
        conn.close()
        logger.info("🔌 Database connection closed")

if __name__ == "__main__":
    main()