# 🧪 BHIV HR Platform - API Testing Guide

**Complete testing guide for 62 endpoints (56 Gateway + 6 Agent)**

## 🔑 Authentication Requirements

### **API Key (Required for all endpoints)**
```bash
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### **Base URLs**
- **Production Gateway**: `https://bhiv-hr-gateway-46pz.onrender.com`
- **Production Agent**: `https://bhiv-hr-agent-m1me.onrender.com`
- **Local Gateway**: `http://localhost:8000`
- **Local Agent**: `http://localhost:9000`

---

## 🌐 Gateway Service (55 Endpoints)

### **Core API (3 endpoints)**

#### 1. Root Endpoint
```bash
GET /
# No authentication required
curl https://bhiv-hr-gateway-46pz.onrender.com/
```

#### 2. Health Check
```bash
GET /health
# No authentication required
curl https://bhiv-hr-gateway-46pz.onrender.com/health
```

#### 3. Test Candidates
```bash
GET /test-candidates
# No authentication required
curl https://bhiv-hr-gateway-46pz.onrender.com/test-candidates
```

### **Monitoring (3 endpoints)**

#### 4. Metrics
```bash
GET /metrics
# No authentication required
curl https://bhiv-hr-gateway-46pz.onrender.com/metrics
```

#### 5. Detailed Health
```bash
GET /health/detailed
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health/detailed
```

#### 6. Metrics Dashboard
```bash
GET /metrics/dashboard
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/metrics/dashboard
```

### **Analytics (3 endpoints)**

#### 7. Candidate Statistics
```bash
GET /candidates/stats
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/candidates/stats
```

#### 8. Database Schema
```bash
GET /v1/database/schema
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/database/schema
```

#### 9. Job Report Export
```bash
GET /v1/reports/job/{job_id}/export.csv
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/reports/job/1/export.csv
```

### **Job Management (2 endpoints)**

#### 10. Get Jobs
```bash
GET /v1/jobs
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

#### 11. Create Job
```bash
POST /v1/jobs
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Senior Software Engineer",
       "description": "We are looking for a senior software engineer with 5+ years of experience in Python and FastAPI.",
       "requirements": "Python, FastAPI, PostgreSQL, Docker",
       "location": "San Francisco, CA",
       "salary_range": "$120,000 - $150,000",
       "company": "Tech Innovations Inc",
       "job_type": "Full-time",
       "experience_level": "Senior"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

### **Candidate Management (5 endpoints)**

#### 12. Get Candidates
```bash
GET /v1/candidates
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates
```

#### 13. Get Candidate by ID
```bash
GET /v1/candidates/{id}
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/1
```

#### 14. Search Candidates
```bash
GET /v1/candidates/search?q=python&location=san francisco
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?q=python&location=san francisco"
```

#### 15. Bulk Upload Candidates
```bash
POST /v1/candidates/bulk
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidates": [
         {
           "name": "John Doe",
           "email": "john.doe@example.com",
           "phone": "+1-555-0123",
           "skills": "Python, FastAPI, PostgreSQL",
           "experience": "5 years",
           "location": "San Francisco, CA"
         }
       ]
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/bulk
```

#### 16. Get Candidates for Job
```bash
GET /v1/candidates/job/{job_id}
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/job/1
```

### **AI Matching (2 endpoints)**

#### 17. Get Top Matches
```bash
GET /v1/match/{job_id}/top
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top
```

#### 18. Batch Matching
```bash
POST /v1/match/batch
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "job_ids": [1, 2, 3],
       "limit": 10
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/batch
```

### **Assessment (5 endpoints)**

#### 19. Get Feedback
```bash
GET /v1/feedback
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```

#### 20. Create Feedback
```bash
POST /v1/feedback
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "integrity": 5,
       "honesty": 4,
       "discipline": 5,
       "hard_work": 4,
       "gratitude": 5,
       "comments": "Excellent candidate with strong values alignment"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```

#### 21. Get Interviews
```bash
GET /v1/interviews
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/interviews
```

#### 22. Schedule Interview
```bash
POST /v1/interviews
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "interview_date": "2025-01-15T10:00:00",
       "interview_type": "Technical",
       "interviewer": "Jane Smith",
       "location": "Conference Room A"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/interviews
```

