#!/usr/bin/env python3
"""
Simple Candidate Upload Script
Upload real candidates one by one to avoid bulk upload issues
"""

import pandas as pd
import requests
import time

def upload_candidates_individually():
    """Upload candidates one by one"""
    
    print("UPLOADING REAL CANDIDATES INDIVIDUALLY")
    print("=" * 50)
    
    # Read CSV
    df = pd.read_csv("data/samples/candidates.csv")
    print(f"Found {len(df)} candidates")
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {
        "Authorization": "Bearer myverysecureapikey123",
        "Content-Type": "application/json"
    }
    
    success_count = 0
    
    for i, row in df.iterrows():
        # Clean data
        def safe_str(val, default=''):
            if pd.isna(val) or val is None:
                return default
            return str(val).strip()
        
        # Parse experience
        exp_str = safe_str(row.get('experience', 'Fresher')).lower()
        exp_years = 0
        if 'year' in exp_str:
            try:
                exp_years = int(''.join(filter(str.isdigit, exp_str)))
            except:
                exp_years = 0
        
        candidate = {
            "name": safe_str(row.get('name'), 'Unknown'),
            "email": safe_str(row.get('email')),
            "phone": safe_str(row.get('phone')),
            "location": safe_str(row.get('location')),
            "experience_years": exp_years,
            "technical_skills": safe_str(row.get('skills')),
            "seniority_level": safe_str(row.get('designation'), 'Entry-level'),
            "education_level": safe_str(row.get('education'), 'Masters'),
            "resume_path": safe_str(row.get('resume_name'))
        }
        
        # Upload single candidate
        try:
            response = requests.post(
                f"{api_base}/v1/candidates/bulk",
                headers=headers,
                json={"candidates": [candidate]},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('candidates_inserted', 0) > 0:
                    success_count += 1
                    print(f"SUCCESS {i+1:2d}. {candidate['name']}")
                else:
                    print(f"ERROR {i+1:2d}. {candidate['name']} - {result.get('errors', ['Unknown error'])[0] if result.get('errors') else 'No error details'}")
            else:
                print(f"ERROR {i+1:2d}. {candidate['name']} - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"ERROR {i+1:2d}. {candidate['name']} - {str(e)}")
        
        time.sleep(0.5)  # Small delay to avoid rate limiting
    
    print(f"\nUploaded {success_count}/{len(df)} candidates successfully")
    return success_count

def verify_and_test():
    """Verify upload and test AI matching"""
    
    print("\nVerifying database...")
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    # Check candidate count
    try:
        response = requests.get(f"{api_base}/test-candidates", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = data.get('total_candidates', 0)
            print(f"Database contains {count} candidates")
            
            if count > 0:
                # Test AI matching
                print("\nTesting AI matching...")
                response = requests.get(f"{api_base}/v1/match/1/top?limit=5", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get('matches', [])
                    print(f"AI matching returned {len(matches)} candidates")
                    
                    if matches:
                        for i, match in enumerate(matches[:3], 1):
                            print(f"  {i}. {match.get('name', 'N/A')} - Score: {match.get('score', 'N/A')}")
                        return True
                    else:
                        print("No matches returned")
                else:
                    print(f"AI matching failed: HTTP {response.status_code}")
            else:
                print("No candidates in database")
        else:
            print(f"Verification failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"Verification error: {e}")
    
    return False

if __name__ == "__main__":
    success_count = upload_candidates_individually()
    if success_count > 0:
        verify_and_test()
    else:
        print("No candidates uploaded successfully")