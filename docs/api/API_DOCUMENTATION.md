# 📚 BHIV HR Platform - Complete API Documentation

**Generated**: January 2025  
**API Version**: v3.1.0  
**Total Endpoints**: 61 (55 Gateway + 6 Agent)  
**Status**: ✅ All Endpoints Operational

---

## 🌐 API Overview

### **Base URLs**
- **Production Gateway**: https://bhiv-hr-gateway-46pz.onrender.com
- **Production Agent**: https://bhiv-hr-agent-m1me.onrender.com
- **Local Gateway**: http://localhost:8000
- **Local Agent**: http://localhost:9000

### **Authentication**
```bash
# API Key Authentication (Primary)
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# Client JWT Authentication
Authorization: Bearer <client_jwt_token>

# Candidate JWT Authentication  
Authorization: Bearer <candidate_jwt_token>
```

### **Response Format**
All API responses follow a consistent JSON format:
```json
{
  "status": "success|error",
  "data": {...},
  "message": "Human readable message",
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

---

## 🚀 Gateway Service API (55 Endpoints)

### **Core API Endpoints (3)**

#### **GET /** - Service Information
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/
```
**Response:**
```json
{
  "message": "BHIV HR Platform API Gateway",
  "version": "3.1.0",
  "status": "healthy",
  "endpoints": 55,
  "documentation": "/docs",
  "monitoring": "/metrics",
  "live_demo": "https://bhiv-platform.aws.example.com"
}
```

#### **GET /health** - Health Check
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "BHIV HR Gateway",
  "version": "3.1.0",
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

#### **GET /test-candidates** - Database Connectivity Test
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates
```
**Response:**
```json
{
  "database_status": "connected",
  "total_candidates": 31,
  "test_timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

---

### **Monitoring Endpoints (3)**

#### **GET /metrics** - Prometheus Metrics
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/metrics
```
**Response:** Prometheus format metrics

#### **GET /health/detailed** - Detailed Health Check
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health/detailed
```
**Response:**
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "ai_engine": "operational",
    "authentication": "active"
  },
  "performance": {
    "response_time": "45ms",
    "memory_usage": "312MB",
    "cpu_usage": "23%"
  }
}
```

#### **GET /metrics/dashboard** - Metrics Dashboard
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/metrics/dashboard
```

---

### **Analytics Endpoints (3)**

#### **GET /candidates/stats** - Candidate Statistics
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/candidates/stats
```
**Response:**
```json
{
  "total_candidates": 31,
  "active_jobs": 19,
  "recent_matches": 25,
  "pending_interviews": 8,
  "statistics_generated_at": "2025-01-XX T XX:XX:XX Z"
}
```

#### **GET /v1/database/schema** - Database Schema Verification
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/database/schema
```
**Response:**
```json
{
  "schema_version": "4.1.0",
  "total_tables": 17,
  "tables": ["candidates", "jobs", "feedback", "interviews", "offers", "users", "clients", "audit_logs", "rate_limits", "csp_violations", "matching_cache", "company_scoring_preferences", "client_auth", "client_sessions", "schema_version", "pg_stat_statements", "pg_stat_statements_info"],
  "phase3_enabled": true,
  "checked_at": "2025-01-XX T XX:XX:XX Z"
}
```

#### **GET /v1/reports/job/{job_id}/export.csv** - Job Report Export
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/reports/job/1/export.csv
```

---

### **Job Management Endpoints (2)**

#### **GET /v1/jobs** - List All Jobs
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```
**Response:**
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "department": "Engineering",
      "location": "Remote",
      "experience_level": "Senior",
      "requirements": "Python, Django, PostgreSQL, REST APIs, 5+ years experience",
      "description": "We are looking for a senior Python developer...",
      "created_at": "2025-01-XX T XX:XX:XX Z"
    }
  ],
  "count": 19
}
```

#### **POST /v1/jobs** - Create New Job
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Software Engineer",
       "department": "Engineering",
       "location": "San Francisco",
       "experience_level": "Mid",
       "requirements": "Python, React, 3+ years",
       "description": "Join our engineering team..."
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```
**Response:**
```json
{
  "message": "Job created successfully",
  "job_id": 20,
  "created_at": "2025-01-XX T XX:XX:XX Z"
}
```

---

### **Candidate Management Endpoints (5)**

