import pandas as pd
import requests
import json
import time

def upload_enhanced_candidates():
    """Upload enhanced candidates to the API"""
    
    # Read the enhanced CSV
    try:
        df = pd.read_csv('../data/enhanced_candidates.csv')
        print(f"Loaded {len(df)} enhanced candidates from CSV")
    except FileNotFoundError:
        print("Enhanced candidates CSV not found. Run simple_enhanced_processor.py first.")
        return
    
    # API configuration
    api_url = "http://localhost:8000/v1/candidates/bulk"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "myverysecureapikey123"
    }
    
    # Convert DataFrame to API format
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
    payload = {"candidates": candidates}
    
    try:
        print("Uploading enhanced candidates to API...")
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Uploaded {result.get('count', 0)} candidates")
            print(f"Message: {result.get('message', 'No message')}")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running.")
        print("Run: docker compose up --build")
    except Exception as e:
        print(f"Error uploading candidates: {e}")

def test_enhanced_endpoints():
    """Test the enhanced API endpoints"""
    
    base_url = "http://localhost:8000"
    headers = {"X-API-KEY": "myverysecureapikey123"}
    
    print("\nTesting enhanced API endpoints...")
    
    # Test 1: Get candidates for job 1
    try:
        response = requests.get(f"{base_url}/v1/candidates/job/1", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Retrieved {data.get('count', 0)} candidates for job 1")
            if data.get('candidates'):
                sample = data['candidates'][0]
                print(f"  Sample: {sample.get('name')} - {sample.get('seniority_level')} - {sample.get('technical_skills')}")
        else:
            print(f"✗ Failed to get candidates: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing candidates endpoint: {e}")
    
    # Test 2: Get AI matching
    try:
        response = requests.get(f"{base_url}/v1/match/1/top", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ AI matching working - got {len(data.get('top_candidates', []))} top candidates")
        else:
            print(f"✗ AI matching failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing AI matching: {e}")
    
    # Test 3: Submit values feedback
    try:
        feedback_data = {
            "candidate_id": 1,
            "reviewer_name": "Test Reviewer",
            "feedback_text": "Excellent technical skills and cultural fit",
            "values_scores": {
                "integrity": 5,
                "honesty": 4,
                "discipline": 5,
                "hard_work": 5,
                "gratitude": 4
            },
            "overall_recommendation": "Strongly Recommend"
        }
        
        response = requests.post(f"{base_url}/v1/feedback", headers=headers, json=feedback_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Values feedback submitted - ID: {data.get('feedback_id')}")
            print(f"  Average score: {data.get('values_summary', {}).get('average_score', 'N/A')}")
        else:
            print(f"✗ Values feedback failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing values feedback: {e}")
    
    # Test 4: Get statistics
    try:
        response = requests.get(f"{base_url}/candidates/stats", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Statistics: {data.get('total_candidates')} candidates, {data.get('total_jobs')} jobs, {data.get('total_feedback')} feedback")
        else:
            print(f"✗ Statistics failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing statistics: {e}")

if __name__ == "__main__":
    print("Enhanced Candidates Upload & Test Script")
    print("=" * 50)
    
    # Upload candidates
    upload_enhanced_candidates()
    
    # Wait a moment for processing
    time.sleep(2)
    
    # Test endpoints
    test_enhanced_endpoints()
    
    print("\nDone! Check the portal at http://localhost:8501 to see enhanced data.")