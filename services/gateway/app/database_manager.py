# BHIV HR Platform - Enterprise Database Manager
# Production-grade database management with proper connection pooling, error handling, and monitoring

import os
import logging
import time
from typing import Dict, List, Any, Optional, Union
from contextlib import contextmanager, asynccontextmanager
from datetime import datetime, timezone

from sqlalchemy import create_engine, text, pool, event
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DisconnectionError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration with environment-specific settings"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development").lower()
        self.database_url = self._get_database_url()
        self.pool_config = self._get_pool_config()
        self.connection_config = self._get_connection_config()
    
    def _get_database_url(self) -> str:
        """Get environment-specific database URL"""
        if self.environment == "production":
            return os.getenv(
                "DATABASE_URL",
                "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
            )
        else:
            return os.getenv(
                "DATABASE_URL",
                "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
            )
    
    def _get_pool_config(self) -> Dict[str, Any]:
        """Get connection pool configuration"""
        if self.environment == "production":
            return {
                "poolclass": pool.QueuePool,
                "pool_size": 20,
                "max_overflow": 30,
                "pool_pre_ping": True,
                "pool_recycle": 3600,
                "pool_timeout": 30
            }
        else:
            return {
                "poolclass": pool.QueuePool,
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": True,
                "pool_recycle": 1800,
                "pool_timeout": 20
            }
    
    def _get_connection_config(self) -> Dict[str, Any]:
        """Get connection-specific configuration"""
        return {
            "connect_timeout": 15,
            "application_name": f"bhiv_hr_gateway_{self.environment}",
            "options": "-c timezone=UTC"
        }

