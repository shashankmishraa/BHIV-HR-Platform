import pandas as pd
import requests
import json

# Configuration
API_BASE = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def upload_csv_candidates():
    """Upload candidates from CSV to platform"""
    print("Loading candidates from enhanced_candidates.csv...")
    
    try:
        df = pd.read_csv('data/enhanced_candidates.csv')
        print(f"Found {len(df)} candidates in CSV")
        
        candidates = []
        for _, row in df.iterrows():
            candidate = {
                "name": str(row['name']),
                "email": str(row['email']) if pd.notna(row['email']) else "",
                "phone": str(row['phone']) if pd.notna(row['phone']) else "",
                "location": str(row['location']) if pd.notna(row['location']) else "",
                "experience_years": int(row['experience_years']) if pd.notna(row['experience_years']) else 0,
                "technical_skills": str(row['technical_skills']) if pd.notna(row['technical_skills']) else "",
                "seniority_level": str(row['seniority_level']) if pd.notna(row['seniority_level']) else "",
                "education_level": str(row['education_level']) if pd.notna(row['education_level']) else "",
                "cv_url": str(row['cv_url']) if pd.notna(row['cv_url']) else "",
                "job_id": 1,  # Assign to job ID 1
                "status": "applied"
            }
            candidates.append(candidate)
        
        # Upload in batches of 10
        batch_size = 10
        total_uploaded = 0
        
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i:i+batch_size]
            
            try:
                response = requests.post(
                    f"{API_BASE}/v1/candidates/bulk",
                    headers=HEADERS,
                    json={"candidates": batch},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    uploaded = result.get('count', 0)
                    total_uploaded += uploaded
                    print(f"Batch {i//batch_size + 1}: Uploaded {uploaded} candidates")
                else:
                    print(f"Batch {i//batch_size + 1}: Failed - {response.status_code}")
                    
            except Exception as e:
                print(f"Batch {i//batch_size + 1}: Error - {str(e)}")
        
        print(f"\nTotal uploaded: {total_uploaded}/{len(candidates)} candidates")
        
        # Verify upload
        response = requests.get(f"{API_BASE}/candidates/stats", headers=HEADERS)
        if response.status_code == 200:
            stats = response.json()
            print(f"Database now has {stats.get('total_candidates', 0)} total candidates")
        
        return total_uploaded
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 0

if __name__ == "__main__":
    upload_csv_candidates()