#### 23. Get Offers
```bash
GET /v1/offers
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/offers
```

### **Security Testing (7 endpoints)**

#### 24. Rate Limit Status
```bash
GET /v1/security/rate-limit-status
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/rate-limit-status
```

#### 25. Input Validation Test
```bash
POST /v1/security/test-input-validation
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "test_input": "<script>alert('xss')</script>",
       "sql_injection": "1; DROP TABLE users; --"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/test-input-validation
```

#### 26. Email Validation
```bash
POST /v1/security/validate-email
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/validate-email
```

#### 27. Phone Validation
```bash
POST /v1/security/validate-phone
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"phone": "+1-555-0123"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/validate-phone
```

#### 28. Security Headers Test
```bash
GET /v1/security/test-headers
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/test-headers
```

#### 29. Penetration Test
```bash
POST /v1/security/penetration-test
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"test_type": "basic"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/penetration-test
```

#### 30. Test Authentication
```bash
GET /v1/security/test-auth
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/test-auth
```

### **CSP Management (4 endpoints)**

#### 31. CSP Policies
```bash
GET /v1/csp/policies
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/csp/policies
```

#### 32. CSP Violations
```bash
GET /v1/csp/violations
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/csp/violations
```

#### 33. CSP Report
```bash
POST /v1/csp/report
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "csp-report": {
         "document-uri": "https://example.com",
         "violated-directive": "script-src",
         "blocked-uri": "https://malicious.com/script.js"
       }
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/csp/report
```

#### 34. CSP Test
```bash
GET /v1/csp/test
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/csp/test
```

### **2FA Authentication (8 endpoints)**

#### 35. Setup 2FA
```bash
POST /v1/auth/2fa/setup
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/setup
```

#### 36. Verify 2FA
```bash
POST /v1/auth/2fa/verify
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 1,
       "token": "123456"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/verify
```

#### 37. 2FA Login
```bash
POST /v1/auth/2fa/login
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "password123",
       "token": "123456"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/login
```

#### 38. 2FA Status
```bash
GET /v1/auth/2fa/status/{user_id}
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/status/1
```

#### 39. Disable 2FA
```bash
POST /v1/auth/2fa/disable
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/disable
```

#### 40. Generate Backup Codes
```bash
POST /v1/auth/2fa/backup-codes
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/backup-codes
```

#### 41. Test Token
```bash
POST /v1/auth/2fa/test-token
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "secret": "JBSWY3DPEHPK3PXP",
       "token": "123456"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/test-token
```

#### 42. QR Code
```bash
GET /v1/auth/2fa/qr/{user_id}
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/2fa/qr/1
```

### **Password Management (6 endpoints)**

#### 43. Validate Password
```bash
POST /v1/auth/password/validate
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"password": "SecurePass123!"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/password/validate
```

#### 44. Generate Password
```bash
GET /v1/auth/password/generate?length=12&include_symbols=true
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/password/generate?length=12&include_symbols=true"
```

#### 45. Password Policy
```bash
GET /v1/auth/password/policy
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/password/policy
```

#### 46. Change Password
```bash
POST /v1/auth/password/change
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 1,
       "current_password": "oldpass123",
       "new_password": "NewSecurePass123!"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/password/change
```

#### 47. Password Strength Test
```bash
POST /v1/auth/password/strength
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"password": "TestPassword123!"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/password/strength
```

#### 48. Security Tips
```bash
GET /v1/auth/password/security-tips
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/auth/password/security-tips
```

### **Client Portal (2 endpoints)**

#### 49. Client Register
```bash
POST /v1/client/register
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "client_id": "NEWCLIENT01",
       "company_name": "New Tech Company",
       "contact_email": "admin@newtech.com",
       "password": "SecurePass123!"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/client/register
```

#### 50. Client Login
```bash
POST /v1/client/login
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "TECH001",
       "password": "demo123"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login
```

### **Candidate Portal (5 endpoints)**

#### 51. Candidate Register
```bash
POST /v1/candidate/register
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith",
       "email": "jane.smith@example.com",
       "phone": "+1-555-0124",
       "password": "SecurePass123!",
       "skills": "React, Node.js, MongoDB",
       "experience": "3 years",
       "location": "New York, NY"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/register
```