class DatabaseHealthMonitor:
    """Monitor database health and performance"""
    
    def __init__(self, engine: Engine):
        self.engine = engine
        self.metrics = {
            "total_connections": 0,
            "failed_connections": 0,
            "query_count": 0,
            "error_count": 0,
            "last_health_check": None,
            "avg_response_time": 0.0
        }
    
    def record_connection(self, success: bool = True):
        """Record connection attempt"""
        self.metrics["total_connections"] += 1
        if not success:
            self.metrics["failed_connections"] += 1
    
    def record_query(self, execution_time: float, success: bool = True):
        """Record query execution"""
        self.metrics["query_count"] += 1
        if not success:
            self.metrics["error_count"] += 1
        
        # Update average response time
        current_avg = self.metrics["avg_response_time"]
        query_count = self.metrics["query_count"]
        self.metrics["avg_response_time"] = (current_avg * (query_count - 1) + execution_time) / query_count
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get connection pool status"""
        try:
            pool = self.engine.pool
            return {
                "size": pool.size(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "checked_in": pool.checkedin(),
                "total_connections": self.metrics["total_connections"],
                "failed_connections": self.metrics["failed_connections"],
                "success_rate": (
                    (self.metrics["total_connections"] - self.metrics["failed_connections"]) / 
                    max(self.metrics["total_connections"], 1) * 100
                )
            }
        except Exception as e:
            logger.error(f"Failed to get pool status: {e}")
            return {"error": str(e)}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            "query_count": self.metrics["query_count"],
            "error_count": self.metrics["error_count"],
            "error_rate": (
                self.metrics["error_count"] / max(self.metrics["query_count"], 1) * 100
            ),
            "avg_response_time_ms": round(self.metrics["avg_response_time"] * 1000, 2),
            "last_health_check": self.metrics["last_health_check"]
        }

class DatabaseManager:
    """Enterprise-grade database manager with comprehensive error handling and monitoring"""
    
    def __init__(self):
        self.config = DatabaseConfig()
        self.engine: Optional[Engine] = None
        self.SessionLocal: Optional[sessionmaker] = None
        self.health_monitor: Optional[DatabaseHealthMonitor] = None
        self._executor = ThreadPoolExecutor(max_workers=10)
        self._initialized = False
        
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize database engine with comprehensive configuration"""
        try:
            logger.info(f"Initializing database engine for {self.config.environment} environment")
            
            # Create engine with full configuration
            self.engine = create_engine(
                self.config.database_url,
                **self.config.pool_config,
                connect_args=self.config.connection_config,
                echo=False,
                future=True
            )
            
            # Setup event listeners for monitoring
            self._setup_event_listeners()
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
            
            # Initialize health monitor
            self.health_monitor = DatabaseHealthMonitor(self.engine)
            
            # Test initial connection
            self._test_connection()
            
            self._initialized = True
            logger.info("✅ Database engine initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Database engine initialization failed: {e}")
            raise DatabaseConnectionError(f"Failed to initialize database: {e}")
    
    def _setup_event_listeners(self):
        """Setup SQLAlchemy event listeners for monitoring"""
        
        @event.listens_for(self.engine, "connect")
        def receive_connect(dbapi_connection, connection_record):
            logger.debug("Database connection established")
            if self.health_monitor:
                self.health_monitor.record_connection(True)
        
        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            logger.debug("Connection checked out from pool")
        
        @event.listens_for(self.engine, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            logger.debug("Connection checked in to pool")
    
    def _test_connection(self, max_retries: int = 3):
        """Test database connection with retry logic"""
        for attempt in range(max_retries):
            try:
                with self.engine.connect() as connection:
                    result = connection.execute(text("SELECT 1 as health_check"))
                    result.fetchone()
                    logger.info(f"✅ Database connection test successful (attempt {attempt + 1})")
                    return True
            except Exception as e:
                logger.warning(f"⚠️ Database connection test failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise DatabaseConnectionError(f"Connection test failed after {max_retries} attempts: {e}")
    
    @contextmanager
    def get_db_session(self):
        """Get database session with comprehensive error handling"""
        if not self._initialized:
            raise DatabaseConnectionError("Database manager not initialized")
        
        session = self.SessionLocal()
        start_time = time.time()
        
        try:
            yield session
            session.commit()
            
            execution_time = time.time() - start_time
            if self.health_monitor:
                self.health_monitor.record_query(execution_time, True)
                
        except Exception as e:
            session.rollback()
            execution_time = time.time() - start_time
            if self.health_monitor:
                self.health_monitor.record_query(execution_time, False)
            
            logger.error(f"Database session error: {e}")
            raise DatabaseOperationError(f"Database operation failed: {e}")
        finally:
            session.close()
    
    @contextmanager
    def get_db_connection(self):
        """Get database connection with comprehensive error handling"""
        if not self._initialized:
            raise DatabaseConnectionError("Database manager not initialized")
        
        connection = None
        transaction = None
        start_time = time.time()
        
        try:
            connection = self.engine.connect()
            transaction = connection.begin()
            
            yield connection
            
            transaction.commit()
            execution_time = time.time() - start_time
            if self.health_monitor:
                self.health_monitor.record_query(execution_time, True)
                
        except Exception as e:
            if transaction:
                transaction.rollback()
            
            execution_time = time.time() - start_time
            if self.health_monitor:
                self.health_monitor.record_query(execution_time, False)
            
            logger.error(f"Database connection error: {e}")
            raise DatabaseOperationError(f"Database operation failed: {e}")
        finally:
            if connection:
                connection.close()
    
    async def execute_query_async(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Any]:
        """Execute query asynchronously"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self.execute_query, query, params)
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Any]:
        """Execute query with proper error handling"""
        try:
            with self.get_db_connection() as connection:
                result = connection.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {query[:100]}... - Error: {e}")
            raise DatabaseOperationError(f"Query execution failed: {e}")
    
    def execute_insert(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[int]:
        """Execute insert query and return ID"""
        try:
            with self.get_db_connection() as connection:
                result = connection.execute(text(query), params or {})
                if result.rowcount > 0:
                    return result.fetchone()[0] if result.returns_rows else result.rowcount
                return None
        except Exception as e:
            logger.error(f"Insert execution failed: {query[:100]}... - Error: {e}")
            raise DatabaseOperationError(f"Insert execution failed: {e}")
    
    def execute_update(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """Execute update query and return affected rows"""
        try:
            with self.get_db_connection() as connection:
                result = connection.execute(text(query), params or {})
                return result.rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {query[:100]}... - Error: {e}")
            raise DatabaseOperationError(f"Update execution failed: {e}")
    
    def check_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        try:
            start_time = time.time()
            
            with self.get_db_connection() as connection:
                # Test basic connectivity
                connection.execute(text("SELECT 1"))
                
                # Check required tables
                tables_query = text("""
                    SELECT table_name, 
                           (SELECT COUNT(*) FROM information_schema.columns 
                            WHERE table_name = t.table_name AND table_schema = 'public') as column_count
                    FROM information_schema.tables t
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                """)
                tables_result = connection.execute(tables_query).fetchall()
                
                tables_info = {row[0]: {"columns": row[1]} for row in tables_result}
                table_names = list(tables_info.keys())
                
                required_tables = [
                    'candidates', 'jobs', 'job_applications', 'interviews', 
                    'feedback', 'client_auth', 'client_sessions', 'audit_log', 'system_config'
                ]
                missing_tables = [table for table in required_tables if table not in table_names]
                
                # Get table counts for existing tables
                for table in required_tables:
                    if table in table_names:
                        try:
                            count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                            tables_info[table]["count"] = count_result.fetchone()[0]
                        except Exception as e:
                            tables_info[table]["count"] = f"error: {e}"
                            logger.warning(f"Failed to count rows in {table}: {e}")
                
                response_time = time.time() - start_time
                
                # Update health monitor
                if self.health_monitor:
                    self.health_monitor.metrics["last_health_check"] = datetime.now(timezone.utc).isoformat()
                
                health_status = {
                    "status": "healthy" if not missing_tables else "degraded",
                    "response_time_ms": round(response_time * 1000, 2),
                    "database_info": {
                        "environment": self.config.environment,
                        "tables_found": len(table_names),
                        "required_tables": len(required_tables),
                        "missing_tables": missing_tables,
                        "tables": tables_info
                    },
                    "connection_pool": self.health_monitor.get_pool_status() if self.health_monitor else {},
                    "performance": self.health_monitor.get_performance_metrics() if self.health_monitor else {},
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                return health_status
                
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "connection_pool": self.health_monitor.get_pool_status() if self.health_monitor else {}
            }
    
    def create_missing_tables(self) -> bool:
        """Create missing database tables and indexes"""
        try:
            logger.info("Creating missing database tables...")
            
            # Read and execute schema files
            schema_files = [
                "01_create_tables.sql",
                "02_create_indexes.sql", 
                "03_create_triggers.sql",
                "04_insert_sample_data.sql"
            ]
            
            for schema_file in schema_files:
                schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "db", schema_file)
                
                if os.path.exists(schema_path):
                    logger.info(f"Executing {schema_file}...")
                    
                    with open(schema_path, 'r') as f:
                        schema_sql = f.read()
                    
                    # Split by semicolon and execute each statement
                    statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
                    
                    with self.get_db_connection() as connection:
                        for statement in statements:
                            if statement:
                                try:
                                    connection.execute(text(statement))
                                except Exception as e:
                                    # Log but continue with other statements
                                    logger.warning(f"Statement failed (continuing): {e}")
                else:
                    logger.warning(f"Schema file not found: {schema_path}")
            
            logger.info("✅ Database schema creation completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database schema creation failed: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            with self.get_db_connection() as connection:
                stats_query = text("""
                    SELECT 
                        (SELECT COUNT(*) FROM candidates WHERE status = 'active') as active_candidates,
                        (SELECT COUNT(*) FROM jobs WHERE status = 'active') as active_jobs,
                        (SELECT COUNT(*) FROM interviews WHERE status IN ('scheduled', 'in_progress')) as upcoming_interviews,
                        (SELECT COUNT(*) FROM feedback WHERE created_at >= CURRENT_DATE - INTERVAL '30 days') as recent_feedback,
                        (SELECT COUNT(*) FROM client_auth WHERE is_active = true) as active_clients,
                        (SELECT COUNT(*) FROM audit_log WHERE created_at >= CURRENT_DATE - INTERVAL '7 days') as recent_audit_entries
                """)
                result = connection.execute(stats_query).fetchone()
                
                return {
                    "database_statistics": {
                        "active_candidates": result[0] or 0,
                        "active_jobs": result[1] or 0,
                        "upcoming_interviews": result[2] or 0,
                        "recent_feedback": result[3] or 0,
                        "active_clients": result[4] or 0,
                        "recent_audit_entries": result[5] or 0
                    },
                    "performance_metrics": self.health_monitor.get_performance_metrics() if self.health_monitor else {},
                    "generated_at": datetime.now(timezone.utc).isoformat()
                }
        except Exception as e:
            logger.error(f"Statistics retrieval failed: {e}")
            raise DatabaseOperationError(f"Statistics retrieval failed: {e}")
    
    def close(self):
        """Close database connections and cleanup"""
        try:
            if self.engine:
                self.engine.dispose()
            if self._executor:
                self._executor.shutdown(wait=True)
            logger.info("Database manager closed successfully")
        except Exception as e:
            logger.error(f"Error closing database manager: {e}")

# Custom exceptions
class DatabaseConnectionError(Exception):
    """Database connection related errors"""
    pass

class DatabaseOperationError(Exception):
    """Database operation related errors"""
    pass

# Global database manager instance
database_manager = DatabaseManager()