# BHIV HR Platform - Complete Endpoint Analysis & Testing

## 📊 Endpoint Summary

### **API Gateway (46 Endpoints)**
- **Core API**: 3 endpoints
- **Job Management**: 2 endpoints  
- **Candidate Management**: 3 endpoints
- **AI Matching Engine**: 1 endpoint
- **Assessment & Workflow**: 3 endpoints
- **Analytics & Statistics**: 2 endpoints
- **Client Portal API**: 1 endpoint
- **Security Testing**: 7 endpoints
- **CSP Management**: 4 endpoints
- **Two-Factor Authentication**: 8 endpoints
- **Password Management**: 6 endpoints
- **Monitoring**: 3 endpoints

### **AI Agent (4 Endpoints)**
- **Core API**: 2 endpoints
- **AI Matching Engine**: 1 endpoint
- **System Diagnostics**: 1 endpoint

## 🔍 Detailed Endpoint Analysis

### **1. Core API Endpoints (Gateway)**

#### `GET /` - API Root Information
**Purpose**: Service information and documentation links
**Authentication**: None required
**Response**: Service metadata, version, endpoint count
```bash
curl http://localhost:8000/
```
**Expected**: 200 OK with service info

#### `GET /health` - Health Check
**Purpose**: Service health monitoring with security headers
**Authentication**: None required
**Response**: Health status, timestamp, security headers
```bash
curl -v http://localhost:8000/health
```
**Expected**: 200 OK with security headers (X-Frame-Options, CSP, etc.)

#### `GET /test-candidates` - Database Connectivity Test
**Purpose**: Test database connection and candidate count
**Authentication**: API Key required
**Response**: Database status, candidate count, timestamp
```bash
curl -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/test-candidates
```
**Expected**: 200 OK with database connection status

### **2. Job Management Endpoints**

#### `POST /v1/jobs` - Create New Job Posting
**Purpose**: Create job with database persistence
**Authentication**: API Key required
**Request Body**: JobCreate model (title, department, location, etc.)
```bash
curl -X POST http://localhost:8000/v1/jobs \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "department": "Engineering", 
    "location": "Remote",
    "experience_level": "Senior",
    "requirements": "Python, Django, PostgreSQL, 5+ years",
    "description": "We are looking for a senior Python developer..."
  }'
```
**Expected**: 200 OK with job_id and creation timestamp

#### `GET /v1/jobs` - List All Active Jobs
**Purpose**: Retrieve all active job postings
**Authentication**: API Key required
**Response**: Array of jobs with full details
```bash
curl -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/v1/jobs
```
**Expected**: 200 OK with jobs array and count

### **3. Candidate Management Endpoints**

#### `GET /v1/candidates/job/{job_id}` - Get Candidates by Job
**Purpose**: Dynamic candidate retrieval for specific job
**Authentication**: API Key required
**Parameters**: job_id (path parameter)
```bash
curl -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/v1/candidates/job/1
```
**Expected**: 200 OK with candidates array

#### `GET /v1/candidates/search` - Search & Filter Candidates
**Purpose**: Advanced candidate search with filters
**Authentication**: API Key required
**Query Parameters**: skills, location, experience_min
```bash
curl -H "Authorization: Bearer myverysecureapikey123" \
  "http://localhost:8000/v1/candidates/search?skills=python&location=mumbai&experience_min=3"
```
**Expected**: 200 OK with filtered candidates

#### `POST /v1/candidates/bulk` - Bulk Upload Candidates
**Purpose**: Bulk candidate insertion with error handling
**Authentication**: API Key required
**Request Body**: CandidateBulk model with candidates array
```bash
curl -X POST http://localhost:8000/v1/candidates/bulk \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": [
      {
        "name": "John Doe",
        "email": "john@example.com",
        "technical_skills": "Python, Django, React",
        "experience_years": 5
      }
    ]
  }'
```
**Expected**: 200 OK with insertion results and error details

### **4. AI Matching Engine Endpoints**

#### `GET /v1/match/{job_id}/top` - Semantic Candidate Matching (Gateway)
**Purpose**: Get top candidate matches for job via gateway
**Authentication**: API Key required
**Parameters**: job_id (path), limit (query, optional)
```bash
curl -H "Authorization: Bearer myverysecureapikey123" \
  "http://localhost:8000/v1/match/1/top?limit=5"
```
**Expected**: 200 OK with matched candidates and scores

#### `POST /match` - AI-Powered Candidate Matching (Agent)
**Purpose**: Advanced semantic matching with dynamic scoring
**Authentication**: None (internal service)
**Request Body**: MatchRequest model with job_id
```bash
curl -X POST http://localhost:9000/match \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}'
```
**Expected**: 200 OK with MatchResponse including top candidates, scores, reasoning

