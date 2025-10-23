#!/usr/bin/env python3
"""
BHIV HR Platform - Database Analysis and Cleanup
Analyzes database for redundant tables and portal connection issues
"""

import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RENDER_DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

def analyze_database():
    """Analyze database tables and identify issues"""
    
    try:
        conn = psycopg2.connect(RENDER_DATABASE_URL)
        cursor = conn.cursor()
        
        logger.info("🔍 Analyzing BHIV HR Platform database...")
        
        # Get all tables
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        all_tables = cursor.fetchall()
        
        # Required core tables for the project
        required_tables = {
            'candidates', 'jobs', 'feedback', 'interviews', 'offers',
            'users', 'clients', 'matching_cache', 'audit_logs', 
            'rate_limits', 'csp_violations', 'company_scoring_preferences',
            'schema_version'
        }
        
        # Identify table categories
        core_tables = []
        backup_tables = []
        system_tables = []
        redundant_tables = []
        
        for table_name, table_type in all_tables:
            if table_name in required_tables:
                core_tables.append(table_name)
            elif table_name.endswith('_backup'):
                backup_tables.append(table_name)
            elif table_name.startswith('pg_'):
                system_tables.append(table_name)
            elif table_name in ['applications', 'client_auth', 'client_sessions', 'match_scores']:
                redundant_tables.append(table_name)
            else:
                logger.warning(f"⚠️ Unknown table: {table_name}")
        
        # Report findings
        logger.info(f"📊 Database Analysis Results:")
        logger.info(f"✅ Core tables ({len(core_tables)}): {', '.join(core_tables)}")
        logger.info(f"🗂️ Backup tables ({len(backup_tables)}): {', '.join(backup_tables)}")
        logger.info(f"⚙️ System tables ({len(system_tables)}): {', '.join(system_tables)}")
        logger.info(f"❌ Redundant tables ({len(redundant_tables)}): {', '.join(redundant_tables)}")
        
        # Check for missing required tables
        existing_core = set(core_tables)
        missing_tables = required_tables - existing_core
        if missing_tables:
            logger.error(f"❌ Missing required tables: {', '.join(missing_tables)}")
        else:
            logger.info("✅ All required tables present")
        
        # Check table data counts
        logger.info("\n📈 Table Data Counts:")
        for table in core_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                logger.info(f"  {table}: {count} records")
            except Exception as e:
                logger.error(f"  {table}: Error - {e}")
        
        # Check for portal connection issues
        logger.info("\n🔧 Portal Connection Diagnostics:")
        
        # Test critical queries portals use
        portal_queries = [
            ("Candidates for HR Portal", "SELECT COUNT(*) FROM candidates WHERE status = 'applied';"),
            ("Jobs for Client Portal", "SELECT COUNT(*) FROM jobs WHERE status = 'active';"),
            ("Client Authentication", "SELECT COUNT(*) FROM clients WHERE status = 'active';"),
            ("User Authentication", "SELECT COUNT(*) FROM users WHERE status = 'active';"),
            ("Feedback System", "SELECT COUNT(*) FROM feedback;")
        ]
        
        for desc, query in portal_queries:
            try:
                cursor.execute(query)
                result = cursor.fetchone()[0]
                logger.info(f"✅ {desc}: {result}")
            except Exception as e:
                logger.error(f"❌ {desc}: {e}")
        
        # Generate cleanup recommendations
        logger.info("\n🧹 Cleanup Recommendations:")
        if redundant_tables:
            logger.info(f"1. Drop redundant tables: {', '.join(redundant_tables)}")
        if backup_tables:
            logger.info(f"2. Consider removing backup tables: {', '.join(backup_tables)}")
        
        cursor.close()
        conn.close()
        
        return redundant_tables, backup_tables
        
    except Exception as e:
        logger.error(f"❌ Database analysis failed: {e}")
        return [], []

def cleanup_redundant_tables(redundant_tables):
    """Remove redundant tables"""
    if not redundant_tables:
        logger.info("✅ No redundant tables to clean up")
        return
    
    try:
        conn = psycopg2.connect(RENDER_DATABASE_URL)
        cursor = conn.cursor()
        
        logger.info(f"🧹 Cleaning up {len(redundant_tables)} redundant tables...")
        
        for table in redundant_tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                logger.info(f"✅ Dropped table: {table}")
            except Exception as e:
                logger.error(f"❌ Failed to drop {table}: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✅ Database cleanup completed")
        
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}")

def main():
    """Main analysis and cleanup"""
    logger.info("🚀 Starting database analysis and cleanup...")
    
    # Analyze database
    redundant_tables, backup_tables = analyze_database()
    
    # Ask for cleanup confirmation
    if redundant_tables:
        logger.info(f"\n⚠️ Found {len(redundant_tables)} redundant tables to remove")
        cleanup_redundant_tables(redundant_tables)
    
    logger.info("\n🎉 Database analysis completed!")

if __name__ == "__main__":
    main()