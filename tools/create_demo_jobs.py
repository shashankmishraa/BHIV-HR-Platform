import requests
import json

API_BASE = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

jobs = [
    {
        "title": "Data Scientist",
        "description": "Looking for experienced Data Scientist with ML/AI expertise",
        "client_id": 1,
        "department": "Data Science",
        "location": "Remote",
        "experience_level": "Mid",
        "employment_type": "Full-time",
        "requirements": "Python, Machine Learning, Pandas, NumPy, Scikit-learn",
        "status": "active"
    },
    {
        "title": "Full Stack Developer",
        "description": "Full stack developer with React and Node.js experience",
        "client_id": 1,
        "department": "Engineering",
        "location": "Mumbai",
        "experience_level": "Senior",
        "employment_type": "Full-time",
        "requirements": "JavaScript, React, Node.js, MongoDB, Git",
        "status": "active"
    }
]

print("Creating demo jobs...")
for i, job in enumerate(jobs, 1):
    try:
        response = requests.post(f"{API_BASE}/v1/jobs", headers=HEADERS, json=job, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"Job {i}: Created '{job['title']}' - ID {result.get('job_id')}")
        else:
            print(f"Job {i}: Failed - {response.status_code}")
    except Exception as e:
        print(f"Job {i}: Error - {str(e)}")

print("\nDone! Platform now has multiple job types for better testing.")