### **5. Assessment & Workflow Endpoints**

#### `POST /v1/feedback` - Values Assessment
**Purpose**: Submit candidate values assessment (5-point scale)
**Authentication**: API Key required
**Request Body**: FeedbackSubmission model with values scores
```bash
curl -X POST http://localhost:8000/v1/feedback \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "integrity": 5,
    "honesty": 4,
    "discipline": 5,
    "hard_work": 4,
    "gratitude": 5,
    "comments": "Excellent candidate"
  }'
```
**Expected**: 200 OK with average score calculation

#### `GET /v1/interviews` - Get All Interviews
**Purpose**: Retrieve scheduled interviews with candidate/job details
**Authentication**: API Key required
```bash
curl -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/v1/interviews
```
**Expected**: 200 OK with interviews array

#### `POST /v1/interviews` - Schedule Interview
**Purpose**: Schedule new interview with database persistence
**Authentication**: API Key required
**Request Body**: InterviewSchedule model
```bash
curl -X POST http://localhost:8000/v1/interviews \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "interview_date": "2025-01-20T10:00:00",
    "interviewer": "John Smith",
    "notes": "Technical interview"
  }'
```
**Expected**: 200 OK with interview_id

### **6. Client Portal Authentication**

#### `POST /v1/client/login` - Client Authentication
**Purpose**: Authenticate client with credentials
**Authentication**: None (login endpoint)
**Request Body**: ClientLogin model
```bash
curl -X POST http://localhost:8000/v1/client/login \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "TECH001",
    "password": "demo123"
  }'
```
**Expected**: 200 OK with access_token and permissions

### **7. Security Testing Endpoints**

#### `GET /v1/security/rate-limit-status` - Rate Limit Status
**Purpose**: Check current rate limiting configuration
**Authentication**: API Key required
```bash
curl -H "Authorization: Bearer myverysecureapikey123" \
  http://localhost:8000/v1/security/rate-limit-status
```
**Expected**: 200 OK with rate limit details

#### `POST /v1/security/test-input-validation` - Input Validation Test
**Purpose**: Test XSS/SQL injection protection
**Authentication**: API Key required
**Request Body**: InputValidation model
```bash
curl -X POST http://localhost:8000/v1/security/test-input-validation \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "<script>alert(\"xss\")</script>"
  }'
```
**Expected**: 200 OK with threat detection results

### **8. Two-Factor Authentication Endpoints**

#### `POST /v1/2fa/setup` - Setup 2FA
**Purpose**: Generate TOTP secret and QR code
**Authentication**: API Key required
**Request Body**: TwoFASetup model
```bash
curl -X POST http://localhost:8000/v1/2fa/setup \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "TECH001"}'
```
**Expected**: 200 OK with secret, QR code, and setup instructions

#### `POST /v1/2fa/verify-setup` - Verify 2FA Setup
**Purpose**: Verify TOTP code during setup
**Authentication**: API Key required
**Request Body**: TwoFALogin model
```bash
curl -X POST http://localhost:8000/v1/2fa/verify-setup \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "TECH001",
    "totp_code": "123456"
  }'
```
**Expected**: 200 OK if valid code, 401 if invalid

### **9. Password Management Endpoints**

#### `POST /v1/password/validate` - Password Strength Validation
**Purpose**: Validate password against security policy
**Authentication**: API Key required
**Request Body**: PasswordValidation model
```bash
curl -X POST http://localhost:8000/v1/password/validate \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{"password": "StrongPass123!"}'
```
**Expected**: 200 OK with strength score and feedback

#### `POST /v1/password/generate` - Generate Secure Password
**Purpose**: Generate cryptographically secure password
**Authentication**: API Key required
**Query Parameters**: length (optional, default 12)
```bash
curl -X POST "http://localhost:8000/v1/password/generate?length=16" \
  -H "Authorization: Bearer myverysecureapikey123"
```
**Expected**: 200 OK with generated password and entropy info

### **10. Analytics & Statistics Endpoints**

#### `GET /candidates/stats` - Candidate Statistics
**Purpose**: Get platform-wide candidate statistics
**Authentication**: API Key required
```bash
curl -H "Authorization: Bearer myverysecureapikey123" \
  http://localhost:8000/candidates/stats
```
**Expected**: 200 OK with candidate counts and metrics

#### `GET /v1/reports/job/{job_id}/export.csv` - Export Job Report
**Purpose**: Generate downloadable job report
**Authentication**: API Key required
**Parameters**: job_id (path parameter)
```bash
curl -H "Authorization: Bearer myverysecureapikey123" \
  http://localhost:8000/v1/reports/job/1/export.csv
```
**Expected**: 200 OK with download URL and metadata

