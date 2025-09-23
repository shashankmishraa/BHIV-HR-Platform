#!/usr/bin/env python3
"""
Database Schema Management
Handles migrations, schema validation, and database operations
"""

import os
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Centralized database management"""
    
    def __init__(self):
        self.engine = self._create_engine()
        self.metadata = MetaData()
        self._define_schema()
    
    def _create_engine(self):
        """Create database engine with proper configuration"""
        # Environment-aware database URL with updated credentials
        default_db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
        
        if os.getenv("RENDER") or os.getenv("DATABASE_URL"):
            database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb")
        elif os.getenv("DOCKER_ENV"):
            database_url = default_db_url
        else:
            database_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
        
        return create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"connect_timeout": 10}
        )
    
    def _define_schema(self):
        """Define expected database schema"""
        self.candidates_table = Table(
            'candidates', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(255), nullable=False),
            Column('email', String(255), unique=True, nullable=False),
            Column('phone', String(20)),
            Column('location', String(255)),
            Column('technical_skills', String(2000)),
            Column('experience_years', Integer),
            Column('seniority_level', String(100)),
            Column('education_level', String(100)),
            Column('resume_path', String(500)),
            Column('status', String(50), default='active'),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        )
        
        self.jobs_table = Table(
            'jobs', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('title', String(255), nullable=False),
            Column('department', String(100), nullable=False),
            Column('location', String(255), nullable=False),
            Column('experience_level', String(50), nullable=False),
            Column('requirements', String(2000), nullable=False),
            Column('description', String(5000), nullable=False),
            Column('client_id', Integer, default=1),
            Column('employment_type', String(50), default='Full-time'),
            Column('status', String(50), default='active'),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        )
        
        self.interviews_table = Table(
            'interviews', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('candidate_id', Integer, nullable=False),
            Column('job_id', Integer, nullable=False),
            Column('interview_date', DateTime),
            Column('interviewer', String(255), default='HR Team'),
            Column('status', String(50), default='scheduled'),
            Column('notes', String(2000)),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        )
        
        self.feedback_table = Table(
            'feedback', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('candidate_id', Integer, nullable=False),
            Column('job_id', Integer, nullable=False),
            Column('integrity', Integer, nullable=False),
            Column('honesty', Integer, nullable=False),
            Column('discipline', Integer, nullable=False),
            Column('hard_work', Integer, nullable=False),
            Column('gratitude', Integer, nullable=False),
            Column('comments', String(2000)),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        )
    
    def check_table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
                return True
        except Exception:
            return False
    
    def check_column_exists(self, table_name: str, column_name: str) -> bool:
        """Check if column exists in table"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT {column_name} FROM {table_name} LIMIT 1"))
                return True
        except Exception:
            return False
    
    def add_missing_columns(self) -> Dict[str, Any]:
        """Add missing columns with proper migrations"""
        migration_results = {
            "migrations_applied": [],
            "errors": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Define required columns for each table
        required_columns = {
            "candidates": [
                ("status", "VARCHAR(50) DEFAULT 'active'"),
                ("created_at", "TIMESTAMP DEFAULT NOW()"),
                ("updated_at", "TIMESTAMP DEFAULT NOW()")
            ],
            "jobs": [
                ("client_id", "INTEGER DEFAULT 1"),
                ("employment_type", "VARCHAR(50) DEFAULT 'Full-time'"),
                ("status", "VARCHAR(50) DEFAULT 'active'"),
                ("created_at", "TIMESTAMP DEFAULT NOW()"),
                ("updated_at", "TIMESTAMP DEFAULT NOW()")
            ],
            "interviews": [
                ("interviewer", "VARCHAR(255) DEFAULT 'HR Team'"),
                ("status", "VARCHAR(50) DEFAULT 'scheduled'"),
                ("notes", "TEXT"),
                ("created_at", "TIMESTAMP DEFAULT NOW()"),
                ("updated_at", "TIMESTAMP DEFAULT NOW()")
            ],
            "feedback": [
                ("comments", "TEXT"),
                ("created_at", "TIMESTAMP DEFAULT NOW()"),
                ("updated_at", "TIMESTAMP DEFAULT NOW()")
            ]
        }
        
        try:
            with self.engine.begin() as conn:
                for table_name, columns in required_columns.items():
                    if not self.check_table_exists(table_name):
                        migration_results["errors"].append(f"Table {table_name} does not exist")
                        continue
                    
                    for column_name, column_def in columns:
                        if not self.check_column_exists(table_name, column_name):
                            try:
                                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_def}"))
                                migration_results["migrations_applied"].append(f"Added {column_name} to {table_name}")
                                logger.info(f"Added column {column_name} to table {table_name}")
                            except Exception as e:
                                error_msg = f"Failed to add {column_name} to {table_name}: {str(e)}"
                                migration_results["errors"].append(error_msg)
                                logger.error(error_msg)
                
                # Create indexes for better performance
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status)",
                    "CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email)",
                    "CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)",
                    "CREATE INDEX IF NOT EXISTS idx_interviews_candidate_job ON interviews(candidate_id, job_id)",
                    "CREATE INDEX IF NOT EXISTS idx_feedback_candidate_job ON feedback(candidate_id, job_id)"
                ]
                
                for index_sql in indexes:
                    try:
                        conn.execute(text(index_sql))
                        migration_results["migrations_applied"].append(f"Created index: {index_sql.split('idx_')[1].split(' ')[0]}")
                    except Exception as e:
                        migration_results["errors"].append(f"Index creation failed: {str(e)}")
        
        except Exception as e:
            migration_results["errors"].append(f"Migration transaction failed: {str(e)}")
            logger.error(f"Database migration failed: {str(e)}")
        
        return migration_results
    
    def validate_schema(self) -> Dict[str, Any]:
        """Validate database schema"""
        validation_results = {
            "valid": True,
            "tables_checked": [],
            "missing_tables": [],
            "missing_columns": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        expected_tables = ["candidates", "jobs", "interviews", "feedback"]
        
        for table_name in expected_tables:
            validation_results["tables_checked"].append(table_name)
            
            if not self.check_table_exists(table_name):
                validation_results["missing_tables"].append(table_name)
                validation_results["valid"] = False
                continue
            
            # Check required columns based on table
            if table_name == "candidates":
                required_cols = ["id", "name", "email", "status"]
            elif table_name == "jobs":
                required_cols = ["id", "title", "department", "location", "status"]
            elif table_name == "interviews":
                required_cols = ["id", "candidate_id", "job_id", "interviewer"]
            elif table_name == "feedback":
                required_cols = ["id", "candidate_id", "job_id", "integrity", "honesty"]
            
            for col in required_cols:
                if not self.check_column_exists(table_name, col):
                    validation_results["missing_columns"].append(f"{table_name}.{col}")
                    validation_results["valid"] = False
        
        return validation_results
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get database health status"""
        try:
            with self.engine.connect() as conn:
                # Test basic connectivity
                conn.execute(text("SELECT 1"))
                
                # Get table counts
                table_counts = {}
                for table in ["candidates", "jobs", "interviews", "feedback"]:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        table_counts[table] = result.fetchone()[0]
                    except Exception:
                        table_counts[table] = "N/A"
                
                return {
                    "status": "healthy",
                    "connection": "active",
                    "pool_size": self.engine.pool.size(),
                    "checked_out": self.engine.pool.checkedout(),
                    "table_counts": table_counts,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        except Exception as e:
            return {
                "status": "unhealthy",
                "connection": "failed",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute query safely with proper error handling"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                if result.returns_rows:
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in result.fetchall()]
                return []
        except SQLAlchemyError as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in database query: {str(e)}")
            raise

# Global database manager instance
database_manager = DatabaseManager()