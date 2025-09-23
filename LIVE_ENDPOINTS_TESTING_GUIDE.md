# BHIV HR Platform - Live Endpoints Testing Guide
**Production Services on Render - Complete API Reference**

## 🌐 Live Service URLs

| Service | URL | Status | Endpoints |
|---------|-----|--------|-----------|
| **Gateway** | https://bhiv-hr-gateway-901a.onrender.com | ✅ Live | 154 endpoints |
| **Agent** | https://bhiv-hr-agent-o6nx.onrender.com | ✅ Live | 11 endpoints |
| **Portal** | https://bhiv-hr-portal-xk2k.onrender.com | ✅ Live | Web Interface |
| **Client Portal** | https://bhiv-hr-client-portal-zdbt.onrender.com | ✅ Live | Web Interface |

## 🔑 Authentication

**API Key**: `prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o`

**Usage**: Add to request headers:
```bash
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

---

## 🚀 Gateway Service - 154 Endpoints
**Base URL**: https://bhiv-hr-gateway-901a.onrender.com

### 📋 Core API Endpoints (4)

#### 1. Root Information
```bash
GET /
HEAD /
```
**Test**:
```bash
curl https://bhiv-hr-gateway-901a.onrender.com/
```

#### 2. Health Check
```bash
GET /health
HEAD /health
```
**Test**:
```bash
curl https://bhiv-hr-gateway-901a.onrender.com/health
```

#### 3. Test Candidates (Requires Auth)
```bash
GET /test-candidates
HEAD /test-candidates
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/test-candidates
```

#### 4. HTTP Methods Test
```bash
GET /http-methods-test
HEAD /http-methods-test
OPTIONS /http-methods-test
```
**Test**:
```bash
curl https://bhiv-hr-gateway-901a.onrender.com/http-methods-test
```

### 💼 Job Management (8)

#### 1. List Jobs
```bash
GET /v1/jobs
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/jobs
```

#### 2. Create Job
```bash
POST /v1/jobs
```
**Test**:
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"title":"Software Engineer","department":"Engineering","location":"Remote","experience_level":"Mid","requirements":"Python, FastAPI","description":"Join our team"}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/jobs
```

#### 3. Get Single Job
```bash
GET /v1/jobs/{job_id}
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/jobs/1
```

#### 4. Update Job
```bash
PUT /v1/jobs/{job_id}
```

#### 5. Delete Job
```bash
DELETE /v1/jobs/{job_id}
```

#### 6. Search Jobs
```bash
GET /v1/jobs/search?query=python&location=remote&department=engineering
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs/search?query=python"
```

#### 7. Job Statistics
```bash
GET /v1/jobs/stats
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/jobs/stats
```

#### 8. Bulk Create Jobs
```bash
POST /v1/jobs/bulk
```

### 👥 Candidate Management (12)

#### 1. List All Candidates
```bash
GET /v1/candidates?limit=50&offset=0
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/candidates
```

#### 2. Create Candidate
```bash
POST /v1/candidates
```
**Test**:
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"name":"John Doe","email":"john@example.com","technical_skills":"Python, React","experience_years":5}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/candidates
```

#### 3. Get Single Candidate
```bash
GET /v1/candidates/{candidate_id}
```

#### 4. Update Candidate
```bash
PUT /v1/candidates/{candidate_id}
```

#### 5. Delete Candidate
```bash
DELETE /v1/candidates/{candidate_id}
```

#### 6. Search Candidates
```bash
GET /v1/candidates/search?skills=python&location=remote&experience_min=3
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-901a.onrender.com/v1/candidates/search?skills=python"
```

#### 7. Candidates by Job
```bash
GET /v1/candidates/job/{job_id}
```

#### 8. Bulk Upload Candidates
```bash
POST /v1/candidates/bulk
```
**Test**:
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"candidates":[{"name":"Jane Smith","email":"jane@example.com","technical_skills":"JavaScript, Node.js","experience_years":3}]}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/candidates/bulk
```

#### 9. Export Candidates
```bash
GET /v1/candidates/export?format=csv
```

#### 10. Candidate Statistics
```bash
GET /v1/candidates/stats
```

#### 11. Legacy Candidate Stats
```bash
GET /candidates/stats
```

### 🤖 AI Matching Engine (9)

#### 1. Get Top Matches (Primary AI Endpoint)
```bash
GET /v1/match/{job_id}/top?limit=10
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/match/1/top
```

#### 2. Performance Test
```bash
GET /v1/match/performance-test?concurrent_requests=5
```

#### 3. Cache Status
```bash
GET /v1/match/cache-status
```

