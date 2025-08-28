import pandas as pd
import requests
import json

def upload_all_enhanced_candidates():
    """Upload all enhanced candidates and verify system works with real data"""
    
    # Read enhanced CSV
    df = pd.read_csv('../data/enhanced_candidates.csv')
    print(f"Loading {len(df)} enhanced candidates...")
    
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
            "status": "applied",
            "job_id": 1
        }
        candidates.append(candidate)
    
    # Upload via API
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "myverysecureapikey123"
    }
    
    response = requests.post(
        "http://localhost:8000/v1/candidates/bulk",
        headers=headers,
        json={"candidates": candidates}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"SUCCESS: Uploaded {result.get('count')} candidates")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")
        return False
    
    return True

def test_enhanced_system():
    """Test all system components with enhanced data"""
    
    headers = {"X-API-KEY": "myverysecureapikey123"}
    base_url = "http://localhost:8000"
    
    print("\nTesting Enhanced BHIV HR Platform")
    print("=" * 50)
    
    # Test 1: Retrieve enhanced candidates
    response = requests.get(f"{base_url}/v1/candidates/job/1", headers=headers)
    if response.status_code == 200:
        data = response.json()
        candidates = data.get('candidates', [])
        print(f"✓ Retrieved {len(candidates)} enhanced candidates")
        
        # Show sample enhanced data
        if candidates:
            sample = candidates[0]
            print(f"  Sample: {sample.get('name')}")
            print(f"  Skills: {sample.get('technical_skills')}")
            print(f"  Seniority: {sample.get('seniority_level')}")
            print(f"  Education: {sample.get('education_level')}")
            print(f"  Location: {sample.get('location')}")
    else:
        print(f"✗ Failed to retrieve candidates: {response.status_code}")
    
    # Test 2: AI Matching with enhanced data
    response = requests.get(f"{base_url}/v1/match/1/top", headers=headers)
    if response.status_code == 200:
        data = response.json()
        top_candidates = data.get('top_candidates', [])
        print(f"\n✓ AI Matching: {len(top_candidates)} top candidates")
        for i, candidate in enumerate(top_candidates[:3], 1):
            print(f"  #{i}: {candidate.get('name')} (Score: {candidate.get('score')})")
    else:
        print(f"\n✗ AI Matching failed: {response.status_code}")
    
    # Test 3: Values-based feedback
    feedback_data = {
        "candidate_id": 1,
        "reviewer_name": "Senior HR Manager",
        "feedback_text": "Excellent technical skills with strong cultural alignment",
        "values_scores": {
            "integrity": 5,
            "honesty": 5,
            "discipline": 4,
            "hard_work": 5,
            "gratitude": 4
        },
        "overall_recommendation": "Strongly Recommend"
    }
    
    response = requests.post(f"{base_url}/v1/feedback", headers=headers, json=feedback_data)
    if response.status_code == 200:
        data = response.json()
        avg_score = data.get('values_summary', {}).get('average_score', 0)
        print(f"\n✓ Values Feedback: Average score {avg_score}/5")
    else:
        print(f"\n✗ Values feedback failed: {response.status_code}")
    
    # Test 4: Interview scheduling
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-02-01T10:00:00Z",
        "interviewer": "Tech Lead"
    }
    
    response = requests.post(f"{base_url}/v1/interviews", headers=headers, json=interview_data)
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Interview Scheduled: ID {data.get('interview_id')}")
    else:
        print(f"\n✗ Interview scheduling failed: {response.status_code}")
    
    # Test 5: Job offer
    offer_data = {
        "candidate_id": 1,
        "job_id": 1,
        "salary": 120000,
        "status": "sent"
    }
    
    response = requests.post(f"{base_url}/v1/offers", headers=headers, json=offer_data)
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Job Offer Created: ID {data.get('offer_id')}")
    else:
        print(f"\n✗ Job offer failed: {response.status_code}")
    
    # Test 6: Export comprehensive report
    response = requests.get(f"{base_url}/v1/reports/job/1/export.csv", headers=headers)
    if response.status_code == 200:
        data = response.json()
        csv_data = data.get('csv_data', [])
        print(f"\n✓ Report Export: {len(csv_data)-1} candidate records")
        if len(csv_data) > 1:
            headers_list = csv_data[0]
            print(f"  Enhanced fields: {', '.join(headers_list[4:9])}")  # Values columns
    else:
        print(f"\n✗ Report export failed: {response.status_code}")
    
    # Test 7: Platform statistics
    response = requests.get(f"{base_url}/candidates/stats", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Platform Statistics:")
        print(f"  Candidates: {data.get('total_candidates')}")
        print(f"  Jobs: {data.get('total_jobs')}")
        print(f"  Feedback: {data.get('total_feedback')}")
    else:
        print(f"\n✗ Statistics failed: {response.status_code}")
    
    print(f"\n🎉 Enhanced System Test Complete!")
    print(f"📊 Portal: http://localhost:8501")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"🤖 AI Agent: http://localhost:9000/docs")

if __name__ == "__main__":
    # Upload enhanced candidates
    if upload_all_enhanced_candidates():
        # Test enhanced system
        test_enhanced_system()
    else:
        print("Upload failed, skipping tests")