#### **GET /v1/candidates** - List Candidates with Pagination
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates?limit=10&offset=0"
```
**Response:**
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1-555-0101",
      "location": "Mumbai",
      "experience_years": 5,
      "technical_skills": "Python, Django, PostgreSQL",
      "seniority_level": "Software Developer",
      "education_level": "Masters",
      "created_at": "2025-01-XX T XX:XX:XX Z"
    }
  ],
  "total": 31,
  "limit": 10,
  "offset": 0,
  "count": 10
}
```

#### **GET /v1/candidates/{id}** - Get Specific Candidate
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/1
```
**Response:**
```json
{
  "candidate": {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1-555-0101",
    "location": "Mumbai",
    "experience_years": 5,
    "technical_skills": "Python, Django, PostgreSQL, REST APIs",
    "seniority_level": "Software Developer",
    "education_level": "Masters",
    "resume_path": "/resumes/john_smith.pdf",
    "created_at": "2025-01-XX T XX:XX:XX Z",
    "updated_at": "2025-01-XX T XX:XX:XX Z"
  }
}
```

#### **GET /v1/candidates/search** - Advanced Search with Filters
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?skills=Python&location=Mumbai&experience_min=3"
```
**Response:**
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1-555-0101",
      "location": "Mumbai",
      "technical_skills": "Python, Django, PostgreSQL",
      "experience_years": 5,
      "seniority_level": "Software Developer",
      "education_level": "Masters",
      "status": "applied"
    }
  ],
  "filters": {
    "skills": "Python",
    "location": "Mumbai",
    "experience_min": 3
  },
  "count": 15
}
```

#### **POST /v1/candidates/bulk** - Bulk Upload with Validation
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidates": [
         {
           "name": "Jane Doe",
           "email": "jane@example.com",
           "phone": "+1-555-0102",
           "experience_years": 3,
           "technical_skills": "React, JavaScript, Node.js",
           "location": "San Francisco"
         }
       ]
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/bulk
```
**Response:**
```json
{
  "message": "Bulk upload completed",
  "candidates_received": 1,
  "candidates_inserted": 1,
  "errors": [],
  "total_errors": 0,
  "status": "success"
}
```

#### **GET /v1/candidates/job/{job_id}** - Candidates by Job
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/job/1
```

---

### **AI Matching Endpoints (2)**

#### **GET /v1/match/{job_id}/top** - AI-Powered Semantic Matching
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top?limit=5
```
**Response:**
```json
{
  "matches": [
    {
      "candidate_id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "score": 92.5,
      "skills_match": "Python, Django, PostgreSQL",
      "experience_match": "5y - Phase 3 matched",
      "location_match": true,
      "reasoning": "Semantic match: 0.85; Skills: Python, Django; Experience: 5y; Location: Mumbai",
      "recommendation_strength": "Strong Match"
    }
  ],
  "job_id": 1,
  "limit": 5,
  "total_candidates": 31,
  "algorithm_version": "3.0.0-phase3-production",
  "processing_time": "0.015s",
  "ai_analysis": "Real AI semantic matching via Agent Service",
  "agent_status": "connected"
}
```

#### **POST /v1/match/batch** - Batch Matching for Multiple Jobs
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"job_ids": [1, 2, 3]}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/batch
```
**Response:**
```json
{
  "batch_results": {
    "1": {
      "job_id": 1,
      "matches": [
        {
          "candidate_id": 1,
          "name": "John Smith",
          "score": 92.5,
          "reasoning": "Batch AI matching - Job 1"
        }
      ],
      "algorithm": "batch-production"
    }
  },
  "total_jobs_processed": 3,
  "total_candidates_analyzed": 31,
  "algorithm_version": "3.0.0-phase3-production-batch",
  "status": "success"
}
```

---

### **Assessment Workflow Endpoints (6)**

#### **POST /v1/feedback** - Values Assessment (5-Point BHIV Values)
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "integrity": 5,
       "honesty": 4,
       "discipline": 4,
       "hard_work": 5,
       "gratitude": 4,
       "comments": "Excellent candidate with strong values alignment"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```
**Response:**
```json
{
  "message": "Feedback submitted successfully",
  "feedback_id": 1,
  "candidate_id": 1,
  "job_id": 1,
  "values_scores": {
    "integrity": 5,
    "honesty": 4,
    "discipline": 4,
    "hard_work": 5,
    "gratitude": 4
  },
  "average_score": 4.4,
  "submitted_at": "2025-01-XX T XX:XX:XX Z"
}
```

