# BHIV HR Platform - Systematic Testing Guide

## 📋 Step-by-Step Testing Sequence

This guide provides a structured approach for testing all API endpoints in logical order.

### 🔧 Prerequisites
- **Base URL**: `https://bhiv-hr-gateway-46pz.onrender.com`
- **API Key**: `prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o`
- **Headers**: `Authorization: Bearer {API_KEY}`

---

## 🚀 Phase 1: System Health & Core Functionality

### Step 1.1: Basic Health Checks
```bash
# 1. Root endpoint
GET /

# 2. Basic health check
GET /health

# 3. Detailed health check
GET /health/detailed

# 4. Readiness probe
GET /health/ready

# 5. Liveness probe
GET /health/live
```

### Step 1.2: System Information
```bash
# 6. System architecture
GET /architecture

# 7. System modules
GET /system/modules

# 8. System architecture details
GET /system/architecture
```

### Step 1.3: Monitoring & Metrics
```bash
# 9. Prometheus metrics
GET /metrics

# 10. JSON metrics
GET /metrics/json

# 11. Health probe (bypasses rate limits)
GET /health/probe
```

---

## 🔐 Phase 2: Authentication & Security

### Step 2.1: Authentication Endpoints
```bash
# 12. Login
POST /auth/login
{
  "username": "TECH001",
  "password": "demo123"
}

# 13. Token validation
POST /auth/validate-token
{
  "token": "{jwt_token}"
}

# 14. Refresh token
POST /auth/refresh
{
  "refresh_token": "{refresh_token}"
}
```

### Step 2.2: API Key Management
```bash
# 15. Generate API key
POST /auth/api-keys/generate
{
  "name": "test_key",
  "permissions": ["read", "write"]
}

# 16. List API keys
GET /auth/api-keys

# 17. Validate API key
POST /auth/api-keys/validate
{
  "api_key": "{api_key}"
}

# 18. Revoke API key
DELETE /auth/api-keys/{key_id}
```

### Step 2.3: User Management
```bash
# 19. Get current user
GET /auth/me

# 20. Update user profile
PUT /auth/me
{
  "name": "Updated Name",
  "email": "updated@example.com"
}

# 21. Change password
POST /auth/change-password
{
  "current_password": "old_pass",
  "new_password": "new_pass"
}
```

---

## 👥 Phase 3: Candidate Management

### Step 3.1: Basic Candidate Operations
```bash
# 22. List all candidates
GET /candidates

# 23. Get candidate by ID
GET /candidates/{candidate_id}

# 24. Create new candidate
POST /candidates
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "skills": ["Python", "FastAPI"]
}

# 25. Update candidate
PUT /candidates/{candidate_id}
{
  "name": "John Updated",
  "skills": ["Python", "FastAPI", "PostgreSQL"]
}

# 26. Delete candidate
DELETE /candidates/{candidate_id}
```

### Step 3.2: Candidate Search & Filtering
```bash
# 27. Search candidates by skills
GET /candidates/search?skills=Python,FastAPI

# 28. Filter candidates by experience
GET /candidates/filter?min_experience=2&max_experience=5

# 29. Get candidates by status
GET /candidates/status/{status}

# 30. Advanced candidate search
POST /candidates/advanced-search
{
  "skills": ["Python"],
  "experience_range": [2, 5],
  "location": "Remote"
}
```

### Step 3.3: Candidate Analytics
```bash
# 31. Candidate statistics
GET /candidates/stats

# 32. Skill distribution
GET /candidates/skills/distribution

# 33. Candidate performance metrics
GET /candidates/{candidate_id}/metrics
```

---

## 💼 Phase 4: Job Management

### Step 4.1: Basic Job Operations
```bash
# 34. List all jobs
GET /jobs

# 35. Get job by ID
GET /jobs/{job_id}

# 36. Create new job
POST /jobs
{
  "title": "Senior Python Developer",
  "description": "Looking for experienced Python developer",
  "requirements": ["Python", "FastAPI", "PostgreSQL"],
  "salary_range": [80000, 120000]
}

# 37. Update job
PUT /jobs/{job_id}
{
  "title": "Senior Python Developer - Updated",
  "salary_range": [85000, 125000]
}

# 38. Delete job
DELETE /jobs/{job_id}
```

### Step 4.2: Job Search & Matching
```bash
# 39. Search jobs by title
GET /jobs/search?title=Python

# 40. Filter jobs by salary
GET /jobs/filter?min_salary=80000&max_salary=120000

# 41. Get jobs by status
GET /jobs/status/{status}

# 42. AI-powered job matching
POST /jobs/{job_id}/match-candidates
{
  "limit": 10,
  "min_score": 0.7
}
```

### Step 4.3: Job Analytics
```bash
# 43. Job statistics
GET /jobs/stats

# 44. Popular skills analysis
GET /jobs/skills/popular

# 45. Job performance metrics
GET /jobs/{job_id}/metrics
```

---

## 🔄 Phase 5: Workflow Management

### Step 5.1: Workflow Operations
```bash
# 46. List all workflows
GET /workflows

# 47. Get workflow by ID
GET /workflows/{workflow_id}

# 48. Create workflow
POST /workflows
{
  "name": "Candidate Onboarding",
  "type": "candidate_onboarding",
  "steps": ["verification", "profile_setup", "notification"]
}

# 49. Start workflow
POST /workflows/{workflow_id}/start

# 50. Stop workflow
POST /workflows/{workflow_id}/stop
```

