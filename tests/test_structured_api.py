import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(method, endpoint, data=None, description=""):
    try:
        url = f"{BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=5)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=5)
        
        status = "PASS" if response.status_code in [200, 201] else f"FAIL ({response.status_code})"
        print(f"{status:12} {method:4} {endpoint:35} - {description}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"FAIL        {method:4} {endpoint:35} - {description} (Error: {str(e)[:50]})")
        return False

print("BHIV HR Platform - Structured API Test")
print("=" * 80)

# Core API Endpoints (3)
print("\nCORE API ENDPOINTS")
test_endpoint("GET", "/", description="API Root Information")
test_endpoint("GET", "/health", description="Health Check")
test_endpoint("GET", "/test-candidates", description="Database Connectivity Test")

# Job Management (2)
print("\nJOB MANAGEMENT")
job_data = {
    "title": "Senior Python Developer",
    "department": "Engineering",
    "location": "Remote",
    "experience_level": "Senior",
    "requirements": "Python, FastAPI, PostgreSQL",
    "description": "Senior developer position"
}
test_endpoint("POST", "/v1/jobs", job_data, "Create New Job Posting")
test_endpoint("GET", "/v1/jobs", description="List All Active Jobs")

# Candidate Management (3)
print("\nCANDIDATE MANAGEMENT")
test_endpoint("GET", "/v1/candidates/job/1", description="Get Candidates by Job ID")
test_endpoint("GET", "/v1/candidates/search?skills=python", description="Search & Filter Candidates")
bulk_data = {"candidates": [{"name": "Test User", "email": "test@example.com"}]}
test_endpoint("POST", "/v1/candidates/bulk", bulk_data, "Bulk Upload Candidates")

# AI Matching Engine (1)
print("\nAI MATCHING ENGINE")
test_endpoint("GET", "/v1/match/1/top?limit=5", description="AI Matching Engine")

# Assessment & Workflow (3)
print("\nASSESSMENT & WORKFLOW")
feedback_data = {
    "candidate_id": 1,
    "job_id": 1,
    "integrity": 5,
    "honesty": 5,
    "discipline": 4,
    "hard_work": 5,
    "gratitude": 4,
    "comments": "Excellent candidate"
}
test_endpoint("POST", "/v1/feedback", feedback_data, "Values Assessment")

interview_data = {
    "candidate_id": 1,
    "job_id": 1,
    "interview_date": "2025-01-15T10:00:00Z",
    "interview_type": "technical",
    "notes": "Technical interview scheduled"
}
test_endpoint("POST", "/v1/interviews", interview_data, "Schedule Interview")

offer_data = {
    "candidate_id": 1,
    "job_id": 1,
    "salary": 120000.0,
    "start_date": "2025-02-01",
    "terms": "Full-time position with benefits"
}
test_endpoint("POST", "/v1/offers", offer_data, "Job Offers Management")

# Analytics & Statistics (2)
print("\nANALYTICS & STATISTICS")
test_endpoint("GET", "/candidates/stats", description="Candidate Statistics")
test_endpoint("GET", "/v1/reports/job/1/export.csv", description="Export Job Report")

# Client Portal API (1)
print("\nCLIENT PORTAL API")
client_data = {"client_id": "TECH001", "password": "google123"}
test_endpoint("POST", "/v1/client/login", client_data, "Client Authentication")

# Enterprise Security Endpoints (6)
print("\nENTERPRISE SECURITY ENDPOINTS")

# Two-Factor Authentication (2)
twofa_setup = {"user_id": "test_user"}
test_endpoint("POST", "/v1/2fa/setup", twofa_setup, "2FA Setup")
twofa_login = {"user_id": "test_user", "totp_code": "123456"}
test_endpoint("POST", "/v1/2fa/login-with-2fa", twofa_login, "2FA Login")

# Password Management (2)
password_validate = {"password": "SecurePass123!"}
test_endpoint("POST", "/v1/password/validate", password_validate, "Password Validation")
test_endpoint("POST", "/v1/password/generate?length=16", description="Password Generation")

# Security Testing (1)
security_test = {"test_type": "xss", "payload": "<script>alert('test')</script>"}
test_endpoint("POST", "/v1/security/test", security_test, "Security Testing")

# CSP Management (1)
test_endpoint("GET", "/v1/csp/policy", description="CSP Policy Management")

print("\n" + "=" * 80)
print("STRUCTURED API TEST COMPLETE")
print("Total Endpoints: 19 (15 Original + 4 Enterprise Security)")
print("API Documentation: http://localhost:8000/docs")