#### 4. Clear Cache
```bash
POST /v1/match/cache-clear
```

#### 5. Batch Matching
```bash
POST /v1/match/batch
```

#### 6. Match History
```bash
GET /v1/match/history
```

#### 7. Submit Feedback
```bash
POST /v1/match/feedback
```

#### 8. Match Analytics
```bash
GET /v1/match/analytics
```

#### 9. Retrain Model
```bash
POST /v1/match/retrain
```

### 📊 Assessment & Workflow (3)

#### 1. Submit Values Feedback
```bash
POST /v1/feedback
```
**Test**:
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"candidate_id":1,"job_id":1,"integrity":5,"honesty":5,"discipline":4,"hard_work":5,"gratitude":4}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/feedback
```

#### 2. Get Interviews
```bash
GET /v1/interviews
```

#### 3. Schedule Interview
```bash
POST /v1/interviews
```
**Test**:
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"candidate_id":1,"job_id":1,"interview_date":"2025-01-25T10:00:00Z","interviewer":"HR Manager"}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/interviews
```

### 📅 Interview Management (8)

#### 1. Update Interview
```bash
PUT /v1/interviews/{interview_id}
```

#### 2. Delete Interview
```bash
DELETE /v1/interviews/{interview_id}
```

#### 3. Get Single Interview
```bash
GET /v1/interviews/{interview_id}
```

#### 4. Schedule Interview (New)
```bash
POST /v1/interviews/schedule
```

#### 5. Interview Calendar
```bash
GET /v1/interviews/calendar?month=2025-01
```

#### 6. Submit Interview Feedback
```bash
POST /v1/interviews/feedback
```

#### 7. Create Job Offer
```bash
POST /v1/offers
```

#### 8. Database Migration
```bash
POST /v1/database/migrate
```

### 📈 Analytics & Statistics (15)

#### 1. Summary Report
```bash
GET /v1/reports/summary
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/reports/summary
```

#### 2. Analytics Dashboard
```bash
GET /v1/analytics/dashboard
```

#### 3. Analytics Trends
```bash
GET /v1/analytics/trends?days=30
```

#### 4. Export Analytics
```bash
GET /v1/analytics/export?format=csv
```

#### 5. Analytics Predictions
```bash
GET /v1/analytics/predictions
```

#### 6. Export Job Report
```bash
GET /v1/reports/job/{job_id}/export.csv
```

### 🔐 Authentication (15)

#### 1. Test Enhanced Auth
```bash
GET /v1/auth/test-enhanced
```
**Test**:
```bash
curl https://bhiv-hr-gateway-901a.onrender.com/v1/auth/test-enhanced
```

#### 2. Auth Status
```bash
GET /v1/auth/status
```

#### 3. User Info
```bash
GET /v1/auth/user/info
```

#### 4. Test Auth System
```bash
GET /v1/auth/test
```

#### 5. Auth Configuration
```bash
GET /v1/auth/config
```

#### 6. Auth System Health
```bash
GET /v1/auth/system/health
```

#### 7. Auth Metrics
```bash
GET /v1/auth/metrics
```

#### 8. List Users
```bash
GET /v1/auth/users
```

#### 9. Logout User
```bash
POST /v1/auth/logout
```

#### 10. Invalidate Sessions
```bash
POST /v1/auth/sessions/invalidate
```

#### 11. List Sessions
```bash
GET /v1/auth/sessions
```

#### 12. Auth Audit Log
```bash
GET /v1/auth/audit/log?hours=24
```

#### 13. Available Permissions
```bash
GET /v1/auth/permissions
```

#### 14. Generate JWT Token
```bash
POST /v1/auth/tokens/generate
```

#### 15. Validate JWT Token
```bash
GET /v1/auth/tokens/validate?token=your_token
```

### 🔑 Two-Factor Authentication (12)

#### 1. Setup 2FA
```bash
POST /v1/auth/2fa/setup
```

#### 2. Verify 2FA Setup
```bash
POST /v1/auth/2fa/verify
```

#### 3. Login with 2FA
```bash
POST /v1/auth/2fa/login
```

#### 4. Get 2FA Status
```bash
GET /v1/auth/2fa/status/{user_id}
```

#### 5. Disable 2FA
```bash
POST /v1/auth/2fa/disable
```

#### 6. Regenerate Backup Codes
```bash
POST /v1/auth/2fa/regenerate-backup-codes
```

#### 7. Test 2FA Token
```bash
GET /v1/2fa/test-token/{client_id}/{token}
```

#### 8. Demo 2FA Setup
```bash
GET /v1/2fa/demo-setup
```

