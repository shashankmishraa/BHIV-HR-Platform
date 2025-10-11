# 🔗 BHIV HR Platform - Complete API Documentation

**Generated**: January 2025  
**API Version**: 3.1.0  
**Base URL**: https://bhiv-hr-gateway-46pz.onrender.com  
**Authentication**: Bearer Token Required

---

## 📊 API Overview

### **Total Endpoints**: 55 (49 Gateway + 6 Agent)
### **Algorithm Version**: 3.0.0-phase3-production
### **AI Engine**: Phase 3 Semantic Matching with Learning
### **Authentication**: Bearer Token
### **Rate Limiting**: 60 requests/minute (default), granular limits by endpoint
### **Response Format**: JSON
### **Status**: 🟢 All endpoints operational

---

## 🔑 Authentication

All API endpoints require authentication using Bearer tokens in the Authorization header:

```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

---

## 📋 Core API Endpoints (3)

### 1. GET `/` - API Root Information
**Purpose**: Returns API service information and available endpoints  
**Authentication**: None required  
**Rate Limit**: 60/min

```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/
```

**Response**:
```json
{
  "message": "BHIV HR Platform API Gateway",
  "version": "3.1.0",
  "status": "healthy",
  "endpoints": 55,
  "documentation": "/docs",
  "monitoring": "/metrics"
}
```

### 2. GET `/health` - Health Check
**Purpose**: Service health status with security headers  
**Authentication**: None required  
**Rate Limit**: 60/min

```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "BHIV HR Gateway",
  "version": "3.1.0",
  "timestamp": "2025-01-02T10:30:00Z"
}
```

### 3. GET `/test-candidates` - Database Connectivity Test
**Purpose**: Test database connection and return candidate count  
**Authentication**: Bearer token required  
**Rate Limit**: 60/min

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates
```

**Response**:
```json
{
  "database_status": "connected",
  "total_candidates": 31,
  "test_timestamp": "2025-01-02T10:30:00Z"
}
```

---

## 💼 Job Management (2)

### 1. POST `/v1/jobs` - Create Job Posting
**Purpose**: Create new job posting with validation  
**Authentication**: Bearer token required  
**Rate Limit**: 100/min

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Software Engineer",
    "department": "Engineering",
    "location": "Remote",
    "experience_level": "Senior",
    "requirements": "Python, FastAPI, PostgreSQL",
    "description": "Join our engineering team..."
  }' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

**Response**:
```json
{
  "message": "Job created successfully",
  "job_id": 123,
  "created_at": "2025-01-02T10:30:00Z"
}
```

### 2. GET `/v1/jobs` - List All Active Jobs
**Purpose**: Retrieve all active job postings with pagination  
**Authentication**: Bearer token required  
**Rate Limit**: 100/min

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

**Response**:
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Senior Software Engineer",
      "department": "Engineering",
      "location": "Remote",
      "experience_level": "Senior",
      "requirements": "Python, FastAPI",
      "description": "Join our team...",
      "created_at": "2025-01-02T10:30:00Z"
    }
  ],
  "count": 1
}
```

---

## 👥 Candidate Management (3)

### 1. GET `/v1/candidates/job/{job_id}` - Get Candidates by Job
**Purpose**: Retrieve candidates for specific job (dynamic matching)  
**Authentication**: Bearer token required  
**Rate Limit**: 50/min

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/job/1
```

### 2. GET `/v1/candidates/search` - Search & Filter Candidates
**Purpose**: Advanced candidate search with multiple filters  
**Authentication**: Bearer token required  
**Rate Limit**: 50/min

**Query Parameters**:
- `skills`: Skills to search for
- `location`: Location filter
- `experience_min`: Minimum years of experience

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?skills=Python&location=Remote&experience_min=3"
```

### 3. POST `/v1/candidates/bulk` - Bulk Upload Candidates
**Purpose**: Upload multiple candidates in batch  
**Authentication**: Bearer token required  
**Rate Limit**: 5/min

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": [
      {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-555-0123",
        "technical_skills": "Python, JavaScript",
        "experience_years": 5
      }
    ]
  }' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/bulk
```

---

## 🤖 AI Matching Engine (1)

