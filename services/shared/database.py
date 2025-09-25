"""Shared database utilities for BHIV HR Platform Services"""

import os
import psycopg2
from contextlib import contextmanager
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Shared database manager for all services"""

    def __init__(self):
        self.database_url = self._get_database_url()

    def _get_database_url(self) -> str:
        """Get database URL based on environment"""
        environment = os.getenv("ENVIRONMENT", "development").lower()

        if environment == "production":
            # Production database on Render
            return os.getenv(
                "DATABASE_URL",
                "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb",
            )
        else:
            # Local development database
            return os.getenv(
                "DATABASE_URL",
                "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb",
            )

    @contextmanager
    def get_connection(self):
        """Get database connection with proper resource management"""
        conn = None
        try:
            conn = psycopg2.connect(self.database_url)
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def test_connection(self) -> Dict[str, Any]:
        """Test database connectivity"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
            return {"status": "connected", "database": "postgresql"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_candidates_count(self) -> int:
        """Get total candidates count"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM candidates")
                    return cursor.fetchone()[0]
        except Exception:
            return 0

    def get_jobs_count(self) -> int:
        """Get total jobs count"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM jobs")
                    return cursor.fetchone()[0]
        except Exception:
            return 0


# Global database manager instance
db_manager = DatabaseManager()


def get_db_connection():
    """Get database connection context manager"""
    return db_manager.get_connection()