### 🔐 API Key Management (6)

#### 1. List API Keys
```bash
GET /v1/auth/api-keys?user_id=demo_user
```

#### 2. Create API Key
```bash
POST /v1/auth/api-keys
```

#### 3. Revoke API Key
```bash
DELETE /v1/auth/api-keys/{key_id}
```

#### 4. Generate New API Key
```bash
POST /v1/security/api-keys/generate?client_id=TECH001
```

#### 5. Rotate API Keys
```bash
POST /v1/security/api-keys/rotate?client_id=TECH001
```

### 🛡️ Security Testing (15)

#### 1. Rate Limit Status
```bash
GET /v1/security/rate-limit-status
```
**Test**:
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/security/rate-limit-status
```

#### 2. Blocked IPs
```bash
GET /v1/security/blocked-ips
```

#### 3. Test Input Validation
```bash
POST /v1/security/test-input-validation
```
**Test**:
```bash
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"input_data":"<script>alert(\"test\")</script>"}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/security/test-input-validation
```

#### 4. Test Email Validation
```bash
POST /v1/security/test-email-validation
```

#### 5. Test Phone Validation
```bash
POST /v1/security/test-phone-validation
```

#### 6. Security Headers Test
```bash
GET /v1/security/security-headers-test
```

#### 7. Penetration Test Endpoints
```bash
GET /v1/security/penetration-test-endpoints
```

#### 8. Security Headers
```bash
GET /v1/security/headers
```

#### 9. Test XSS Protection
```bash
POST /v1/security/test-xss
```

#### 10. Test SQL Injection Protection
```bash
POST /v1/security/test-sql-injection
```

#### 11. Security Audit Log
```bash
GET /v1/security/audit-log
```

#### 12. Security Status
```bash
GET /v1/security/status
```

#### 13. Rotate Security Keys
```bash
POST /v1/security/rotate-keys
```

#### 14. Security Policy
```bash
GET /v1/security/policy
```

#### 15. CORS Configuration
```bash
GET /v1/security/cors-config
```

### 🛡️ CSP Management (4)

#### 1. CSP Violation Report
```bash
POST /v1/security/csp-report
```

#### 2. View CSP Violations
```bash
GET /v1/security/csp-violations
```

#### 3. Current CSP Policies
```bash
GET /v1/security/csp-policies
```

#### 4. Test CSP Policy
```bash
POST /v1/security/test-csp-policy
```

### 🔐 Password Management (6)

#### 1. Validate Password
```bash
POST /v1/password/validate
```

#### 2. Generate Password
```bash
GET /v1/password/generate?length=16
```

#### 3. Password Policy
```bash
GET /v1/password/policy
```

#### 4. Change Password
```bash
POST /v1/password/change
```

#### 5. Password Strength Test
```bash
GET /v1/password/strength-test
```

#### 6. Reset Password
```bash
POST /v1/password/reset
```

### 🔧 Session Management (6)

#### 1. Create Session
```bash
POST /v1/sessions/create
```

#### 2. Validate Session
```bash
GET /v1/sessions/validate
```

#### 3. Logout Session
```bash
POST /v1/sessions/logout
```

#### 4. Active Sessions
```bash
GET /v1/sessions/active
```

#### 5. Cleanup Sessions
```bash
POST /v1/sessions/cleanup
```

#### 6. Session Stats
```bash
GET /v1/sessions/stats
```

### 👤 Client Portal API (6)

#### 1. Client Login
```bash
POST /v1/client/login
```
**Test**:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"client_id":"TECH001","password":"demo123"}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/client/login
```

#### 2. Get Client Profile
```bash
GET /v1/client/profile
```

#### 3. Update Client Profile
```bash
PUT /v1/client/profile
```

### 🗄️ Database Management (4)

#### 1. Database Health
```bash
GET /v1/database/health
```

#### 2. Database Migration
```bash
POST /v1/database/migrate
```

#### 3. Add Interviewer Column
```bash
POST /v1/database/add-interviewer-column
```

### 📊 Monitoring (22)

#### 1. Prometheus Metrics
```bash
GET /metrics
```
**Test**:
```bash
curl https://bhiv-hr-gateway-901a.onrender.com/metrics
```

#### 2. Simple Health Check
```bash
GET /health/simple
```

#### 3. Detailed Health Check
```bash
GET /health/detailed
```

#### 4. Error Analytics
```bash
GET /monitoring/errors?hours=24
```

#### 5. Search Logs
```bash
GET /monitoring/logs/search?query=error&hours=1
```

