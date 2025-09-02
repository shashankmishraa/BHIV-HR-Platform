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
        print(f"{status:12} {method:4} {endpoint:45} - {description}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"FAIL        {method:4} {endpoint:45} - {description} (Error: {str(e)[:30]})")
        return False

print("BHIV HR Platform - Complete Enterprise API Test")
print("=" * 90)

# Core API Endpoints (3)
print("\nCore API Endpoints")
test_endpoint("GET", "/", description="API Root Information")
test_endpoint("GET", "/health", description="Health Check")
test_endpoint("GET", "/test-candidates", description="Database Connectivity Test")

# Job Management (2)
print("\nJob Management")
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
print("\nCandidate Management")
test_endpoint("GET", "/v1/candidates/job/1", description="Get All Candidates (Dynamic Matching)")
test_endpoint("GET", "/v1/candidates/search?skills=python", description="Search & Filter Candidates")
bulk_data = {"candidates": [{"name": "Test User", "email": "test@example.com"}]}
test_endpoint("POST", "/v1/candidates/bulk", bulk_data, "Bulk Upload Candidates")

# AI Matching Engine (1)
print("\nAI Matching Engine")
test_endpoint("GET", "/v1/match/1/top?limit=5", description="Semantic candidate matching and ranking")

# Assessment & Workflow (3)
print("\nAssessment & Workflow")
feedback_data = {
    "candidate_id": 1, "job_id": 1, "integrity": 5, "honesty": 5,
    "discipline": 4, "hard_work": 5, "gratitude": 4, "comments": "Excellent"
}
test_endpoint("POST", "/v1/feedback", feedback_data, "Values Assessment")

interview_data = {
    "candidate_id": 1, "job_id": 1, "interview_date": "2025-01-15T10:00:00Z",
    "interview_type": "technical", "notes": "Technical interview"
}
test_endpoint("POST", "/v1/interviews", interview_data, "Schedule Interview")

offer_data = {
    "candidate_id": 1, "job_id": 1, "salary": 120000.0,
    "start_date": "2025-02-01", "terms": "Full-time with benefits"
}
test_endpoint("POST", "/v1/offers", offer_data, "Job Offers Management")

# Analytics & Statistics (2)
print("\nAnalytics & Statistics")
test_endpoint("GET", "/candidates/stats", description="Candidate Statistics")
test_endpoint("GET", "/v1/reports/job/1/export.csv", description="Export Job Report")

# Client Portal API (1)
print("\nClient Portal API")
client_data = {"client_id": "TECH001", "password": "google123"}
test_endpoint("POST", "/v1/client/login", client_data, "Client Authentication")

# Security Testing (7 endpoints)
print("\nSecurity Testing")
test_endpoint("GET", "/v1/security/rate-limit-status", description="Check Rate Limit Status")
test_endpoint("GET", "/v1/security/blocked-ips", description="View Blocked IPs")

input_test = {"input_data": "<script>alert('test')</script>"}
test_endpoint("POST", "/v1/security/test-input-validation", input_test, "Test Input Validation")

email_test = {"email": "test@example.com"}
test_endpoint("POST", "/v1/security/test-email-validation", email_test, "Test Email Validation")

phone_test = {"phone": "+1-555-123-4567"}
test_endpoint("POST", "/v1/security/test-phone-validation", phone_test, "Test Phone Validation")

test_endpoint("GET", "/v1/security/security-headers-test", description="Test Security Headers")
test_endpoint("GET", "/v1/security/penetration-test-endpoints", description="Penetration Testing Endpoints")

# CSP Management (4 endpoints)
print("\nCSP Management")
csp_report = {
    "violated_directive": "script-src",
    "blocked_uri": "https://malicious.com/script.js",
    "document_uri": "https://bhiv-platform.com/dashboard"
}
test_endpoint("POST", "/v1/security/csp-report", csp_report, "CSP Violation Reporting")
test_endpoint("GET", "/v1/security/csp-violations", description="View CSP Violations")
test_endpoint("GET", "/v1/security/csp-policies", description="Current CSP Policies")

csp_policy = {"policy": "default-src 'self'; script-src 'self'"}
test_endpoint("POST", "/v1/security/test-csp-policy", csp_policy, "Test CSP Policy")

# Two-Factor Authentication (8 endpoints)
print("\nTwo-Factor Authentication")
twofa_setup = {"user_id": "test_user"}
test_endpoint("POST", "/v1/2fa/setup", twofa_setup, "Setup 2FA for Client")

twofa_verify = {"user_id": "test_user", "totp_code": "123456"}
test_endpoint("POST", "/v1/2fa/verify-setup", twofa_verify, "Verify 2FA Setup")

twofa_login = {"user_id": "test_user", "totp_code": "123456"}
test_endpoint("POST", "/v1/2fa/login-with-2fa", twofa_login, "Login with 2FA")

test_endpoint("GET", "/v1/2fa/status/TECH001", description="Get 2FA Status")
test_endpoint("POST", "/v1/2fa/disable", twofa_setup, "Disable 2FA")
test_endpoint("POST", "/v1/2fa/regenerate-backup-codes", twofa_setup, "Regenerate Backup Codes")
test_endpoint("GET", "/v1/2fa/test-token/TECH001/123456", description="Test 2FA Token")
test_endpoint("GET", "/v1/2fa/demo-setup", description="Demo 2FA Setup")

# Password Management (6 endpoints)
print("\nPassword Management")
password_validate = {"password": "SecurePass123!"}
test_endpoint("POST", "/v1/password/validate", password_validate, "Validate Password Strength")
test_endpoint("POST", "/v1/password/generate?length=16", description="Generate Secure Password")
test_endpoint("GET", "/v1/password/policy", description="Get Password Policy")

password_change = {"old_password": "oldpass123", "new_password": "NewSecure123!"}
test_endpoint("POST", "/v1/password/change", password_change, "Change Password")
test_endpoint("GET", "/v1/password/strength-test", description="Password Strength Testing Tool")
test_endpoint("GET", "/v1/password/security-tips", description="Password Security Best Practices")

print("\n" + "=" * 90)
print("COMPLETE ENTERPRISE API TEST FINISHED")
print("Total Endpoints: 40+ (15 Original + 25+ Enterprise Security)")
print("API Documentation: http://localhost:8000/docs")