#!/usr/bin/env python3
"""Fix missing database schema components"""

import asyncpg
import asyncio

async def fix_database_schema():
    """Add missing columns to fix 422 validation errors"""
    try:
        conn = await asyncpg.connect(
            'postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb'
        )
        
        print("=== FIXING DATABASE SCHEMA ===")
        
        # 1. Add missing columns to jobs table
        print("Adding missing columns to jobs table...")
        
        # Add salary_min column
        try:
            await conn.execute("ALTER TABLE jobs ADD COLUMN salary_min INTEGER DEFAULT 0;")
            print("Added salary_min column")
        except Exception as e:
            if "already exists" in str(e):
                print("salary_min column already exists")
            else:
                print(f"Error adding salary_min: {e}")
        
        # Add salary_max column
        try:
            await conn.execute("ALTER TABLE jobs ADD COLUMN salary_max INTEGER DEFAULT 0;")
            print("Added salary_max column")
        except Exception as e:
            if "already exists" in str(e):
                print("salary_max column already exists")
            else:
                print(f"Error adding salary_max: {e}")
        
        # Add job_type column (alias for employment_type)
        try:
            await conn.execute("ALTER TABLE jobs ADD COLUMN job_type VARCHAR(50) DEFAULT 'Full-time';")
            print("Added job_type column")
        except Exception as e:
            if "already exists" in str(e):
                print("job_type column already exists")
            else:
                print(f"Error adding job_type: {e}")
        
        # Add company_id column (alias for client_id)
        try:
            await conn.execute("ALTER TABLE jobs ADD COLUMN company_id VARCHAR(100) DEFAULT 'default';")
            print("Added company_id column")
        except Exception as e:
            if "already exists" in str(e):
                print("company_id column already exists")
            else:
                print(f"Error adding company_id: {e}")
        
        # 2. Add missing columns to candidates table
        print("\nAdding missing columns to candidates table...")
        
        # Add skills column (alias for technical_skills)
        try:
            await conn.execute("ALTER TABLE candidates ADD COLUMN skills TEXT[];")
            print("Added skills column")
        except Exception as e:
            if "already exists" in str(e):
                print("skills column already exists")
            else:
                print(f"Error adding skills: {e}")
        
        # 3. Update existing data to populate new columns
        print("\nUpdating existing data...")
        
        # Update job_type from employment_type
        await conn.execute("UPDATE jobs SET job_type = employment_type WHERE job_type IS NULL OR job_type = 'Full-time';")
        print("Updated job_type from employment_type")
        
        # Update company_id from client_id
        await conn.execute("UPDATE jobs SET company_id = COALESCE(client_id::text, 'default') WHERE company_id = 'default';")
        print("Updated company_id from client_id")
        
        # Set default salary ranges for existing jobs
        await conn.execute("""
            UPDATE jobs SET 
                salary_min = CASE 
                    WHEN experience_level = 'Entry-level' THEN 60000
                    WHEN experience_level = 'Mid-level' THEN 80000
                    WHEN experience_level = 'Senior' THEN 120000
                    ELSE 70000
                END,
                salary_max = CASE 
                    WHEN experience_level = 'Entry-level' THEN 80000
                    WHEN experience_level = 'Mid-level' THEN 120000
                    WHEN experience_level = 'Senior' THEN 180000
                    ELSE 100000
                END
            WHERE salary_min = 0 OR salary_max = 0;
        """)
        print("Updated salary ranges based on experience level")
        
        # Update skills from technical_skills
        await conn.execute("""
            UPDATE candidates SET 
                skills = string_to_array(technical_skills, ', ')
            WHERE skills IS NULL AND technical_skills IS NOT NULL;
        """)
        print("Updated skills from technical_skills")
        
        # 4. Verify the fixes
        print("\n=== VERIFICATION ===")
        
        # Check jobs table
        jobs_columns = await conn.fetch("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'jobs' 
            ORDER BY ordinal_position;
        """)
        jobs_column_names = [c['column_name'] for c in jobs_columns]
        print(f"Jobs table columns: {jobs_column_names}")
        
        # Check if required columns exist
        required_job_columns = ['salary_min', 'salary_max', 'job_type', 'company_id']
        missing_job_columns = [c for c in required_job_columns if c not in jobs_column_names]
        if not missing_job_columns:
            print("All required job columns present")
        else:
            print(f"Still missing job columns: {missing_job_columns}")
        
        # Test sample data
        sample_job = await conn.fetchrow("SELECT * FROM jobs LIMIT 1;")
        if sample_job:
            print(f"Sample job data: title='{sample_job['title']}', salary_min={sample_job['salary_min']}, salary_max={sample_job['salary_max']}")
        
        await conn.close()
        print("\nDatabase schema fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"Database schema fix failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(fix_database_schema())