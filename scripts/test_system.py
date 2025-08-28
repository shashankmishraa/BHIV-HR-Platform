import requests
import json

def test_system():
    """Test all system endpoints with real enhanced data"""
    
    base_url = "http://localhost:8000"
    headers = {"X-API-KEY": "myverysecureapikey123"}
    
    print("Testing BHIV HR Platform with Enhanced Data")
    print("=" * 50)
    
    # Test 1: Get enhanced candidates
    try:
        response = requests.get(f"{base_url}/v1/candidates/job/1", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Retrieved {data.get('count', 0)} enhanced candidates")
            if data.get('candidates'):
                sample = data['candidates'][0]
                print(f"  Sample: {sample.get('name')}")
                print(f"  Seniority: {sample.get('seniority_level')}")
                print(f"  Skills: {sample.get('technical_skills')}")
                print(f"  Education: {sample.get('education_level')}")
                print(f"  Location: {sample.get('location')}")
        else:
            print(f"FAILED: Get candidates - {response.status_code}")
    except Exception as e:
        print(f"ERROR: Testing candidates - {e}")
    
    # Test 2: AI Matching with enhanced data
    try:
        response = requests.get(f"{base_url}/v1/match/1/top", headers=headers)
        if response.status_code == 200:
            data = response.json()
            top_candidates = data.get('top_candidates', [])
            print(f"\nSUCCESS: AI matching returned {len(top_candidates)} top candidates")
            for i, candidate in enumerate(top_candidates[:3], 1):
                print(f"  #{i}: {candidate.get('name')} (Score: {candidate.get('score')})")
        else:
            print(f"FAILED: AI matching - {response.status_code}")
    except Exception as e:
        print(f"ERROR: Testing AI matching - {e}")
    
    # Test 3: Values feedback
    try:
        feedback_data = {
            "candidate_id": 1,
            "reviewer_name": "HR Manager",
            "feedback_text": "Strong technical background with good cultural fit",
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
            avg_score = data.get('values_summary', {}).get('average_score', 0)
            print(f"\nSUCCESS: Values feedback submitted (Avg: {avg_score}/5)")
        else:
            print(f"FAILED: Values feedback - {response.status_code}")
    except Exception as e:
        print(f"ERROR: Testing values feedback - {e}")
    
    # Test 4: Statistics
    try:
        response = requests.get(f"{base_url}/candidates/stats", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"\nSUCCESS: Platform Statistics")
            print(f"  Total Candidates: {data.get('total_candidates')}")
            print(f"  Total Jobs: {data.get('total_jobs')}")
            print(f"  Total Feedback: {data.get('total_feedback')}")
        else:
            print(f"FAILED: Statistics - {response.status_code}")
    except Exception as e:
        print(f"ERROR: Testing statistics - {e}")
    
    # Test 5: Job creation
    try:
        job_data = {
            "title": "Senior Python Developer",
            "description": "Looking for experienced Python developers with AI/ML background",
            "client_id": 1
        }
        
        response = requests.post(f"{base_url}/v1/jobs", headers=headers, json=job_data)
        if response.status_code == 200:
            data = response.json()
            print(f"\nSUCCESS: Created job ID {data.get('job_id')}")
        else:
            print(f"FAILED: Job creation - {response.status_code}")
    except Exception as e:
        print(f"ERROR: Testing job creation - {e}")
    
    # Test 6: Export report
    try:
        response = requests.get(f"{base_url}/v1/reports/job/1/export.csv", headers=headers)
        if response.status_code == 200:
            data = response.json()
            csv_data = data.get('csv_data', [])
            print(f"\nSUCCESS: Exported report with {len(csv_data)-1} candidate records")
            if len(csv_data) > 1:
                print(f"  Headers: {', '.join(csv_data[0][:5])}...")
        else:
            print(f"FAILED: Report export - {response.status_code}")
    except Exception as e:
        print(f"ERROR: Testing report export - {e}")
    
    print(f"\nSystem test complete!")
    print(f"Access the portal at: http://localhost:8501")
    print(f"API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    test_system()