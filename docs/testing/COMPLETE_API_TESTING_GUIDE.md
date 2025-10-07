# BHIV HR Platform - Complete API Testing Guide

## 🔧 Setup & Authentication

### Environment Variables
```bash
export API_KEY="Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
export GATEWAY_URL="https://bhiv-hr-gateway-46pz.onrender.com"
export AGENT_URL="https://bhiv-hr-agent-m1me.onrender.com"
```

### Headers for All Requests
```bash
-H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
-H "Content-Type: application/json"
```

---

## 📋 GATEWAY SERVICE ENDPOINTS (44 Total)

### 1. CORE ENDPOINTS (3)

#### 1.1 Root Endpoint
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/
```
**Expected Response:**
```json
{
  "message": "BHIV HR Platform API Gateway",
  "version": "3.1.0",
  "status": "operational",
  "endpoints": 46
}
```
**Validation:** Status 200, contains version and endpoint count

#### 1.2 Health Check
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/health
```
**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-03T13:20:00Z",
  "version": "3.1.0",
  "database": "connected",
  "uptime": "2h 15m"
}
```
**Validation:** Status 200, database connected, uptime present

#### 1.3 Test Candidates
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/test-candidates
```
**Expected Response:**
```json
{
  "total_candidates": 112000,
  "sample_candidates": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "technical_skills": "Python, JavaScript"
    }
  ]
}
```
**Validation:** Status 200, contains candidate count and sample data

---

### 2. JOB MANAGEMENT (2)

#### 2.1 List All Jobs
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/v1/jobs
```
**Expected Response:**
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "department": "Engineering",
      "location": "Remote",
      "status": "active",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 15
}
```
**Validation:** Status 200, array of jobs with required fields

#### 2.2 Create New Job
```bash
curl -X POST -H "Authorization: $API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "QA Test Engineer",
    "department": "Quality Assurance", 
    "location": "Remote",
    "experience_level": "Mid-level",
    "requirements": "API Testing, Automation, Python",
    "description": "Join our QA team to ensure product quality"
  }' \
  $GATEWAY_URL/v1/jobs
```
**Expected Response:**
```json
{
  "message": "Job created successfully",
  "job_id": 16,
  "job": {
    "id": 16,
    "title": "QA Test Engineer",
    "status": "active"
  }
}
```
**Validation:** Status 201, returns job_id and confirmation

---

### 3. CANDIDATE MANAGEMENT (3)

#### 3.1 Get All Candidates
```bash
curl -H "Authorization: $API_KEY" "$GATEWAY_URL/v1/candidates?limit=10"
```
**Expected Response:**
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "technical_skills": "Python, Django, PostgreSQL",
      "experience_years": 5,
      "location": "New York"
    }
  ],
  "total": 112000,
  "page": 1,
  "limit": 10
}
```
**Validation:** Status 200, pagination info, candidate array

#### 3.2 Get Specific Candidate
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/v1/candidates/1
```
**Expected Response:**
```json
{
  "candidate": {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1-555-0123",
    "location": "New York",
    "experience_years": 5,
    "technical_skills": "Python, Django, PostgreSQL",
    "seniority_level": "Senior",
    "education_level": "Bachelor's",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```
**Validation:** Status 200, complete candidate profile

#### 3.3 Bulk Upload Candidates
```bash
curl -X POST -H "Authorization: $API_KEY" -H "Content-Type: application/json" \
  -d '[
    {
      "name": "Test Candidate 1",
      "email": "test1@example.com",
      "technical_skills": "Java, Spring Boot",
      "experience_years": 3,
      "location": "San Francisco"
    },
    {
      "name": "Test Candidate 2", 
      "email": "test2@example.com",
      "technical_skills": "React, Node.js",
      "experience_years": 2,
      "location": "Austin"
    }
  ]' \
  $GATEWAY_URL/v1/candidates/bulk
```
**Expected Response:**
```json
{
  "message": "Bulk upload completed",
  "created": 2,
  "failed": 0,
  "candidate_ids": [113001, 113002]
}
```
**Validation:** Status 201, creation count, new IDs

---

### 4. AI MATCHING (1)

#### 4.1 Get Top Matches for Job
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/v1/match/1/top
```
**Expected Response:**
```json
{
  "job_id": 1,
  "job_title": "Senior Python Developer",
  "matches": [
    {
      "candidate_id": 42,
      "name": "Sarah Wilson",
      "match_score": 95.5,
      "technical_skills": "Python, Django, PostgreSQL, AWS",
      "experience_years": 7,
      "match_reasons": [
        "Strong Python expertise",
        "Django framework experience",
        "Senior level experience"
      ]
    }
  ],
  "total_matches": 25
}
```
**Validation:** Status 200, scored matches, match reasons

---

### 5. SECURITY ENDPOINTS (15)

#### 5.1 Rate Limit Status
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/v1/security/rate-limit-status
```
**Expected Response:**
```json
{
  "rate_limit": {
    "requests_remaining": 58,
    "requests_limit": 60,
    "reset_time": "2025-01-03T14:00:00Z",
    "window_seconds": 60
  },
  "user_tier": "standard"
}
```
**Validation:** Status 200, remaining requests, reset time

