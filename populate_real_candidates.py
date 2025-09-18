#!/usr/bin/env python3
"""
Populate Database with Real Candidates
Load actual candidate data from CSV into the database
"""

import pandas as pd
import requests
import json

def populate_candidates():
    """Load real candidates from CSV into database"""
    
    print("POPULATING DATABASE WITH REAL CANDIDATES")
    print("=" * 50)
    
    # Read CSV data
    csv_file = "data/samples/candidates.csv"
    try:
        df = pd.read_csv(csv_file)
        print(f"Found {len(df)} candidates in CSV")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False
    
    # Convert to database format
    candidates = []
    for _, row in df.iterrows():
        # Parse experience
        exp_str = str(row.get('experience', 'Fresher')).lower()
        if 'year' in exp_str:
            try:
                exp_years = int(''.join(filter(str.isdigit, exp_str)))
            except:
                exp_years = 0
        elif exp_str == 'fresher':
            exp_years = 0
        else:
            exp_years = 1
        
        # Handle NaN values
        def safe_str(val, default=''):
            if pd.isna(val) or val is None:
                return default
            return str(val).strip()
        
        candidate = {
            "name": safe_str(row.get('name'), 'Unknown'),
            "email": safe_str(row.get('email')),
            "phone": safe_str(row.get('phone')),
            "location": safe_str(row.get('location')),
            "experience_years": exp_years,
            "technical_skills": safe_str(row.get('skills')),
            "seniority_level": safe_str(row.get('designation'), 'Entry-level'),
            "education_level": safe_str(row.get('education'), 'Masters'),
            "resume_path": safe_str(row.get('resume_name')),
            "status": "active"
        }
        candidates.append(candidate)
    
    # Upload to database
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {
        "Authorization": "Bearer myverysecureapikey123",
        "Content-Type": "application/json"
    }
    
    print(f"Uploading {len(candidates)} candidates to database...")
    
    try:
        response = requests.post(
            f"{api_base}/v1/candidates/bulk",
            headers=headers,
            json={"candidates": candidates},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Uploaded {result.get('candidates_inserted', 0)} candidates")
            if result.get('errors'):
                print(f"Errors: {len(result.get('errors', []))}")
            return True
        else:
            print(f"ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def verify_upload():
    """Verify candidates were uploaded"""
    
    print("\nVerifying upload...")
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    try:
        response = requests.get(f"{api_base}/test-candidates", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = data.get('total_candidates', 0)
            print(f"Database now contains {count} candidates")
            return count > 0
        else:
            print(f"Verification failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def test_ai_matching():
    """Test AI matching with real data"""
    
    print("\nTesting AI matching...")
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    try:
        response = requests.get(f"{api_base}/v1/match/1/top?limit=5", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            print(f"AI matching returned {len(matches)} candidates")
            
            if matches:
                first = matches[0]
                print(f"First candidate: {first.get('name', 'N/A')}")
                print(f"Email: {first.get('email', 'N/A')}")
                print(f"Score: {first.get('score', 'N/A')}")
                return True
            else:
                print("No candidates returned by AI matching")
                return False
        else:
            print(f"AI matching failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"AI matching error: {e}")
        return False

if __name__ == "__main__":
    success = populate_candidates()
    if success:
        verify_upload()
        test_ai_matching()
    
    print("\nDone!")