"""Dynamic Data Loader for BHIV HR Platform"""

import os
import psycopg2
from typing import List, Dict, Any

class DynamicDataLoader:
    """Load data dynamically from database instead of static files"""
    
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
    
    def load_candidates(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Load candidates from database"""
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, email, phone, location, experience_years,
                       technical_skills, seniority_level, education_level
                FROM candidates 
                WHERE status = 'active'
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            
            candidates = []
            for row in cursor.fetchall():
                candidates.append({
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "phone": row[3],
                    "location": row[4],
                    "experience_years": row[5],
                    "technical_skills": row[6],
                    "seniority_level": row[7],
                    "education_level": row[8]
                })
            
            cursor.close()
            conn.close()
            return candidates
            
        except Exception as e:
            print(f"Error loading candidates: {e}")
            return []
    
    def load_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Load jobs from database"""
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, department, location, experience_level,
                       requirements, description, status
                FROM jobs 
                WHERE status = 'active'
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            
            jobs = []
            for row in cursor.fetchall():
                jobs.append({
                    "id": row[0],
                    "title": row[1],
                    "department": row[2],
                    "location": row[3],
                    "experience_level": row[4],
                    "requirements": row[5],
                    "description": row[6],
                    "status": row[7]
                })
            
            cursor.close()
            conn.close()
            return jobs
            
        except Exception as e:
            print(f"Error loading jobs: {e}")
            return []
    
    def get_skills_distribution(self) -> Dict[str, int]:
        """Get dynamic skills distribution from database"""
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT technical_skills
                FROM candidates 
                WHERE technical_skills IS NOT NULL
            """)
            
            skills_count = {}
            for row in cursor.fetchall():
                skills = row[0].split(',') if row[0] else []
                for skill in skills:
                    skill = skill.strip().lower()
                    if skill:
                        skills_count[skill] = skills_count.get(skill, 0) + 1
            
            cursor.close()
            conn.close()
            return skills_count
            
        except Exception as e:
            print(f"Error getting skills distribution: {e}")
            return {}

# Global instance
dynamic_loader = DynamicDataLoader()
