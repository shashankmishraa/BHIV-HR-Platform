#!/usr/bin/env python3
"""Remove static/mock data and replace with dynamic alternatives"""

import os
import shutil

def remove_static_data():
    """Remove static data files and mock implementations"""
    
    # Files to remove or clean up
    static_files = [
        "data/samples/candidates.csv",  # Static candidate data
        "models/job_templates.json",    # Static job templates
        "models/skill_embeddings.pkl",  # Static skill embeddings
    ]
    
    removed_files = []
    
    for file_path in static_files:
        full_path = os.path.join("c:/bhiv hr ai platform", file_path)
        if os.path.exists(full_path):
            try:
                # Move to archive instead of deleting
                archive_dir = os.path.join("c:/bhiv hr ai platform", "data/archive")
                os.makedirs(archive_dir, exist_ok=True)
                
                filename = os.path.basename(full_path)
                archive_path = os.path.join(archive_dir, f"archived_{filename}")
                
                shutil.move(full_path, archive_path)
                removed_files.append(f"{file_path} -> archived")
                print(f"Archived: {file_path}")
            except Exception as e:
                print(f"Error archiving {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")
    
    return removed_files

def create_dynamic_alternatives():
    """Create dynamic data loading alternatives"""
    
    # Create dynamic candidate loader
    dynamic_loader = '''"""Dynamic Data Loader for BHIV HR Platform"""

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
'''
    
    # Write dynamic loader
    loader_path = "c:/bhiv hr ai platform/services/shared/dynamic_loader.py"
    os.makedirs(os.path.dirname(loader_path), exist_ok=True)
    
    with open(loader_path, 'w') as f:
        f.write(dynamic_loader)
    
    print(f"Created: {loader_path}")
    
    return ["services/shared/dynamic_loader.py"]

def main():
    """Main function to remove static data and create dynamic alternatives"""
    print("Removing Static Data and Creating Dynamic Alternatives")
    print("=" * 60)
    
    # Remove static files
    print("Archiving static data files...")
    removed = remove_static_data()
    
    # Create dynamic alternatives
    print("Creating dynamic data loaders...")
    created = create_dynamic_alternatives()
    
    print("\n" + "=" * 60)
    print("Static Data Migration Complete")
    print(f"Archived files: {len(removed)}")
    print(f"Created files: {len(created)}")
    
    if removed:
        print("\nArchived files:")
        for file in removed:
            print(f"  - {file}")
    
    if created:
        print("\nCreated files:")
        for file in created:
            print(f"  - {file}")
    
    print("\nNext steps:")
    print("  1. Update services to use dynamic_loader instead of static files")
    print("  2. Test all endpoints with dynamic data")
    print("  3. Verify database connectivity and data integrity")

if __name__ == "__main__":
    main()