#### **GET /v1/feedback** - Get All Feedback Records
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```

#### **POST /v1/interviews** - Schedule Interview
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "interview_date": "2025-02-01 10:00:00",
       "interviewer": "John Manager",
       "notes": "Technical interview scheduled"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/interviews
```
**Response:**
```json
{
  "message": "Interview scheduled successfully",
  "interview_id": 1,
  "candidate_id": 1,
  "job_id": 1,
  "interview_date": "2025-02-01 10:00:00",
  "status": "scheduled"
}
```

#### **GET /v1/interviews** - Get All Interviews
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/interviews
```

#### **POST /v1/offers** - Job Offers Management
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "salary": 120000.00,
       "start_date": "2025-03-01",
       "terms": "Full-time position with benefits"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/offers
```

#### **GET /v1/offers** - Get All Job Offers
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/offers
```

---

### **Security Testing Endpoints (7)**

#### **GET /v1/security/rate-limit-status** - Check Rate Limit Status
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/rate-limit-status
```
**Response:**
```json
{
  "rate_limit_enabled": true,
  "requests_per_minute": 60,
  "current_requests": 15,
  "remaining_requests": 45,
  "reset_time": "2025-01-XX T XX:XX:XX Z",
  "status": "active"
}
```

#### **POST /v1/security/test-input-validation** - Test Input Validation
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"input_data": "<script>alert(\"test\")</script>"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/test-input-validation
```
**Response:**
```json
{
  "input": "<script>alert(\"test\")</script>",
  "validation_result": "BLOCKED",
  "threats_detected": ["XSS attempt detected"],
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

#### **POST /v1/security/test-email-validation** - Test Email Validation
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/test-email-validation
```

#### **POST /v1/security/test-phone-validation** - Test Phone Validation
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"phone": "+1-555-123-4567"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/test-phone-validation
```

#### **GET /v1/security/security-headers-test** - Test Security Headers
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/security-headers-test
```

#### **GET /v1/security/blocked-ips** - View Blocked IPs
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/blocked-ips
```

#### **GET /v1/security/penetration-test-endpoints** - Penetration Testing Endpoints
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/penetration-test-endpoints
```

---

### **2FA Authentication Endpoints (8)**

#### **POST /v1/2fa/setup** - Setup 2FA for Client
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "client_001"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/2fa/setup
```
**Response:**
```json
{
  "message": "2FA setup initiated",
  "user_id": "client_001",
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "manual_entry_key": "JBSWY3DPEHPK3PXP",
  "instructions": "Scan QR code with Google Authenticator, Microsoft Authenticator, or Authy"
}
```

#### **POST /v1/2fa/verify-setup** - Verify 2FA Setup
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "client_001", "totp_code": "123456"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/2fa/verify-setup
```

#### **POST /v1/2fa/login-with-2fa** - Login with 2FA
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "client_001", "totp_code": "123456"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/2fa/login-with-2fa
```

#### **GET /v1/2fa/status/{client_id}** - Get 2FA Status
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/2fa/status/client_001
```

#### **POST /v1/2fa/disable** - Disable 2FA
#### **POST /v1/2fa/regenerate-backup-codes** - Regenerate Backup Codes
#### **GET /v1/2fa/test-token/{client_id}/{token}** - Test 2FA Token
#### **GET /v1/2fa/demo-setup** - Demo 2FA Setup

---

### **Client Portal Endpoints (1)**

#### **POST /v1/client/login** - Client Authentication with JWT
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"client_id": "TECH001", "password": "demo123"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login
```
**Response:**
```json
{
  "success": true,
  "message": "Authentication successful",
  "client_id": "TECH001",
  "company_name": "Tech Innovations Inc",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "permissions": ["view_jobs", "create_jobs", "view_candidates", "schedule_interviews"]
}
```

---

### **Candidate Portal Endpoints (5)**

#### **POST /v1/candidate/register** - Candidate Registration
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith",
       "email": "jane@example.com",
       "password": "securepassword123",
       "phone": "+1-555-0123",
       "location": "San Francisco",
       "experience_years": 3,
       "technical_skills": "React, JavaScript, Node.js",
       "education_level": "Bachelors",
       "seniority_level": "Mid-level"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/register
```
**Response:**
```json
{
  "success": true,
  "message": "Registration successful",
  "candidate_id": 32
}
```

#### **POST /v1/candidate/login** - Candidate Login with JWT
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "jane@example.com", "password": "securepassword123"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/login
```
**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "candidate": {
    "id": 32,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1-555-0123",
    "location": "San Francisco",
    "experience_years": 3,
    "technical_skills": "React, JavaScript, Node.js",
    "seniority_level": "Mid-level",
    "education_level": "Bachelors",
    "status": "applied"
  }
}
```

#### **PUT /v1/candidate/profile/{id}** - Update Candidate Profile
```bash
curl -X PUT -H "Authorization: Bearer <candidate_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith Updated",
       "technical_skills": "React, JavaScript, Node.js, TypeScript",
       "experience_years": 4
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/profile/32
```

#### **POST /v1/candidate/apply** - Job Application Submission
```bash
curl -X POST -H "Authorization: Bearer <candidate_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 32,
       "job_id": 1,
       "cover_letter": "I am very interested in this position..."
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/apply
```

#### **GET /v1/candidate/applications/{id}** - Get Candidate Applications
```bash
curl -H "Authorization: Bearer <candidate_jwt_token>" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/applications/32
```

---

## 🤖 Agent Service API (6 Endpoints)

### **Base URL**
- **Production**: https://bhiv-hr-agent-m1me.onrender.com
- **Local**: http://localhost:9000

### **Core Endpoints (2)**

#### **GET /** - Service Information
```bash
curl https://bhiv-hr-agent-m1me.onrender.com/
```
**Response:**
```json
{
  "service": "BHIV AI Agent",
  "version": "3.0.0",
  "endpoints": 6,
  "available_endpoints": {
    "root": "GET / - Service information",
    "health": "GET /health - Service health check",
    "test_db": "GET /test-db - Database connectivity test",
    "match": "POST /match - AI-powered candidate matching",
    "batch_match": "POST /batch-match - Batch AI matching for multiple jobs",
    "analyze": "GET /analyze/{candidate_id} - Detailed candidate analysis"
  }
}
```

#### **GET /health** - Health Check
```bash
curl https://bhiv-hr-agent-m1me.onrender.com/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "BHIV AI Agent",
  "version": "3.0.0",
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

