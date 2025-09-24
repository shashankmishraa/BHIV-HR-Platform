# Fixed Database Connection with Proper Pooling
import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import logging

logger = logging.getLogger(__name__)

def get_fixed_db_engine():
    """Fixed database engine with proper connection pooling"""
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
    else:
        db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
    
    return create_engine(
        db_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={"connect_timeout": 10}
    )

def test_connection():
    """Test database connection and verify tables"""
    try:
        engine = get_fixed_db_engine()
        with engine.connect() as conn:
            # Test basic connection
            conn.execute(text("SELECT 1"))
            
            # Check required tables exist
            tables_query = text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """)
            result = conn.execute(tables_query)
            tables = [row[0] for row in result]
            
            required_tables = ['candidates', 'jobs', 'interviews', 'feedback', 'client_auth']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                logger.error(f"Missing tables: {missing_tables}")
                return False
            
            # Test table counts
            for table in required_tables:
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = count_result.fetchone()[0]
                logger.info(f"Table {table}: {count} records")
            
            logger.info("✅ Database connection and schema verification successful")
            return True
            
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def get_db_health():
    """Get database health status"""
    try:
        engine = get_fixed_db_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
            # Get table counts
            tables_query = text("""
                SELECT 
                    (SELECT COUNT(*) FROM candidates) as candidates,
                    (SELECT COUNT(*) FROM jobs) as jobs,
                    (SELECT COUNT(*) FROM interviews) as interviews,
                    (SELECT COUNT(*) FROM feedback) as feedback,
                    (SELECT COUNT(*) FROM client_auth) as client_auth
            """)
            result = conn.execute(tables_query).fetchone()
            
            return {
                "status": "healthy",
                "tables": {
                    "candidates": result[0],
                    "jobs": result[1], 
                    "interviews": result[2],
                    "feedback": result[3],
                    "client_auth": result[4]
                },
                "connection_pool": {
                    "size": engine.pool.size(),
                    "checked_out": engine.pool.checkedout()
                }
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Global engine instance
_engine = None

def get_engine():
    """Get global database engine"""
    global _engine
    if _engine is None:
        _engine = get_fixed_db_engine()
    return _engine