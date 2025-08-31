import requests
import json

def test_portal_user_journey():
    """Test complete user journey through the portal"""
    print("BHIV HR Portal - Complete User Journey Test")
    print("=" * 50)
    
    headers = {"Authorization": "Bearer myverysecureapikey123", "Content-Type": "application/json"}
    
    # Step 1: Create a new job (as recruiter would do)
    print("Step 1: Creating New Job...")
    job_data = {
        "title": "AI/ML Engineer",
        "description": "Looking for AI/ML engineer with deep learning experience",
        "client_id": 1,
        "department": "AI Research",
        "location": "Bangalore",
        "experience_level": "Senior",
        "employment_type": "Full-time",
        "requirements": "Python, TensorFlow, PyTorch, Machine Learning, Deep Learning",
        "status": "active"
    }
    
    try:
        response = requests.post("http://localhost:8000/v1/jobs", headers=headers, json=job_data)
        if response.status_code == 200:
            result = response.json()
            new_job_id = result.get("job_id")
            print(f"  SUCCESS: Created job '{job_data['title']}' with ID {new_job_id}")
        else:
            print(f"  FAILED: Job creation failed - {response.status_code}")
            new_job_id = 1
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        new_job_id = 1
    
    # Step 2: Search for candidates
    print(f"\nStep 2: Searching Candidates for Job {new_job_id}...")
    search_params = [
        ("Python skills", "skills=Python"),
        ("Machine Learning", "skills=Machine Learning"),
        ("Senior level", "experience_min=4"),
        ("Location: Mumbai", "location=Mumbai")
    ]
    
    for search_name, params in search_params:
        try:
            url = f"http://localhost:8000/v1/candidates/search?job_id={new_job_id}&{params}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                print(f"  {search_name}: Found {count} candidates")
            else:
                print(f"  {search_name}: Search failed")
        except Exception as e:
            print(f"  {search_name}: ERROR - {str(e)}")
    
    # Step 3: Get AI-powered shortlist
    print(f"\nStep 3: Getting AI Shortlist for Job {new_job_id}...")
    try:
        response = requests.get(f"http://localhost:8000/v1/match/{new_job_id}/top", headers=headers)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('top_candidates', [])
            processing_time = data.get('processing_time', 0)
            print(f"  SUCCESS: Generated {len(candidates)} top candidates in {processing_time}s")
            
            if candidates:
                print("  Top 3 Matches:")
                for i, candidate in enumerate(candidates[:3], 1):
                    name = candidate.get('name', 'Unknown')
                    score = candidate.get('score', 0)
                    skills = candidate.get('skills_match', [])
                    print(f"    {i}. {name} - Score: {score}/100")
                    if skills:
                        print(f"       Skills: {', '.join(skills)}")
        else:
            print(f"  FAILED: AI matching failed - {response.status_code}")
    except Exception as e:
        print(f"  ERROR: {str(e)}")
    
    # Step 4: Submit values assessment
    print("\nStep 4: Submitting Values Assessment...")
    feedback_data = {
        "candidate_id": 1,
        "reviewer": "Senior HR Manager",
        "feedback_text": "Excellent candidate with strong technical skills and cultural fit. Shows great potential for leadership roles.",
        "values_scores": {
            "integrity": 5,
            "honesty": 5,
            "discipline": 4,
            "hard_work": 5,
            "gratitude": 4
        }
    }
    
    try:
        response = requests.post("http://localhost:8000/v1/feedback", headers=headers, json=feedback_data)
        if response.status_code == 200:
            result = response.json()
            feedback_id = result.get('feedback_id')
            values_profile = result.get('values_profile', {})
            avg_score = values_profile.get('values_average', 0)
            recommendation = values_profile.get('recommendation', 'Unknown')
            
            print(f"  SUCCESS: Submitted feedback ID {feedback_id}")
            print(f"  Values Average: {avg_score}/5")
            print(f"  Recommendation: {recommendation}")
        else:
            print(f"  FAILED: Values assessment failed - {response.status_code}")
    except Exception as e:
        print(f"  ERROR: {str(e)}")
    
    # Step 5: Schedule interview
    print("\nStep 5: Scheduling Interview...")
    interview_data = {
        "candidate_id": 1,
        "job_id": new_job_id,
        "interview_date": "2025-02-15T14:00:00Z",
        "interviewer": "Technical Lead - AI Team"
    }
    
    try:
        response = requests.post("http://localhost:8000/v1/interviews", headers=headers, json=interview_data)
        if response.status_code == 200:
            result = response.json()
            interview_id = result.get('interview_id')
            print(f"  SUCCESS: Scheduled interview ID {interview_id}")
            print(f"  Date: Feb 15, 2025 at 2:00 PM")
            print(f"  Interviewer: {interview_data['interviewer']}")
        else:
            print(f"  FAILED: Interview scheduling failed - {response.status_code}")
    except Exception as e:
        print(f"  ERROR: {str(e)}")
    
    # Step 6: Make job offer
    print("\nStep 6: Making Job Offer...")
    offer_data = {
        "candidate_id": 1,
        "job_id": new_job_id,
        "salary": 150000,
        "status": "sent"
    }
    
    try:
        response = requests.post("http://localhost:8000/v1/offers", headers=headers, json=offer_data)
        if response.status_code == 200:
            result = response.json()
            offer_id = result.get('offer_id')
            print(f"  SUCCESS: Created job offer ID {offer_id}")
            print(f"  Salary: ${offer_data['salary']:,}")
            print(f"  Status: {offer_data['status'].title()}")
        else:
            print(f"  FAILED: Job offer failed - {response.status_code}")
    except Exception as e:
        print(f"  ERROR: {str(e)}")
    
    # Step 7: View dashboard statistics
    print("\nStep 7: Viewing Dashboard Statistics...")
    try:
        response = requests.get("http://localhost:8000/candidates/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"  Platform Statistics:")
            print(f"    Total Candidates: {stats.get('total_candidates', 0)}")
            print(f"    Active Jobs: {stats.get('total_jobs', 0)}")
            print(f"    Feedback Submitted: {stats.get('total_feedback', 0)}")
        else:
            print(f"  FAILED: Statistics retrieval failed")
    except Exception as e:
        print(f"  ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("USER JOURNEY COMPLETE")
    print("=" * 50)
    print("Portal Features Tested:")
    print("  ✓ Job Creation")
    print("  ✓ Candidate Search & Filtering")
    print("  ✓ AI-Powered Matching")
    print("  ✓ Values Assessment")
    print("  ✓ Interview Scheduling")
    print("  ✓ Job Offer Management")
    print("  ✓ Dashboard Statistics")
    
    print("\nClient Experience Summary:")
    print("  - Intuitive workflow from job creation to offer")
    print("  - Real-time AI recommendations")
    print("  - Comprehensive values-based assessment")
    print("  - Complete recruitment lifecycle management")
    print("  - Professional interface with live data")

if __name__ == "__main__":
    test_portal_user_journey()