### 1. GET `/v1/match/{job_id}/top` - AI-Powered Candidate Matching
**Purpose**: Get top candidates matched by AI for specific job  
**Authentication**: Bearer token required  
**Rate Limit**: 20/min

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top?limit=10
```

**Response**:
```json
{
  "matches": [
    {
      "candidate_id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "score": 85.5,
      "skills_match": ["Python", "FastAPI"],
      "experience_match": "Perfect match for Senior level",
      "values_alignment": 4.2,
      "recommendation_strength": "Strong Match"
    }
  ],
  "job_id": 1,
  "algorithm_version": "v2.0.0-dynamic",
  "processing_time": "0.05s"
}
```

---

## 📊 Assessment & Workflow (3)

### 1. POST `/v1/feedback` - Submit Values Assessment
**Purpose**: Submit 5-point values assessment for candidate  
**Authentication**: Bearer token required  
**Rate Limit**: 60/min

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "integrity": 4,
    "honesty": 5,
    "discipline": 4,
    "hard_work": 4,
    "gratitude": 5
  }' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```

### 2. GET `/v1/interviews` - List Scheduled Interviews
**Purpose**: Retrieve all scheduled interviews  
**Authentication**: Bearer token required  
**Rate Limit**: 60/min

### 3. POST `/v1/interviews` - Schedule Interview
**Purpose**: Schedule new interview for candidate  
**Authentication**: Bearer token required  
**Rate Limit**: 60/min

---

## 📈 Analytics & Statistics (2)

### 1. GET `/candidates/stats` - Candidate Statistics
**Purpose**: Get real-time candidate statistics  
**Authentication**: Bearer token required  
**Rate Limit**: 60/min

### 2. GET `/v1/reports/job/{job_id}/export.csv` - Export Job Report
**Purpose**: Export job-specific report in CSV format  
**Authentication**: Bearer token required  
**Rate Limit**: 60/min

---

## 🏢 Client Portal API (1)

### 1. POST `/v1/client/login` - Client Authentication
**Purpose**: Authenticate client and return JWT token  
**Authentication**: None required (login endpoint)  
**Rate Limit**: 60/min

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "TECH001",
    "password": "demo123"
  }' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login
