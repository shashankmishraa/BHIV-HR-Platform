# Database Initialization for BHIV HR Platform

import os
from sqlalchemy import create_engine, text
from datetime import datetime

def initialize_render_database():
    """Initialize database schema and sample data for Render deployment"""
    try:
        database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        engine = create_engine(database_url, pool_pre_ping=True)
        
        with engine.connect() as connection:
            # Test connection
            connection.execute(text("SELECT 1"))
            
            # Create tables if they don't exist
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    technical_skills TEXT,
                    experience_years INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            connection.execute(text("""
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            connection.commit()
            
            return {
                "message": "Database initialized successfully",
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "message": f"Database initialization failed: {str(e)}",
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }