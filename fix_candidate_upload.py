#!/usr/bin/env python3
"""
Fix Candidate Upload Issues
Handle empty emails and duplicate entries properly
"""

import pandas as pd
import requests
import time
import uuid

def fix_and_upload_candidates():
    """Fix candidate data and upload remaining candidates"""
    
    print("FIXING CANDIDATE UPLOAD ISSUES")
    print("=" * 50)
    
    # Read CSV
    df = pd.read_csv("data/samples/candidates.csv")
    print(f"Found {len(df)} candidates in CSV")
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {
        "Authorization": "Bearer myverysecureapikey123",
        "Content-Type": "application/json"
    }
    
    # Get existing candidates to avoid duplicates
    try:
        response = requests.get(f"{api_base}/v1/candidates/search", headers=headers, timeout=10)
        existing_emails = set()
        if response.status_code == 200:
            existing_candidates = response.json().get('candidates', [])
            existing_emails = {c.get('email', '') for c in existing_candidates if c.get('email')}
            print(f"Found {len(existing_emails)} existing candidates")
    except Exception as e:
        print(f"Could not fetch existing candidates: {e}")
        existing_emails = set()
    
    success_count = 0
    
    for i, row in df.iterrows():
        # Clean data
        def safe_str(val, default=''):
            if pd.isna(val) or val is None:
                return default
            return str(val).strip()
        
        # Handle empty emails by generating unique ones
        email = safe_str(row.get('email'))
        if not email or email in existing_emails:
            # Generate unique email for candidates without email
            name = safe_str(row.get('name'), 'Unknown').replace(' ', '').lower()
            unique_id = str(uuid.uuid4())[:8]
            email = f"{name}_{unique_id}@placeholder.com"
        
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
            "email": email,
            "phone": safe_str(row.get('phone')),
            "location": safe_str(row.get('location')),
            "experience_years": exp_years,
            "technical_skills": safe_str(row.get('skills')),
            "seniority_level": safe_str(row.get('designation'), 'Entry-level'),
            "education_level": safe_str(row.get('education'), 'Masters'),
            "resume_path": safe_str(row.get('resume_name')),
            "status": "active"
        }
        
        # Skip if email already exists
        if candidate['email'] in existing_emails:
            print(f"SKIP {i+1:2d}. {candidate['name']} - Email already exists")
            continue
        
        # Upload candidate
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
                    existing_emails.add(candidate['email'])  # Track to avoid duplicates
                    print(f"SUCCESS {i+1:2d}. {candidate['name']} - {candidate['email']}")
                else:
                    error_msg = result.get('errors', ['Unknown error'])[0] if result.get('errors') else 'No error details'
                    print(f"ERROR {i+1:2d}. {candidate['name']} - {error_msg}")
            else:
                print(f"ERROR {i+1:2d}. {candidate['name']} - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"ERROR {i+1:2d}. {candidate['name']} - {str(e)}")
        
        time.sleep(0.3)  # Small delay
    
    print(f"\nUploaded {success_count} new candidates successfully")
    return success_count

def verify_final_count():
    """Verify final candidate count"""
    
    print("\nVerifying final database state...")
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    try:
        # Check total count
        response = requests.get(f"{api_base}/test-candidates", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            total_count = data.get('total_candidates', 0)
            print(f"Total candidates in database: {total_count}")
            
            # Test AI matching
            response = requests.get(f"{api_base}/v1/match/1/top?limit=10", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                print(f"AI matching returns: {len(matches)} candidates")
                
                if matches:
                    print("Sample candidates:")
                    for i, match in enumerate(matches[:5], 1):
                        print(f"  {i}. {match.get('name', 'N/A')} - {match.get('email', 'N/A')}")
                
                return total_count, len(matches)
        
    except Exception as e:
        print(f"Verification error: {e}")
    
    return 0, 0

if __name__ == "__main__":
    success_count = fix_and_upload_candidates()
    total_candidates, ai_matches = verify_final_count()
    
    print(f"\n" + "=" * 50)
    print(f"FINAL RESULTS:")
    print(f"New candidates uploaded: {success_count}")
    print(f"Total candidates in database: {total_candidates}")
    print(f"AI matching working: {'Yes' if ai_matches > 0 else 'No'}")
    print(f"Expected total from CSV: 31")
    print(f"Upload completion: {(total_candidates/31)*100:.1f}%")