```

---

## 🔒 Security Testing (7)

### 1. GET `/v1/security/rate-limit-status` - Rate Limit Status
**Purpose**: Check current rate limiting status  
**Authentication**: Bearer token required

### 2. GET `/v1/security/blocked-ips` - View Blocked IPs
**Purpose**: View list of blocked IP addresses  
**Authentication**: Bearer token required

### 3. POST `/v1/security/test-input-validation` - Input Validation Test
**Purpose**: Test input validation and XSS protection  
**Authentication**: Bearer token required

### 4. POST `/v1/security/test-email-validation` - Email Validation
**Purpose**: Test email format validation  
**Authentication**: Bearer token required

### 5. POST `/v1/security/test-phone-validation` - Phone Validation
**Purpose**: Test phone number format validation  
**Authentication**: Bearer token required

### 6. GET `/v1/security/security-headers-test` - Security Headers Test
**Purpose**: Test security headers implementation  
**Authentication**: Bearer token required

### 7. GET `/v1/security/penetration-test-endpoints` - Penetration Testing Info
**Purpose**: Get information about penetration testing endpoints  
**Authentication**: Bearer token required

---

## 🛡️ CSP Management (4)

### 1. POST `/v1/security/csp-report` - CSP Violation Reporting
**Purpose**: Report Content Security Policy violations  
**Authentication**: Bearer token required

### 2. GET `/v1/security/csp-violations` - View CSP Violations
**Purpose**: View recorded CSP violations  
**Authentication**: Bearer token required

### 3. GET `/v1/security/csp-policies` - Current CSP Policies
**Purpose**: Get current Content Security Policy settings  
**Authentication**: Bearer token required

### 4. POST `/v1/security/test-csp-policy` - Test CSP Policy
**Purpose**: Test Content Security Policy configuration  
**Authentication**: Bearer token required

---

## 🔐 Two-Factor Authentication (8)

### 1. POST `/v1/2fa/setup` - Setup 2FA
**Purpose**: Initialize 2FA setup with QR code generation  
**Authentication**: Bearer token required

### 2. POST `/v1/2fa/verify-setup` - Verify 2FA Setup
**Purpose**: Verify 2FA setup with TOTP code  
**Authentication**: Bearer token required

### 3. POST `/v1/2fa/login-with-2fa` - Login with 2FA
**Purpose**: Authenticate using 2FA TOTP code  
**Authentication**: Bearer token required

### 4. GET `/v1/2fa/status/{client_id}` - Get 2FA Status
**Purpose**: Check 2FA status for specific client  
**Authentication**: Bearer token required

### 5. POST `/v1/2fa/disable` - Disable 2FA
**Purpose**: Disable 2FA for user account  
**Authentication**: Bearer token required

### 6. POST `/v1/2fa/regenerate-backup-codes` - Regenerate Backup Codes
**Purpose**: Generate new backup codes for 2FA  
**Authentication**: Bearer token required

### 7. GET `/v1/2fa/test-token/{client_id}/{token}` - Test 2FA Token
**Purpose**: Test 2FA token validity  
**Authentication**: Bearer token required

### 8. GET `/v1/2fa/demo-setup` - Demo 2FA Setup
**Purpose**: Get demo 2FA setup for testing  
**Authentication**: Bearer token required

---

## 🔑 Password Management (6)

### 1. POST `/v1/password/validate` - Validate Password Strength
**Purpose**: Validate password strength and complexity  
**Authentication**: Bearer token required

### 2. POST `/v1/password/generate` - Generate Secure Password
**Purpose**: Generate cryptographically secure password  
**Authentication**: Bearer token required

### 3. GET `/v1/password/policy` - Password Policy
**Purpose**: Get current password policy requirements  
**Authentication**: Bearer token required

### 4. POST `/v1/password/change` - Change Password
**Purpose**: Change user password securely  
**Authentication**: Bearer token required

### 5. GET `/v1/password/strength-test` - Password Strength Testing Tool
**Purpose**: Get password strength testing information  
**Authentication**: Bearer token required

### 6. GET `/v1/password/security-tips` - Password Security Best Practices
**Purpose**: Get password security recommendations  
**Authentication**: Bearer token required

---

## 📊 Monitoring (3)

### 1. GET `/metrics` - Prometheus Metrics
**Purpose**: Export Prometheus-compatible metrics  
**Authentication**: Bearer token required  
**Response Format**: Plain text (Prometheus format)

### 2. GET `/health/detailed` - Detailed Health Check
**Purpose**: Comprehensive health check with system metrics  
**Authentication**: Bearer token required

### 3. GET `/metrics/dashboard` - Metrics Dashboard
**Purpose**: Get dashboard-ready metrics data  
**Authentication**: Bearer token required

---

## 🚨 Error Handling

### **Standard Error Response Format**
```json
{
  "error": "Error description",
  "status_code": 400,
  "timestamp": "2025-01-02T10:30:00Z",
  "path": "/v1/jobs"
}
```

### **Common HTTP Status Codes**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized (Invalid/Missing API Key)
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests (Rate Limited)
- `500` - Internal Server Error

---

## 🔄 Rate Limiting

### **Default Limits**
- **Default**: 60 requests/minute
- **Job Management**: 100 requests/minute
- **Candidate Search**: 50 requests/minute
- **AI Matching**: 20 requests/minute
- **Bulk Operations**: 5 requests/minute

### **Rate Limit Headers**
All responses include rate limiting headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests in current window

---

## 📝 Usage Examples

### **Complete Workflow Example**

```bash
# 1. Check API health
curl https://bhiv-hr-gateway-46pz.onrender.com/health

# 2. Create a job
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Software Engineer", "department": "Engineering"}' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# 3. Upload candidates
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"candidates": [{"name": "John Doe", "email": "john@example.com"}]}' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/bulk

# 4. Get AI matches
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top

# 5. Submit assessment
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 1, "job_id": 1, "integrity": 5}' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```

---

## 🔗 Interactive Documentation

### **Swagger/OpenAPI Documentation**
Visit the interactive API documentation at:
**https://bhiv-hr-gateway-46pz.onrender.com/docs**

### **Alternative Documentation**
ReDoc format available at:
**https://bhiv-hr-gateway-46pz.onrender.com/redoc**

---

## 📞 Support & Resources

### **API Status**
- **Status Page**: All endpoints operational
- **Response Time**: <100ms average
- **Uptime**: 99.9% target
- **Support**: GitHub Issues

### **Development Resources**
- **Base URL**: https://bhiv-hr-gateway-46pz.onrender.com
- **API Key**: Contact for production access
- **Demo Credentials**: TECH001 / demo123
- **GitHub**: https://github.com/shashankmishraa/BHIV-HR-Platform

---

**Last Updated**: January 2025  
**API Version**: 3.1.0  
**Status**: 🟢 All 55 Endpoints Operational (49 Gateway + 6 Agent)