#### 5.2 Password Validation
```bash
curl -X POST -H "Authorization: $API_KEY" -H "Content-Type: application/json" \
  -d '{"password": "TestPassword123!"}' \
  $GATEWAY_URL/v1/security/validate-password
```
**Expected Response:**
```json
{
  "valid": true,
  "strength": "strong",
  "requirements_met": {
    "min_length": true,
    "uppercase": true,
    "lowercase": true,
    "numbers": true,
    "special_chars": true
  }
}
```
**Validation:** Status 200, validation details

#### 5.3 Generate 2FA Secret
```bash
curl -X POST -H "Authorization: $API_KEY" -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}' \
  $GATEWAY_URL/v1/security/2fa/generate
```
**Expected Response:**
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code_url": "otpauth://totp/BHIV%20HR:test_user?secret=JBSWY3DPEHPK3PXP&issuer=BHIV%20HR",
  "backup_codes": ["12345678", "87654321"]
}
```
**Validation:** Status 200, secret and QR code

#### 5.4 Verify 2FA Token
```bash
curl -X POST -H "Authorization: $API_KEY" -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "token": "123456"}' \
  $GATEWAY_URL/v1/security/2fa/verify
```
**Expected Response:**
```json
{
  "valid": true,
  "message": "Token verified successfully"
}
```
**Validation:** Status 200, verification result

#### 5.5 Security Headers Check
```bash
curl -I -H "Authorization: $API_KEY" $GATEWAY_URL/v1/security/headers
```
**Expected Headers:**
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```
**Validation:** Security headers present

---

### 6. ANALYTICS (2)

#### 6.1 Candidate Statistics
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/candidates/stats
```
**Expected Response:**
```json
{
  "total_candidates": 112000,
  "by_experience": {
    "junior": 35000,
    "mid": 45000,
    "senior": 32000
  },
  "by_location": {
    "Remote": 40000,
    "New York": 15000,
    "San Francisco": 12000
  },
  "top_skills": [
    {"skill": "Python", "count": 25000},
    {"skill": "JavaScript", "count": 22000}
  ]
}
```
**Validation:** Status 200, statistical breakdown

#### 6.2 System Reports
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/v1/reports/summary
```
**Expected Response:**
```json
{
  "period": "last_30_days",
  "metrics": {
    "total_jobs_posted": 45,
    "total_applications": 1250,
    "matches_generated": 3500,
    "interviews_scheduled": 125
  },
  "performance": {
    "avg_response_time": "85ms",
    "uptime": "99.9%"
  }
}
```
**Validation:** Status 200, comprehensive metrics

---

### 7. CLIENT PORTAL (1)

#### 7.1 Client Login
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"client_id": "TECH001", "password": "demo123"}' \
  $GATEWAY_URL/v1/client/login
```
**Expected Response:**
```json
{
  "success": true,
  "client": {
    "client_id": "TECH001",
    "client_name": "Tech Innovations Inc",
    "status": "active"
  },
  "token": "jwt_token_here",
  "expires_in": 3600
}
```
**Validation:** Status 200, JWT token, client info

---

### 8. MONITORING (3)

#### 8.1 Prometheus Metrics
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/metrics
```
**Expected Response:**
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/health"} 1250
http_requests_total{method="POST",endpoint="/v1/jobs"} 45

# HELP response_time_seconds Response time in seconds
# TYPE response_time_seconds histogram
response_time_seconds_bucket{le="0.1"} 1200
```
**Validation:** Prometheus format, key metrics present

#### 8.2 Detailed Health Check
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/health/detailed
```
**Expected Response:**
```json
{
  "status": "healthy",
  "components": {
    "database": {
      "status": "healthy",
      "response_time": "15ms",
      "connections": 5
    },
    "ai_agent": {
      "status": "healthy",
      "response_time": "25ms"
    },
    "cache": {
      "status": "healthy",
      "hit_rate": "85%"
    }
  },
  "system": {
    "cpu_usage": "25%",
    "memory_usage": "60%",
    "disk_usage": "40%"
  }
}
```
**Validation:** Status 200, component health, system metrics

#### 8.3 Metrics Dashboard
```bash
curl -H "Authorization: $API_KEY" $GATEWAY_URL/metrics/dashboard
```
**Expected Response:**
```json
{
  "real_time_metrics": {
    "requests_per_minute": 45,
    "active_users": 12,
    "response_time_avg": "78ms"
  },
  "business_metrics": {
    "jobs_posted_today": 3,
    "matches_generated_today": 125,
    "candidates_added_today": 15
  }
}
```
**Validation:** Status 200, real-time and business metrics

---

## 🤖 AGENT SERVICE ENDPOINTS (5 Total)

### 1. CORE ENDPOINTS (2)

#### 1.1 Agent Root
```bash
curl -H "Authorization: $API_KEY" $AGENT_URL/
```
**Expected Response:**
```json
{
  "service": "BHIV HR AI Agent",
  "version": "2.1.0",
  "status": "operational",
  "capabilities": ["candidate_analysis", "job_matching", "skill_assessment"]
}
```
**Validation:** Status 200, service info and capabilities

