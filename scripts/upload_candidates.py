import pandas as pd
import requests
import json

def upload_candidates():
    try:
        # Read processed candidates
        df = pd.read_csv('data/clean_candidates.csv')
        print(f"Loaded {len(df)} candidates from CSV")
        
        # Convert to API format
        candidates = []
        for _, row in df.iterrows():
            candidate = {
                "name": str(row['name']),
                "email": str(row['email']),
                "phone": str(row['phone']),
                "location": str(row['location']),
                "cv_url": str(row['cv_url']),
                "experience_years": int(row['experience_years']),
                "education_level": str(row['education_level']),
                "technical_skills": str(row['technical_skills']),
                "seniority_level": str(row['seniority_level']),
                "status": str(row['status']),
                "job_id": int(row['job_id'])
            }
            candidates.append(candidate)
        
        # Upload to API
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer myverysecureapikey123"
        }
        
        response = requests.post(
            "http://localhost:8000/v1/candidates/bulk",
            headers=headers,
            json={"candidates": candidates}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Successfully uploaded {result.get('count', 0)} candidates")
        else:
            print(f"Upload failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_candidates()