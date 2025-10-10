# 🔗 BHIV HR Platform - Live API Documentation

**Complete API Reference for Production Services**

## 🌐 Live Service URLs

| Service | Production URL | Status | Endpoints |
|---------|---------------|--------|-----------|
| **API Gateway** | https://bhiv-hr-gateway-46pz.onrender.com | 🟢 Online | 49 |
| **AI Agent** | https://bhiv-hr-agent-m1me.onrender.com | 🟢 Online | 6 |
| **HR Portal** | https://bhiv-hr-portal-cead.onrender.com | 🟢 Online | Web UI |
| **Client Portal** | https://bhiv-hr-client-portal-5g33.onrender.com | 🟢 Online | Web UI |

**Total API Endpoints**: 55 (All Operational)

---

## 🔑 Authentication

### Production API Key
```bash
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### Demo Client Credentials
```bash
Client ID: TECH001
Password: demo123
```

---

## 🚀 Gateway Service API (49 Endpoints)

### Core API (3 Endpoints)
```bash
GET  /                    # Service information
GET  /health             # Health check
GET  /test-candidates    # Database connectivity test
```

### Job Management (2 Endpoints)
```bash
GET  /v1/jobs           # List all jobs
POST /v1/jobs           # Create new job
```

### Candidate Management (5 Endpoints)
```bash
GET  /v1/candidates                # List all candidates
GET  /v1/candidates/{id}           # Get specific candidate
GET  /v1/candidates/search         # Search candidates
POST /v1/candidates/bulk           # Bulk upload candidates
GET  /v1/candidates/job/{job_id}   # Get candidates for job
```

### AI Matching Engine (2 Endpoints)
```bash
GET  /v1/match/{job_id}/top        # Get top AI matches
POST /v1/match/batch               # Batch AI matching
```

### Assessment & Workflow (5 Endpoints)
```bash
GET  /v1/feedback      # Get all feedback
POST /v1/feedback      # Submit values assessment
GET  /v1/interviews    # List interviews
POST /v1/interviews    # Schedule interview
GET  /v1/offers        # List job offers
POST /v1/offers        # Create job offer
```

### Analytics & Statistics (2 Endpoints)
```bash
GET  /candidates/stats                    # Candidate statistics
GET  /v1/reports/job/{job_id}/export.csv  # Export job report
```

### Client Portal API (1 Endpoint)
```bash
POST /v1/client/login  # Client authentication
```

### Security Testing (7 Endpoints)
```bash
GET  /v1/security/rate-limit-status           # Rate limit status
GET  /v1/security/blocked-ips                 # View blocked IPs
POST /v1/security/test-input-validation       # Input validation test
POST /v1/security/test-email-validation       # Email validation
POST /v1/security/test-phone-validation       # Phone validation
GET  /v1/security/security-headers-test       # Security headers test
GET  /v1/security/penetration-test-endpoints  # Penetration testing info
```

### CSP Management (4 Endpoints)
```bash
POST /v1/security/csp-report        # CSP violation reporting
GET  /v1/security/csp-violations    # View CSP violations
GET  /v1/security/csp-policies      # Current CSP policies
POST /v1/security/test-csp-policy   # Test CSP policy
```

### Two-Factor Authentication (8 Endpoints)
```bash
POST /v1/2fa/setup                          # Setup 2FA
POST /v1/2fa/verify-setup                   # Verify 2FA setup
POST /v1/2fa/login-with-2fa                 # Login with 2FA
GET  /v1/2fa/status/{client_id}             # Get 2FA status
POST /v1/2fa/disable                        # Disable 2FA
POST /v1/2fa/regenerate-backup-codes        # Regenerate backup codes
GET  /v1/2fa/test-token/{client_id}/{token} # Test 2FA token
GET  /v1/2fa/demo-setup                     # Demo 2FA setup
```

### Password Management (6 Endpoints)
```bash
POST /v1/password/validate        # Validate password strength
POST /v1/password/generate        # Generate secure password
GET  /v1/password/policy          # Password policy
POST /v1/password/change          # Change password
GET  /v1/password/strength-test   # Password strength testing tool
GET  /v1/password/security-tips   # Password security best practices
```

### Monitoring (3 Endpoints)
```bash
GET  /metrics            # Prometheus metrics
GET  /health/detailed    # Detailed health check
GET  /metrics/dashboard  # Metrics dashboard
```

---

## 🤖 AI Agent Service API (6 Endpoints)

### Core API (2 Endpoints)
```bash
GET  /         # Service information
GET  /health   # Health check
```

### AI Matching Engine (2 Endpoints)
```bash
POST /match           # AI-powered candidate matching
POST /batch-match     # Batch AI matching for multiple jobs
```

### Candidate Analysis (1 Endpoint)
```bash
GET  /analyze/{candidate_id}  # Detailed candidate analysis
```

### System Diagnostics (1 Endpoint)
```bash
GET  /test-db  # Database connectivity test
```

---

## 📊 Live System Status

### Current Metrics (Live Data)
- **Total Candidates**: 8
- **Active Jobs**: 4
- **System Uptime**: 99.9%
- **Average Response Time**: <100ms
- **Database Connections**: 5 active
- **Memory Usage**: 59.5%
- **CPU Usage**: 54.6%

### Service Health
```json
{
  "gateway": {
    "status": "healthy",
    "version": "3.1.0",
    "endpoints": 49,
    "uptime_hours": 0.22
  },
  "agent": {
    "status": "healthy", 
    "version": "2.1.0",
    "endpoints": 6
  }
}
```

---

## 🔄 Rate Limiting (Live Configuration)

### Dynamic Rate Limits
- **Default**: 60 requests/minute
- **Job Management**: 100 requests/minute  
- **Candidate Search**: 50 requests/minute
- **AI Matching**: 20 requests/minute
- **Bulk Operations**: 5 requests/minute

### Load-Based Adjustments
- **High Load (CPU >80%)**: Limits reduced by 50%
- **Low Load (CPU <30%)**: Limits increased by 50%

---

## 🧪 Live Testing Examples

### Health Check
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health
```

### Get Jobs
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

### AI Matching
```bash
curl -X POST \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}' \
  https://bhiv-hr-agent-m1me.onrender.com/match
```

### Client Login
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"client_id": "TECH001", "password": "demo123"}' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login
```

---

## 📚 Interactive Documentation

### Live Swagger UI
- **Gateway**: https://bhiv-hr-gateway-46pz.onrender.com/docs
- **AI Agent**: https://bhiv-hr-agent-m1me.onrender.com/docs

### ReDoc Format
- **Gateway**: https://bhiv-hr-gateway-46pz.onrender.com/redoc
- **AI Agent**: https://bhiv-hr-agent-m1me.onrender.com/redoc

---

## 🔧 Dependencies & Technology Stack

### Gateway Service
```
FastAPI 0.115.6
Python 3.12.7
PostgreSQL 17
Prometheus Metrics
JWT Authentication
2FA Support (TOTP)
```

### AI Agent Service  
```
FastAPI 0.115.6
Python 3.12.7
Sentence Transformers 3.0.1
Scikit-learn 1.3.2
Semantic Matching Engine
```

### Portal Services
```
Streamlit 1.41.1
Python 3.12.7
Real-time API Integration
```

---

**Last Updated**: January 2025  
**Live Status**: 🟢 All 55 Endpoints Operational  
**Verified**: October 10, 2025 14:24 UTC