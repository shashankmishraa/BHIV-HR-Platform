#!/usr/bin/env python3
"""
BHIV HR Platform - Database Migration Manager
Handles database schema updates and data population
"""

import os
import sys
import psycopg2
from datetime import datetime
import json
import logging

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class DatabaseMigrationManager:
    """Comprehensive database migration and management"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for migration operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def get_connection(self):
        """Get database connection with error handling"""
        try:
            conn = psycopg2.connect(self.database_url)
            conn.autocommit = True
            return conn
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            return None
    
    def check_table_schema(self, table_name):
        """Check current table schema"""
        try:
            conn = self.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor()
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            
            columns = cursor.fetchall()
            conn.close()
            
            return {
                "table": table_name,
                "columns": [
                    {
                        "name": col[0],
                        "type": col[1],
                        "nullable": col[2] == "YES",
                        "default": col[3]
                    } for col in columns
                ]
            }
        except Exception as e:
            self.logger.error(f"Schema check failed for {table_name}: {e}")
            return None
    
    def run_migration_script(self, script_path):
        """Execute migration script"""
        try:
            if not os.path.exists(script_path):
                self.logger.error(f"Migration script not found: {script_path}")
                return False
            
            with open(script_path, 'r') as f:
                migration_sql = f.read()
            
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute(migration_sql)
            
            self.logger.info(f"Migration script executed successfully: {script_path}")
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Migration failed: {e}")
            return False
    
    def add_status_column_migration(self):
        """Add status column to candidates table"""
        migration_script = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "services", 
            "db", 
            "migrate_add_status.sql"
        )
        
        self.logger.info("Running status column migration...")
        return self.run_migration_script(migration_script)
    
    def populate_sample_candidates(self):
        """Populate database with sample candidates"""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Sample candidates data
            sample_candidates = [
                {
                    "name": "John Smith",
                    "email": "john.smith@email.com",
                    "phone": "+1-555-0101",
                    "location": "San Francisco, CA",
                    "experience_years": 5,
                    "technical_skills": "Python, Django, PostgreSQL, React, AWS",
                    "seniority_level": "Senior",
                    "education_level": "Bachelor's in Computer Science",
                    "status": "active"
                },
                {
                    "name": "Sarah Johnson",
                    "email": "sarah.johnson@email.com", 
                    "phone": "+1-555-0102",
                    "location": "New York, NY",
                    "experience_years": 3,
                    "technical_skills": "JavaScript, React, Node.js, MongoDB",
                    "seniority_level": "Mid-level",
                    "education_level": "Bachelor's in Software Engineering",
                    "status": "active"
                },
                {
                    "name": "Michael Chen",
                    "email": "michael.chen@email.com",
                    "phone": "+1-555-0103", 
                    "location": "Austin, TX",
                    "experience_years": 7,
                    "technical_skills": "Java, Spring Boot, Microservices, Docker, Kubernetes",
                    "seniority_level": "Senior",
                    "education_level": "Master's in Computer Science",
                    "status": "active"
                },
                {
                    "name": "Emily Davis",
                    "email": "emily.davis@email.com",
                    "phone": "+1-555-0104",
                    "location": "Seattle, WA", 
                    "experience_years": 2,
                    "technical_skills": "Python, Machine Learning, TensorFlow, Pandas",
                    "seniority_level": "Junior",
                    "education_level": "Bachelor's in Data Science",
                    "status": "active"
                },
                {
                    "name": "David Wilson",
                    "email": "david.wilson@email.com",
                    "phone": "+1-555-0105",
                    "location": "Remote",
                    "experience_years": 8,
                    "technical_skills": "DevOps, AWS, Terraform, Jenkins, CI/CD",
                    "seniority_level": "Senior",
                    "education_level": "Bachelor's in Information Technology",
                    "status": "active"
                }
            ]
            
            inserted_count = 0
            for candidate in sample_candidates:
                try:
                    # Check if candidate already exists
                    cursor.execute("SELECT COUNT(*) FROM candidates WHERE email = %s", (candidate["email"],))
                    if cursor.fetchone()[0] > 0:
                        self.logger.info(f"Candidate {candidate['email']} already exists, skipping")
                        continue
                    
                    # Insert candidate
                    cursor.execute("""
                        INSERT INTO candidates (name, email, phone, location, experience_years, 
                                              technical_skills, seniority_level, education_level, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        candidate["name"],
                        candidate["email"], 
                        candidate["phone"],
                        candidate["location"],
                        candidate["experience_years"],
                        candidate["technical_skills"],
                        candidate["seniority_level"],
                        candidate["education_level"],
                        candidate["status"]
                    ))
                    inserted_count += 1
                    self.logger.info(f"Inserted candidate: {candidate['name']}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to insert candidate {candidate['name']}: {e}")
                    continue
            
            conn.close()
            self.logger.info(f"Successfully inserted {inserted_count} candidates")
            return inserted_count > 0
            
        except Exception as e:
            self.logger.error(f"Sample data population failed: {e}")
            return False
    
    def verify_database_health(self):
        """Comprehensive database health check"""
        try:
            conn = self.get_connection()
            if not conn:
                return {"status": "error", "message": "Connection failed"}
            
            cursor = conn.cursor()
            
            # Check table existence and counts
            tables_info = {}
            tables = ["candidates", "jobs", "interviews", "feedback", "offers"]
            
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    tables_info[table] = {"count": count, "status": "ok"}
                except Exception as e:
                    tables_info[table] = {"count": 0, "status": "error", "error": str(e)}
            
            # Check candidates table schema
            candidates_schema = self.check_table_schema("candidates")
            has_status_column = any(col["name"] == "status" for col in candidates_schema["columns"]) if candidates_schema else False
            
            conn.close()
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "tables": tables_info,
                "candidates_schema_fixed": has_status_column,
                "total_candidates": tables_info.get("candidates", {}).get("count", 0)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def run_complete_migration(self):
        """Run complete database migration and setup"""
        self.logger.info("Starting complete database migration...")
        
        # Step 1: Check current state
        health_before = self.verify_database_health()
        self.logger.info(f"Database state before migration: {health_before}")
        
        # Step 2: Run status column migration
        if not health_before.get("candidates_schema_fixed", False):
            self.logger.info("Adding status column to candidates table...")
            if not self.add_status_column_migration():
                self.logger.error("Status column migration failed")
                return False
        else:
            self.logger.info("Status column already exists")
        
        # Step 3: Populate sample data if needed
        if health_before.get("total_candidates", 0) == 0:
            self.logger.info("Populating sample candidates...")
            if not self.populate_sample_candidates():
                self.logger.error("Sample data population failed")
                return False
        else:
            self.logger.info(f"Database already has {health_before.get('total_candidates', 0)} candidates")
        
        # Step 4: Verify final state
        health_after = self.verify_database_health()
        self.logger.info(f"Database state after migration: {health_after}")
        
        return health_after.get("status") == "healthy" and health_after.get("candidates_schema_fixed", False)

def main():
    """Main migration execution"""
    print("BHIV HR Platform - Database Migration Manager")
    print("=" * 50)
    
    manager = DatabaseMigrationManager()
    
    # Run complete migration
    success = manager.run_complete_migration()
    
    if success:
        print("\n✅ Database migration completed successfully!")
        print("- Status column added to candidates table")
        print("- Sample candidates populated")
        print("- Database health verified")
    else:
        print("\n❌ Database migration failed!")
        print("Check logs for details")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)