#### 52. Candidate Login
```bash
POST /v1/candidate/login
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "jane.smith@example.com",
       "password": "SecurePass123!"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/login
```

#### 53. Update Candidate Profile
```bash
PUT /v1/candidate/profile/{id}
curl -X PUT \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith Updated",
       "skills": "React, Node.js, MongoDB, Python",
       "experience": "4 years",
       "location": "San Francisco, CA"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/profile/1
```

#### 54. Apply for Job
```bash
POST /v1/candidate/apply
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "cover_letter": "I am very interested in this position and believe my skills align well with your requirements."
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/apply
```

#### 55. Get Candidate Applications
```bash
GET /v1/candidate/applications/{id}
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/applications/1
```

### **Additional Endpoint (1)**

#### 56. Create Job Offer
```bash
POST /v1/offers
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "salary": 125000,
       "start_date": "2025-02-01",
       "benefits": "Health insurance, 401k, PTO",
       "offer_status": "pending"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/offers
```

---

## 🤖 Agent Service (6 Endpoints)

### **Core (2 endpoints)**

#### 57. Agent Root
```bash
GET /
# No authentication required
curl https://bhiv-hr-agent-m1me.onrender.com/
```

#### 58. Agent Health
```bash
GET /health
# No authentication required
curl https://bhiv-hr-agent-m1me.onrender.com/health
```

### **AI Processing (3 endpoints)**

#### 59. AI Match
```bash
POST /match
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "job_id": 1,
       "limit": 10,
       "company_id": "TECH001"
     }' \
     https://bhiv-hr-agent-m1me.onrender.com/match
```

#### 60. Batch Match
```bash
POST /batch-match
curl -X POST \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "job_ids": [1, 2, 3],
       "limit": 5,
       "company_id": "TECH001"
     }' \
     https://bhiv-hr-agent-m1me.onrender.com/batch-match
```

#### 61. Analyze Candidate
```bash
GET /analyze/{candidate_id}
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-agent-m1me.onrender.com/analyze/1
```

### **Diagnostics (1 endpoint)**

#### 62. Test Database
```bash
GET /test-db
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-agent-m1me.onrender.com/test-db
```

---

## 🧪 Quick Test Script

### **Basic Health Check**
```bash
#!/bin/bash
echo "Testing BHIV HR Platform APIs..."

# Gateway Health
echo "1. Gateway Health:"
curl -s https://bhiv-hr-gateway-46pz.onrender.com/health | jq

# Agent Health
echo "2. Agent Health:"
curl -s https://bhiv-hr-agent-m1me.onrender.com/health | jq

# Get Jobs
echo "3. Jobs List:"
curl -s -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs | jq

# Get Candidates
echo "4. Candidates List:"
curl -s -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates | jq

# AI Matching
echo "5. AI Matching:"
curl -s -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top | jq

echo "All tests completed!"
```

---

## 📊 Expected Response Formats

### **Success Response**
```json
{
  "status": "success",
  "data": {...},
  "message": "Operation completed successfully"
}
```

### **Error Response**
```json
{
  "status": "error",
  "error": "Error description",
  "details": "Additional error details"
}
```

### **Authentication Error**
```json
{
  "detail": "Invalid API key"
}
```

---

## 🔧 Testing Tools

### **Postman Collection**
Import the following environment variables:
- `base_url_gateway`: `https://bhiv-hr-gateway-46pz.onrender.com`
- `base_url_agent`: `https://bhiv-hr-agent-m1me.onrender.com`
- `api_key`: `prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o`

### **Python Testing Script**
```python
import requests

BASE_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

headers = {"Authorization": f"Bearer {API_KEY}"}

# Test health endpoint
response = requests.get(f"{BASE_URL}/health")
print(f"Health: {response.json()}")

# Test jobs endpoint
response = requests.get(f"{BASE_URL}/v1/jobs", headers=headers)
print(f"Jobs: {response.json()}")
```

---

**Total Endpoints Tested**: 62 (56 Gateway + 6 Agent)
**Authentication**: Bearer Token Required
**Production Status**: ✅ All Services Operational
**Last Updated**: October 23, 2025