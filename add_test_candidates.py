#!/usr/bin/env python3
"""
Add real test candidates to database
"""
import requests
import sys

BASE_URL = "http://localhost:8000"
LOCAL_API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {LOCAL_API_KEY}", "Content-Type": "application/json"}

def add_real_candidates():
    """Add realistic candidate data"""
    print("=== Adding Real Test Candidates ===")
    
    candidates = [
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "+1-555-0101",
            "location": "San Francisco, CA",
            "experience_years": 5,
            "technical_skills": "Python, FastAPI, PostgreSQL, Docker, React, AWS, Machine Learning, REST APIs, Git",
            "seniority_level": "Senior Developer",
            "education_level": "Bachelor's in Computer Science",
            "status": "applied"
        },
        {
            "name": "Michael Chen",
            "email": "michael.chen@email.com", 
            "phone": "+1-555-0102",
            "location": "Seattle, WA",
            "experience_years": 3,
            "technical_skills": "JavaScript, Node.js, React, MongoDB, Express, TypeScript, GraphQL, Jest",
            "seniority_level": "Mid-level Developer",
            "education_level": "Bachelor's in Software Engineering",
            "status": "applied"
        },
        {
            "name": "Emily Rodriguez",
            "email": "emily.rodriguez@email.com",
            "phone": "+1-555-0103", 
            "location": "Austin, TX",
            "experience_years": 7,
            "technical_skills": "Python, Django, PostgreSQL, Redis, Celery, Docker, Kubernetes, AWS, CI/CD",
            "seniority_level": "Senior Developer",
            "education_level": "Master's in Computer Science",
            "status": "applied"
        },
        {
            "name": "David Kumar",
            "email": "david.kumar@email.com",
            "phone": "+1-555-0104",
            "location": "New York, NY", 
            "experience_years": 4,
            "technical_skills": "Java, Spring Boot, MySQL, Microservices, Docker, Jenkins, REST APIs, JUnit",
            "seniority_level": "Senior Developer",
            "education_level": "Bachelor's in Information Technology",
            "status": "applied"
        },
        {
            "name": "Lisa Wang",
            "email": "lisa.wang@email.com",
            "phone": "+1-555-0105",
            "location": "Remote",
            "experience_years": 6,
            "technical_skills": "Python, Flask, SQLAlchemy, Redis, Docker, AWS, Machine Learning, Pandas, NumPy",
            "seniority_level": "Senior Developer", 
            "education_level": "PhD in Data Science",
            "status": "applied"
        },
        {
            "name": "James Thompson",
            "email": "james.thompson@email.com",
            "phone": "+1-555-0106",
            "location": "Chicago, IL",
            "experience_years": 2,
            "technical_skills": "React, JavaScript, HTML, CSS, Node.js, MongoDB, Git, Agile",
            "seniority_level": "Junior Developer",
            "education_level": "Bachelor's in Web Development",
            "status": "applied"
        }
    ]
    
    try:
        payload = {"candidates": candidates}
        response = requests.post(f"{BASE_URL}/v1/candidates/bulk", headers=HEADERS, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Bulk upload completed")
            print(f"  Candidates received: {data.get('candidates_received', 0)}")
            print(f"  Candidates inserted: {data.get('candidates_inserted', 0)}")
            print(f"  Status: {data.get('status')}")
            
            if data.get('errors'):
                print(f"  Errors: {len(data.get('errors', []))}")
                for error in data.get('errors', [])[:3]:
                    print(f"    - {error}")
            
            return data.get('candidates_inserted', 0) > 0
        else:
            print(f"FAILED: Bulk upload returned {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"FAILED: Bulk upload error - {e}")
        return False

def verify_candidates():
    """Verify candidates were added"""
    print("\n=== Verifying Candidates ===")
    
    try:
        response = requests.get(f"{BASE_URL}/v1/candidates", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            total = data.get('total', 0)
            print(f"SUCCESS: Found {len(candidates)} candidates (Total: {total})")
            
            for i, candidate in enumerate(candidates[:3]):
                print(f"  {i+1}. {candidate.get('name')} - {candidate.get('experience_years')}y exp")
                print(f"     Skills: {candidate.get('technical_skills', '')[:50]}...")
            
            return total > 0
        else:
            print(f"FAILED: Verification returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Verification error - {e}")
        return False

def main():
    """Add candidates and verify"""
    print("=== Adding Real Test Candidates to Database ===\n")
    
    # Add candidates
    success = add_real_candidates()
    
    if success:
        # Verify they were added
        verify_success = verify_candidates()
        
        if verify_success:
            print("\nSUCCESS: Real candidates added and verified!")
            print("Ready for comprehensive endpoint testing")
            return 0
        else:
            print("\nWARNING: Candidates added but verification failed")
            return 1
    else:
        print("\nFAILED: Could not add candidates")
        return 1

if __name__ == "__main__":
    sys.exit(main())