### Step 5.2: Workflow Monitoring
```bash
# 51. Get workflow status
GET /workflows/{workflow_id}/status

# 52. Get workflow history
GET /workflows/{workflow_id}/history

# 53. Workflow statistics
GET /workflows/stats

# 54. Active workflows
GET /workflows/active
```

### Step 5.3: Pipeline Management
```bash
# 55. List pipelines
GET /workflows/pipelines

# 56. Create pipeline
POST /workflows/pipelines
{
  "name": "Hiring Pipeline",
  "stages": ["application", "screening", "interview", "offer"]
}

# 57. Execute pipeline
POST /workflows/pipelines/{pipeline_id}/execute
```

---

## 📊 Phase 6: Advanced Monitoring & Analytics

### Step 6.1: System Monitoring
```bash
# 58. System status
GET /monitoring/status

# 59. Performance metrics
GET /monitoring/performance

# 60. Error logs
GET /monitoring/errors

# 61. Audit logs
GET /monitoring/audit
```

### Step 6.2: Real-time Analytics
```bash
# 62. Live metrics
GET /monitoring/live-metrics

# 63. Dashboard data
GET /monitoring/dashboard

# 64. Alert status
GET /monitoring/alerts

# 65. System resources
GET /monitoring/resources
```

### Step 6.3: Reporting
```bash
# 66. Generate report
POST /monitoring/reports
{
  "type": "performance",
  "period": "last_7_days"
}

# 67. Export metrics
GET /monitoring/export?format=json&period=last_24_hours

# 68. Health summary
GET /monitoring/health-summary
```

---

## 🧪 Phase 7: Integration Testing

### Step 7.1: Cross-Module Integration
```bash
# 69. End-to-end candidate flow
POST /candidates (create) → GET /jobs/{job_id}/match-candidates → POST /workflows (start onboarding)

# 70. Job posting workflow
POST /jobs (create) → POST /workflows (job_posting_workflow) → GET /monitoring/status

# 71. Authentication flow
POST /auth/login → GET /auth/me → POST /candidates (with auth)
```

### Step 7.2: Error Handling
```bash
# 72. Invalid endpoints
GET /invalid-endpoint (should return 404)

# 73. Malformed requests
POST /candidates with invalid JSON (should return 422)

# 74. Unauthorized access
GET /candidates without auth header (should return 401)
```

### Step 7.3: Performance Testing
```bash
# 75. Concurrent requests
Multiple simultaneous GET /health requests

# 76. Large payload handling
POST /candidates with large data

# 77. Rate limiting
Multiple rapid requests to test rate limits
```

---

## ✅ Testing Checklist

### Phase 1: System Health ✓
- [ ] All health endpoints respond
- [ ] System information accessible
- [ ] Metrics collection working

### Phase 2: Authentication ✓
- [ ] Login/logout functionality
- [ ] API key management
- [ ] User profile operations

### Phase 3: Candidates ✓
- [ ] CRUD operations
- [ ] Search and filtering
- [ ] Analytics and reporting

### Phase 4: Jobs ✓
- [ ] Job management
- [ ] AI matching functionality
- [ ] Performance metrics

### Phase 5: Workflows ✓
- [ ] Workflow creation and execution
- [ ] Pipeline management
- [ ] Status monitoring

### Phase 6: Monitoring ✓
- [ ] Real-time monitoring
- [ ] Analytics dashboard
- [ ] Error tracking

### Phase 7: Integration ✓
- [ ] Cross-module functionality
- [ ] Error handling
- [ ] Performance validation

---

## 📝 Test Results Template

```json
{
  "test_session": {
    "date": "2025-01-XX",
    "tester": "Your Name",
    "environment": "production",
    "base_url": "https://bhiv-hr-gateway-46pz.onrender.com"
  },
  "results": {
    "phase_1_health": {
      "total_endpoints": 11,
      "passed": 0,
      "failed": 0,
      "notes": ""
    },
    "phase_2_auth": {
      "total_endpoints": 10,
      "passed": 0,
      "failed": 0,
      "notes": ""
    },
    "phase_3_candidates": {
      "total_endpoints": 12,
      "passed": 0,
      "failed": 0,
      "notes": ""
    },
    "phase_4_jobs": {
      "total_endpoints": 12,
      "passed": 0,
      "failed": 0,
      "notes": ""
    },
    "phase_5_workflows": {
      "total_endpoints": 13,
      "passed": 0,
      "failed": 0,
      "notes": ""
    },
    "phase_6_monitoring": {
      "total_endpoints": 11,
      "passed": 0,
      "failed": 0,
      "notes": ""
    },
    "phase_7_integration": {
      "total_endpoints": 9,
      "passed": 0,
      "failed": 0,
      "notes": ""
    }
  },
  "summary": {
    "total_endpoints_tested": 78,
    "overall_pass_rate": "0%",
    "critical_issues": [],
    "recommendations": []
  }
}
```

---

## 🚀 Quick Start Commands

```bash
# Test basic functionality
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health

# Test authentication
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"TECH001","password":"demo123"}'

# Test candidate creation
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/candidates \
     -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test User","email":"test@example.com","skills":["Python"]}'
```

This systematic approach ensures comprehensive testing of all 180+ endpoints in a logical, step-by-step manner.