import requests
import json

def test_upload():
    # Test data
    candidate = {
        "name": "Test Candidate",
        "email": "test@example.com",
        "phone": "+1-555-1234",
        "location": "Mumbai",
        "cv_url": "https://example.com/test.pdf",
        "experience_years": 5,
        "education_level": "Masters",
        "technical_skills": "Python, Java, SQL",
        "seniority_level": "Mid-level",
        "status": "applied",
        "job_id": 1
    }
    
    print("Testing candidate upload with enhanced fields:")
    print(f"Name: {candidate['name']}")
    print(f"Skills: {candidate['technical_skills']}")
    print(f"Seniority: {candidate['seniority_level']}")
    print(f"Education: {candidate['education_level']}")
    
    # Upload
    response = requests.post(
        "http://localhost:8000/v1/candidates/bulk",
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": "myverysecureapikey123"
        },
        json={"candidates": [candidate]}
    )
    
    print(f"\nUpload response: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS!")
        print(response.json())
    else:
        print("FAILED!")
        print(response.text)
    
    # Retrieve and check
    response = requests.get(
        "http://localhost:8000/v1/candidates/job/1",
        headers={"X-API-KEY": "myverysecureapikey123"}
    )
    
    if response.status_code == 200:
        data = response.json()
        candidates = data.get('candidates', [])
        if candidates:
            latest = candidates[0]  # Most recent
            print(f"\nRetrieved candidate:")
            print(f"Name: {latest.get('name')}")
            print(f"Skills: {latest.get('technical_skills')}")
            print(f"Seniority: {latest.get('seniority_level')}")
            print(f"Education: {latest.get('education_level')}")
            print(f"Location: {latest.get('location')}")
        else:
            print("No candidates found")
    else:
        print(f"Failed to retrieve: {response.status_code}")

if __name__ == "__main__":
    test_upload()