---

### **AI Processing Endpoints (3)**

#### **POST /match** - Phase 3 AI Semantic Matching
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"job_id": 1}' \
     https://bhiv-hr-agent-m1me.onrender.com/match
```
**Response:**
```json
{
  "job_id": 1,
  "top_candidates": [
    {
      "candidate_id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "score": 92.5,
      "skills_match": ["Python", "Django", "PostgreSQL"],
      "experience_match": "5y - Phase 3 matched",
      "location_match": true,
      "reasoning": "Semantic match: 0.85; Skills: Python, Django; Experience: 5y"
    }
  ],
  "total_candidates": 31,
  "processing_time": 0.015,
  "algorithm_version": "3.0.0-phase3-production",
  "status": "success"
}
```

#### **POST /batch-match** - Batch Processing for Multiple Jobs
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"job_ids": [1, 2, 3]}' \
     https://bhiv-hr-agent-m1me.onrender.com/batch-match
```
**Response:**
```json
{
  "batch_results": {
    "1": {
      "job_id": 1,
      "matches": [
        {
          "candidate_id": 1,
          "name": "John Smith",
          "score": 92.5,
          "reasoning": "Batch AI matching - Job 1"
        }
      ],
      "algorithm": "batch-production"
    }
  },
  "total_jobs_processed": 3,
  "total_candidates_analyzed": 31,
  "algorithm_version": "3.0.0-phase3-production-batch",
  "status": "success"
}
```

