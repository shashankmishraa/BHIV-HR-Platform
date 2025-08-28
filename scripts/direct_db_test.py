import os
from sqlalchemy import create_engine, text

def test_direct_insert():
    """Test direct database insert with enhanced fields"""
    
    database_url = "postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr"
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as connection:
            # Insert test candidate directly
            query = text("""
                INSERT INTO candidates (job_id, name, email, phone, location, cv_url, 
                                      experience_years, education_level, technical_skills, 
                                      seniority_level, status, created_at)
                VALUES (:job_id, :name, :email, :phone, :location, :cv_url, 
                        :experience_years, :education_level, :technical_skills, 
                        :seniority_level, :status, NOW())
                RETURNING id
            """)
            
            result = connection.execute(query, {
                "job_id": 1,
                "name": "Direct Test Candidate",
                "email": "direct@test.com",
                "phone": "+1-555-9999",
                "location": "Test City",
                "cv_url": "https://example.com/direct.pdf",
                "experience_years": 3,
                "education_level": "Bachelors",
                "technical_skills": "Python, React, Docker",
                "seniority_level": "Mid-level",
                "status": "applied"
            })
            
            candidate_id = result.fetchone()[0]
            connection.commit()
            
            print(f"Inserted candidate with ID: {candidate_id}")
            
            # Retrieve and verify
            query = text("""
                SELECT name, seniority_level, technical_skills, education_level, location
                FROM candidates 
                WHERE id = :id
            """)
            
            result = connection.execute(query, {"id": candidate_id})
            row = result.fetchone()
            
            if row:
                print(f"Retrieved:")
                print(f"  Name: {row[0]}")
                print(f"  Seniority: {row[1]}")
                print(f"  Skills: {row[2]}")
                print(f"  Education: {row[3]}")
                print(f"  Location: {row[4]}")
            else:
                print("No data retrieved")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_direct_insert()