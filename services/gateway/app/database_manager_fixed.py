# Fixed Database Manager with Proper Error Handling and Implementation Standards
import os
import logging
from sqlalchemy import create_engine, text, pool
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import time

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _get_database_url(self):
        """Get database URL with proper environment handling"""
        environment = os.getenv("ENVIRONMENT", "development").lower()
        
        if environment == "production":
            # Render production database
            default_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
        else:
            # Docker local database
            default_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
        
        database_url = os.getenv("DATABASE_URL", default_url)
        logger.info(f"Using database URL: {database_url.split('@')[0]}@***")
        return database_url
    
    def _initialize_engine(self):
        """Initialize database engine with proper configuration"""
        try:
            database_url = self._get_database_url()
            
            self.engine = create_engine(
                database_url,
                poolclass=pool.QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "bhiv_hr_gateway"
                }
            )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Test connection
            self._test_connection()
            logger.info("✅ Database engine initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Database engine initialization failed: {e}")
            raise
    
    def _test_connection(self):
        """Test database connection"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                    logger.info(f"✅ Database connection test successful (attempt {attempt + 1})")
                    return True
            except Exception as e:
                logger.warning(f"⚠️ Database connection test failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
    
    @contextmanager
    def get_db_session(self):
        """Get database session with proper error handling"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    @contextmanager
    def get_db_connection(self):
        """Get database connection with proper error handling"""
        connection = self.engine.connect()
        transaction = connection.begin()
        try:
            yield connection
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            connection.close()
    
    def execute_query(self, query, params=None):
        """Execute query with proper error handling"""
        try:
            with self.get_db_connection() as connection:
                result = connection.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_insert(self, query, params=None):
        """Execute insert query and return ID"""
        try:
            with self.get_db_connection() as connection:
                result = connection.execute(text(query), params or {})
                return result.fetchone()[0] if result.rowcount > 0 else None
        except Exception as e:
            logger.error(f"Insert execution failed: {e}")
            raise
    
    def check_health(self):
        """Comprehensive health check"""
        try:
            with self.get_db_connection() as connection:
                # Test basic connectivity
                connection.execute(text("SELECT 1"))
                
                # Check required tables
                tables_query = text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                """)
                tables = connection.execute(tables_query).fetchall()
                table_names = [row[0] for row in tables]
                
                required_tables = ['candidates', 'jobs', 'interviews', 'feedback', 'client_auth']
                missing_tables = [table for table in required_tables if table not in table_names]
                
                # Get table counts
                table_counts = {}
                for table in required_tables:
                    if table in table_names:
                        count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        table_counts[table] = count_result.fetchone()[0]
                    else:
                        table_counts[table] = "missing"
                
                return {
                    "status": "healthy" if not missing_tables else "degraded",
                    "tables_found": len(table_names),
                    "required_tables": len(required_tables),
                    "missing_tables": missing_tables,
                    "table_counts": table_counts,
                    "connection_pool": {
                        "size": self.engine.pool.size(),
                        "checked_out": self.engine.pool.checkedout(),
                        "overflow": self.engine.pool.overflow(),
                        "checked_in": self.engine.pool.checkedin()
                    }
                }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection_pool": "unavailable"
            }
    
    def create_missing_tables(self):
        """Create missing tables"""
        try:
            with self.get_db_connection() as connection:
                # Create tables SQL
                create_tables_sql = """
                -- Create candidates table
                CREATE TABLE IF NOT EXISTS candidates (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    phone VARCHAR(50),
                    location VARCHAR(255),
                    experience_years INTEGER DEFAULT 0,
                    technical_skills TEXT,
                    seniority_level VARCHAR(100),
                    education_level VARCHAR(255),
                    resume_path VARCHAR(500),
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Create jobs table
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    department VARCHAR(255),
                    location VARCHAR(255),
                    experience_level VARCHAR(100),
                    requirements TEXT,
                    description TEXT,
                    status VARCHAR(50) DEFAULT 'active',
                    client_id VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Create interviews table
                CREATE TABLE IF NOT EXISTS interviews (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
                    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
                    interview_date TIMESTAMP,
                    status VARCHAR(50) DEFAULT 'scheduled',
                    notes TEXT,
                    interviewer VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Create feedback table
                CREATE TABLE IF NOT EXISTS feedback (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
                    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
                    integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
                    honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
                    discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
                    hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
                    gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Create client_auth table
                CREATE TABLE IF NOT EXISTS client_auth (
                    id SERIAL PRIMARY KEY,
                    client_id VARCHAR(100) UNIQUE NOT NULL,
                    company_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP
                );

                -- Create indexes
                CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email);
                CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);
                CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
                CREATE INDEX IF NOT EXISTS idx_interviews_candidate_id ON interviews(candidate_id);
                CREATE INDEX IF NOT EXISTS idx_interviews_job_id ON interviews(job_id);
                CREATE INDEX IF NOT EXISTS idx_feedback_candidate_id ON feedback(candidate_id);
                CREATE INDEX IF NOT EXISTS idx_feedback_job_id ON feedback(job_id);
                """
                
                connection.execute(text(create_tables_sql))
                logger.info("✅ Database tables created successfully")
                return True
                
        except Exception as e:
            logger.error(f"❌ Table creation failed: {e}")
            return False

# Global database manager instance
database_manager = DatabaseManager()