### **11. Monitoring Endpoints**

#### `GET /metrics` - Prometheus Metrics
**Purpose**: Export metrics in Prometheus format
**Authentication**: None required
```bash
curl http://localhost:8000/metrics
```
**Expected**: 200 OK with metrics in text/plain format

#### `GET /health/detailed` - Detailed Health Check
**Purpose**: Comprehensive system health information
**Authentication**: None required
```bash
curl http://localhost:8000/health/detailed
```
**Expected**: 200 OK with detailed system status

#### `GET /metrics/dashboard` - Metrics Dashboard Data
**Purpose**: Dashboard-ready metrics and analytics
**Authentication**: None required
```bash
curl http://localhost:8000/metrics/dashboard
```
**Expected**: 200 OK with performance and business metrics

## 🧪 Comprehensive Testing Suite

### **Automated Test Script**
```bash
#!/bin/bash
# Complete endpoint testing script

API_BASE="http://localhost:8000"
AGENT_BASE="http://localhost:9000"
API_KEY="myverysecureapikey123"
AUTH_HEADER="Authorization: Bearer $API_KEY"

echo "=== BHIV HR Platform Endpoint Testing ==="

# Test Core Endpoints
echo "Testing Core Endpoints..."
curl -s "$API_BASE/" | jq .
curl -s "$API_BASE/health" | jq .
curl -s -H "$AUTH_HEADER" "$API_BASE/test-candidates" | jq .

# Test Job Management
echo "Testing Job Management..."
curl -s -H "$AUTH_HEADER" "$API_BASE/v1/jobs" | jq .

# Test Candidate Management  
echo "Testing Candidate Management..."
curl -s -H "$AUTH_HEADER" "$API_BASE/v1/candidates/search" | jq .

# Test AI Matching
echo "Testing AI Matching..."
curl -s -X POST "$AGENT_BASE/match" \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}' | jq .

# Test Security
echo "Testing Security..."
curl -s -H "$AUTH_HEADER" "$API_BASE/v1/security/rate-limit-status" | jq .

# Test Authentication
echo "Testing Authentication..."
curl -s -X POST "$API_BASE/v1/client/login" \
  -H "Content-Type: application/json" \
  -d '{"client_id": "TECH001", "password": "demo123"}' | jq .

echo "=== Testing Complete ==="
```

### **Performance Testing**
```bash
# Load testing with concurrent requests
for i in {1..10}; do
  curl -s -H "Authorization: Bearer myverysecureapikey123" \
    "http://localhost:8000/v1/jobs" &
done
wait
```

### **Security Testing**
```bash
# XSS Testing
curl -X POST http://localhost:8000/v1/security/test-input-validation \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{"input_data": "<script>alert(\"xss\")</script>"}'

# SQL Injection Testing  
curl -X POST http://localhost:8000/v1/security/test-input-validation \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{"input_data": "'; DROP TABLE users; --"}'
```

## 📋 Testing Checklist

### **Functional Testing**
- [ ] All endpoints return expected HTTP status codes
- [ ] Request/response schemas match OpenAPI specification
- [ ] Database operations persist correctly
- [ ] Error handling returns appropriate error messages
- [ ] Authentication/authorization works correctly

### **Security Testing**
- [ ] API key validation prevents unauthorized access
- [ ] Input validation blocks XSS/SQL injection attempts
- [ ] Rate limiting prevents abuse
- [ ] Security headers are present
- [ ] 2FA setup and verification works

### **Performance Testing**
- [ ] Response times under 100ms for simple endpoints
- [ ] AI matching completes under 2 seconds
- [ ] Concurrent requests handled properly
- [ ] Database connections managed efficiently

### **Integration Testing**
- [ ] Gateway-to-Agent communication works
- [ ] Portal-to-Gateway API calls succeed
- [ ] Database transactions maintain consistency
- [ ] Cross-service authentication functions

## 🎯 Expected Results

### **Successful Deployment Shows**:
1. **All 50 endpoints** responding with correct status codes
2. **Database integration** working across all services
3. **Authentication flows** functioning properly
4. **AI matching** returning realistic candidate scores
5. **Security features** blocking malicious inputs
6. **Monitoring endpoints** providing system metrics
7. **Error handling** graceful and informative

### **Performance Benchmarks**:
- **API Response Time**: < 100ms average
- **AI Matching**: < 2 seconds
- **Database Queries**: < 50ms
- **Concurrent Users**: 50+ simultaneous
- **Throughput**: 1000+ requests/minute

The platform provides **comprehensive API coverage** with robust security, monitoring, and AI capabilities ready for production use.