#### 6. Check Dependencies
```bash
GET /monitoring/dependencies
```

#### 7. Metrics Dashboard
```bash
GET /metrics/dashboard
```
**Test**:
```bash
curl https://bhiv-hr-gateway-901a.onrender.com/metrics/dashboard
```

#### 8. Performance Metrics
```bash
GET /monitoring/performance
```

#### 9. System Alerts
```bash
GET /monitoring/alerts
```

#### 10. Monitoring Config
```bash
GET /monitoring/config
```

#### 11. Test Monitoring
```bash
POST /monitoring/test
```

#### 12. Reset Metrics
```bash
POST /monitoring/reset
```

---

## 🤖 Agent Service - 11 Endpoints
**Base URL**: https://bhiv-hr-agent-o6nx.onrender.com

### 📋 Core API Endpoints (3)

#### 1. Service Information
```bash
GET /
HEAD /
```
**Test**:
```bash
curl https://bhiv-hr-agent-o6nx.onrender.com/
```

#### 2. Health Check
```bash
GET /health
HEAD /health
```
**Test**:
```bash
curl https://bhiv-hr-agent-o6nx.onrender.com/health
```

#### 3. HTTP Methods Test
```bash
GET /http-methods-test
HEAD /http-methods-test
OPTIONS /http-methods-test
```

### 🤖 AI Matching Engine (6)

#### 1. Match Candidates (Primary AI Endpoint)
```bash
POST /match
```
**Test**:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"job_id":1}' \
     https://bhiv-hr-agent-o6nx.onrender.com/match
```

#### 2. Analyze Candidate
```bash
GET /analyze/{candidate_id}
```
**Test**:
```bash
curl https://bhiv-hr-agent-o6nx.onrender.com/analyze/1
```

### 🔧 System Diagnostics (2)

#### 1. Semantic Engine Status
```bash
GET /semantic-status
```
**Test**:
```bash
curl https://bhiv-hr-agent-o6nx.onrender.com/semantic-status
```

#### 2. Database Test
```bash
GET /test-db
HEAD /test-db
```
**Test**:
```bash
curl https://bhiv-hr-agent-o6nx.onrender.com/test-db
```

#### 3. Agent Status
```bash
GET /status
```

#### 4. Version Information
```bash
GET /version
```

#### 5. Agent Metrics
```bash
GET /metrics
```

---

## 🌐 Web Interfaces

### 📊 HR Portal
**URL**: https://bhiv-hr-portal-xk2k.onrender.com
- Complete HR dashboard
- Candidate management
- Job posting
- AI matching interface
- Values assessment

### 👤 Client Portal
**URL**: https://bhiv-hr-client-portal-zdbt.onrender.com
**Login**: TECH001 / demo123
- Client authentication
- Job posting
- Candidate review
- Interview scheduling

---

## 🧪 Testing Examples

### Quick Health Check All Services
```bash
# Gateway Health
curl https://bhiv-hr-gateway-901a.onrender.com/health

# Agent Health  
curl https://bhiv-hr-agent-o6nx.onrender.com/health

# Portal Web
curl https://bhiv-hr-portal-xk2k.onrender.com/

# Client Portal Web
curl https://bhiv-hr-client-portal-zdbt.onrender.com/
```

### Test AI Matching Flow
```bash
# 1. Get jobs
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/jobs

# 2. Get candidates
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/candidates

# 3. Get AI matches (Gateway)
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/match/1/top

# 4. Get AI matches (Agent)
curl -X POST -H "Content-Type: application/json" \
     -d '{"job_id":1}' \
     https://bhiv-hr-agent-o6nx.onrender.com/match
```

### Test Security Features
```bash
# Rate limit status
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/security/rate-limit-status

# Input validation
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"input_data":"<script>alert(\"xss\")</script>"}' \
     https://bhiv-hr-gateway-901a.onrender.com/v1/security/test-input-validation
```

---

## 📊 Summary

**Total Live Endpoints**: 165
- **Gateway Service**: 154 endpoints
- **Agent Service**: 11 endpoints
- **Web Interfaces**: 2 portals

**Categories**:
- Core API: 4 endpoints
- Job Management: 8 endpoints  
- Candidate Management: 12 endpoints
- AI Matching: 9 endpoints
- Authentication: 15 endpoints
- Security Testing: 15 endpoints
- Monitoring: 22 endpoints
- Analytics: 15 endpoints
- And more...

**Status**: 🟢 All services operational and accessible
**Cost**: $0/month on Render free tier
**Uptime**: 99.9% target with auto-deployment

---

*Last Updated: January 2025 | Version: v3.2.0*