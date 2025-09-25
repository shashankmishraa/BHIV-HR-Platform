"""Database connection and utilities for BHIV HR Platform Gateway"""

import os
import asyncio
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database connection manager"""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.engine = None
        self.async_engine = None
        self.session_factory = None

    def get_connection_url(self) -> str:
        """Get database connection URL"""
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        return self.database_url

    def create_engine(self):
        """Create database engine"""
        if not self.engine:
            self.engine = create_engine(
                self.get_connection_url(),
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                echo=False,
            )
        return self.engine

    def create_async_engine(self):
        """Create async database engine"""
        if not self.async_engine:
            # Convert postgres:// to postgresql:// for async
            url = self.get_connection_url()
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)

            self.async_engine = create_async_engine(
                url, pool_size=10, max_overflow=20, pool_pre_ping=True, echo=False
            )
        return self.async_engine

    def get_session_factory(self):
        """Get session factory"""
        if not self.session_factory:
            engine = self.create_engine()
            self.session_factory = sessionmaker(bind=engine)
        return self.session_factory

    async def test_connection(self) -> Dict[str, Any]:
        """Test database connection"""
        try:
            engine = self.create_engine()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                row = result.fetchone()

            return {
                "status": "connected",
                "test_query": "passed",
                "database": "postgresql",
                "connection_pool": "healthy",
            }
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "database": "postgresql",
                "connection_pool": "failed",
            }

    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            engine = self.create_engine()
            with engine.connect() as conn:
                # Get table count
                tables_result = conn.execute(
                    text(
                        """
                    SELECT COUNT(*) as table_count 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """
                    )
                )
                table_count = tables_result.fetchone()[0]

                # Get database size
                size_result = conn.execute(
                    text(
                        """
                    SELECT pg_size_pretty(pg_database_size(current_database())) as db_size
                """
                    )
                )
                db_size = size_result.fetchone()[0]

                # Get connection count
                conn_result = conn.execute(
                    text(
                        """
                    SELECT COUNT(*) as active_connections 
                    FROM pg_stat_activity 
                    WHERE state = 'active'
                """
                    )
                )
                active_connections = conn_result.fetchone()[0]

            return {
                "total_tables": table_count,
                "database_size": db_size,
                "active_connections": active_connections,
                "max_connections": 100,
                "schema_version": "1.0",
            }
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {"error": str(e), "status": "failed"}


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_health() -> Dict[str, Any]:
    """Get database health status"""
    return await db_manager.test_connection()


async def get_db_stats() -> Dict[str, Any]:
    """Get database statistics"""
    return await db_manager.get_database_stats()