#### 1.2 Agent Health
```bash
curl -H "Authorization: $API_KEY" $AGENT_URL/health
```
**Expected Response:**
```json
{
  "status": "healthy",
  "ai_engine": "operational",
  "database": "connected",
  "processing_queue": 0,
  "last_model_update": "2025-01-01T00:00:00Z"
}
```
**Validation:** Status 200, AI engine status, queue info

---

### 2. AI PROCESSING (3)

#### 2.1 Analyze Candidate
```bash
curl -H "Authorization: $API_KEY" $AGENT_URL/analyze/1
```
**Expected Response:**
```json
{
  "candidate_id": 1,
  "analysis": {
    "skill_assessment": {
      "technical_skills": ["Python", "Django", "PostgreSQL"],
      "skill_levels": {
        "Python": "Expert",
        "Django": "Advanced", 
        "PostgreSQL": "Intermediate"
      },
      "overall_score": 85
    },
    "experience_analysis": {
      "years": 5,
      "seniority": "Senior",
      "career_progression": "Strong"
    },
    "recommendations": [
      "Excellent Python expertise",
      "Strong web development background",
      "Database skills complement technical stack"
    ]
  }
}
```
**Validation:** Status 200, detailed analysis, skill assessment

#### 2.2 Match Candidates to Job
```bash
curl -X POST -H "Authorization: $API_KEY" -H "Content-Type: application/json" \
  -d '{"job_id": 1}' \
  $AGENT_URL/match
```
**Expected Response:**
```json
{
  "job_id": 1,
  "matches": [
    {
      "candidate_id": 42,
      "match_score": 95.5,
      "confidence": "high",
      "match_factors": {
        "skills_match": 90,
        "experience_match": 95,
        "location_match": 100
      },
      "explanation": "Excellent technical fit with strong Python and Django experience"
    }
  ],
  "processing_time": "0.02s",
  "total_evaluated": 112000
}
```
**Validation:** Status 200, scored matches, processing time

#### 2.3 Bulk Analysis
```bash
curl -X POST -H "Authorization: $API_KEY" -H "Content-Type: application/json" \
  -d '{"candidate_ids": [1, 2, 3, 4, 5]}' \
  $AGENT_URL/analyze/bulk
```
**Expected Response:**
```json
{
  "analyses": [
    {
      "candidate_id": 1,
      "overall_score": 85,
      "key_strengths": ["Python", "Leadership"]
    }
  ],
  "processed": 5,
  "processing_time": "0.15s"
}
```
**Validation:** Status 200, bulk analysis results

---

## 🧪 VALIDATION CHECKLIST

### ✅ Success Criteria
- [ ] All endpoints return appropriate HTTP status codes
- [ ] Response times under 100ms for simple queries
- [ ] Authentication required for protected endpoints
- [ ] Rate limiting enforced (60 requests/minute)
- [ ] Error responses include helpful messages
- [ ] Database connections stable
- [ ] AI processing completes within 2 seconds

### ❌ Failure Scenarios to Test
```bash
# Invalid API key
curl -H "Authorization: Bearer invalid_key" $GATEWAY_URL/health

# Rate limit exceeded (send 61+ requests in 1 minute)
for i in {1..65}; do curl -H "Authorization: $API_KEY" $GATEWAY_URL/health; done

# Invalid JSON payload
curl -X POST -H "Authorization: $API_KEY" -d 'invalid json' $GATEWAY_URL/v1/jobs

# Non-existent resource
curl -H "Authorization: $API_KEY" $GATEWAY_URL/v1/candidates/999999
```

### 📊 Performance Benchmarks
```bash
# Response time test
time curl -H "Authorization: $API_KEY" $GATEWAY_URL/health

# Concurrent requests test
ab -n 100 -c 10 -H "Authorization: $API_KEY" $GATEWAY_URL/health

# Large dataset query
curl -H "Authorization: $API_KEY" "$GATEWAY_URL/v1/candidates?limit=1000"
```

---

## 🔧 Troubleshooting

### Common Issues
1. **503 Service Unavailable**: Service starting up, wait 30 seconds
2. **401 Unauthorized**: Check API key format and Bearer prefix
3. **429 Too Many Requests**: Rate limit exceeded, wait 1 minute
4. **500 Internal Server Error**: Database connection issue, check logs

### Debug Commands
```bash
# Check service status
curl -I $GATEWAY_URL/health
curl -I $AGENT_URL/health

# Verify SSL certificate
openssl s_client -connect bhiv-hr-gateway-46pz.onrender.com:443

# Test database connectivity
curl -H "Authorization: $API_KEY" $GATEWAY_URL/test-candidates
```

---

**Total Endpoints Tested: 53**
- Gateway Service: 48 endpoints
- Agent Service: 5 endpoints

**Expected Success Rate: 100%**
**Average Response Time: <100ms**
**Uptime Target: 99.9%**
**Security Features: Enterprise-grade (2FA, CSP, Rate limiting)**
**Last Updated: January 2025**