#### **GET /analyze/{candidate_id}** - Detailed Candidate Analysis
```bash
curl https://bhiv-hr-agent-m1me.onrender.com/analyze/1
```
**Response:**
```json
{
  "candidate_id": 1,
  "name": "John Smith",
  "email": "john@example.com",
  "experience_years": 5,
  "seniority_level": "Software Developer",
  "education_level": "Masters",
  "location": "Mumbai",
  "skills_analysis": {
    "Programming": ["python", "java", "javascript"],
    "Web Development": ["django", "react"],
    "Database": ["postgresql", "mysql"]
  },
  "semantic_skills": ["Python", "Django", "PostgreSQL", "REST APIs"],
  "total_skills": 15,
  "ai_analysis_enabled": true,
  "analysis_timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

---

### **Diagnostics Endpoints (1)**

#### **GET /test-db** - Database Connectivity Test
```bash
curl https://bhiv-hr-agent-m1me.onrender.com/test-db
```
**Response:**
```json
{
  "status": "success",
  "candidates_count": 31,
  "samples": [
    {"id": 1, "name": "John Smith"},
    {"id": 2, "name": "Jane Doe"},
    {"id": 3, "name": "Mike Johnson"}
  ]
}
```

---

## 🔒 Authentication Guide

### **API Key Authentication**
```bash
# Primary authentication method
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### **Client JWT Authentication**
```bash
# Step 1: Login to get JWT token
curl -X POST -H "Content-Type: application/json" \
     -d '{"client_id": "TECH001", "password": "demo123"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login

# Step 2: Use JWT token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **Candidate JWT Authentication**
```bash
# Step 1: Register or login to get JWT token
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "candidate@example.com", "password": "password123"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/login

# Step 2: Use candidate JWT token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📊 Rate Limiting

### **Rate Limits by Endpoint**
```
Default Tier:
- /v1/jobs: 100 requests/minute
- /v1/candidates/search: 50 requests/minute
- /v1/match: 20 requests/minute
- /v1/candidates/bulk: 5 requests/minute
- Default: 60 requests/minute

Premium Tier:
- /v1/jobs: 500 requests/minute
- /v1/candidates/search: 200 requests/minute
- /v1/match: 100 requests/minute
- /v1/candidates/bulk: 25 requests/minute
- Default: 300 requests/minute
```

### **Dynamic Rate Limiting**
Rate limits adjust based on system CPU usage:
- **High Load (>80% CPU)**: Reduce limits by 50%
- **Low Load (<30% CPU)**: Increase limits by 50%
- **Normal Load**: Standard limits apply

---

## 🚨 Error Handling

### **Standard Error Response**
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": "Email format is invalid"
  },
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

### **Common HTTP Status Codes**
- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Too Many Requests
- **500**: Internal Server Error

---

## 📈 Performance Metrics

### **Response Times**
- **Gateway API**: <100ms average
- **Agent API**: <50ms average
- **AI Matching**: <0.02 seconds
- **Database Queries**: <50ms

### **Throughput**
- **Gateway**: 500+ requests/minute
- **Agent**: 200+ requests/minute
- **Concurrent Users**: 10+ supported
- **Batch Processing**: 50 candidates/chunk

---

## 🔧 SDK & Integration

### **cURL Examples**
All examples provided above use cURL for easy testing and integration.

### **Python Integration Example**
```python
import requests

# API Configuration
BASE_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Get all jobs
response = requests.get(f"{BASE_URL}/v1/jobs", headers=HEADERS)
jobs = response.json()

# AI matching
match_response = requests.get(f"{BASE_URL}/v1/match/1/top", headers=HEADERS)
matches = match_response.json()
```

### **JavaScript Integration Example**
```javascript
const BASE_URL = "https://bhiv-hr-gateway-46pz.onrender.com";
const API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o";

const headers = {
  "Authorization": `Bearer ${API_KEY}`,
  "Content-Type": "application/json"
};

// Get candidates
fetch(`${BASE_URL}/v1/candidates`, { headers })
  .then(response => response.json())
  .then(data => console.log(data));

// AI matching
fetch(`${BASE_URL}/v1/match/1/top`, { headers })
  .then(response => response.json())
  .then(matches => console.log(matches));
```

---

## 📚 Interactive Documentation

### **Swagger UI**
- **Gateway**: https://bhiv-hr-gateway-46pz.onrender.com/docs
- **Agent**: https://bhiv-hr-agent-m1me.onrender.com/docs

### **ReDoc**
- **Gateway**: https://bhiv-hr-gateway-46pz.onrender.com/redoc
- **Agent**: https://bhiv-hr-agent-m1me.onrender.com/redoc

---

**BHIV HR Platform API Documentation** - Complete API reference with 61 endpoints, triple authentication, and comprehensive examples.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: January 2025 | **API Version**: v3.1.0 | **Endpoints**: 61 Total | **Status**: ✅ All Operational