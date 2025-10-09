# BHIV HR Platform - Deployment Status

## 🚀 Current Deployment Status

**Last Updated**: January 3, 2025  
**Status**: 🟢 ALL SERVICES OPERATIONAL  
**Python Version**: 3.12.7  
**Total Endpoints**: 53 (48 Gateway + 5 Agent)  
**Uptime**: 99.9%  
**Cost**: $0/month (Free tier)

---

## 📊 Service Overview

| Service | URL | Technology | Status | Endpoints | Response Time |
|---------|-----|------------|--------|-----------|---------------|
| **API Gateway** | [bhiv-hr-gateway-46pz.onrender.com](https://bhiv-hr-gateway-46pz.onrender.com/docs) | FastAPI 0.115.6 + Python 3.12.7 | 🟢 Live | 48 | <100ms |
| **AI Agent** | [bhiv-hr-agent-m1me.onrender.com](https://bhiv-hr-agent-m1me.onrender.com/docs) | FastAPI 0.115.6 + Python 3.12.7 | 🟢 Live | 5 | <50ms |
| **HR Portal** | [bhiv-hr-portal-cead.onrender.com](https://bhiv-hr-portal-cead.onrender.com/) | Streamlit 1.41.1 + Python 3.12.7 | 🟢 Live | Web UI | <200ms |
| **Client Portal** | [bhiv-hr-client-portal-5g33.onrender.com](https://bhiv-hr-client-portal-5g33.onrender.com/) | Streamlit 1.41.1 + Python 3.12.7 | 🟢 Live | Web UI | <200ms |
| **Database** | PostgreSQL 17 | PostgreSQL 17 | 🟢 Live | - | <20ms |

---

## 🔧 Gateway Service Endpoints (48 Total)

### Core API (7 endpoints)
- `GET /` - Service information
- `GET /health` - Health check
- `GET /test-candidates` - Database connectivity test
- `GET /metrics` - Prometheus metrics
- `GET /health/detailed` - Detailed health check
- `GET /metrics/dashboard` - Metrics dashboard
- `GET /candidates/stats` - Candidate statistics

### Job Management (2 endpoints)
- `GET /v1/jobs` - List all jobs
- `POST /v1/jobs` - Create new job

### Candidate Management (5 endpoints)
- `GET /v1/candidates` - List all candidates (paginated)
- `GET /v1/candidates/{id}` - Get specific candidate
- `GET /v1/candidates/search` - Search candidates with filters
- `POST /v1/candidates/bulk` - Bulk upload candidates
- `GET /v1/candidates/job/{job_id}` - Get candidates for specific job

### AI Matching (1 endpoint)
- `GET /v1/match/{job_id}/top` - Get top candidate matches for job

### Assessment & Workflow (6 endpoints)
- `GET /v1/feedback` - Get all feedback records
- `POST /v1/feedback` - Submit values assessment
- `GET /v1/interviews` - Get all interviews
- `POST /v1/interviews` - Schedule interview
- `GET /v1/offers` - Get all job offers
- `POST /v1/offers` - Create job offer

### Security Testing (7 endpoints)
- `GET /v1/security/rate-limit-status` - Check rate limit status
- `GET /v1/security/blocked-ips` - View blocked IPs
- `POST /v1/security/test-input-validation` - Test input validation
- `POST /v1/security/test-email-validation` - Test email validation
- `POST /v1/security/test-phone-validation` - Test phone validation
- `GET /v1/security/security-headers-test` - Test security headers
- `GET /v1/security/penetration-test-endpoints` - Penetration testing endpoints
- `GET /v1/security/csp-policies` - Current CSP policies
- `GET /v1/security/csp-violations` - View CSP violations
- `POST /v1/security/csp-report` - CSP violation reporting
- `POST /v1/security/test-csp-policy` - Test CSP policy

### Two-Factor Authentication (8 endpoints)
- `POST /v1/2fa/setup` - Setup 2FA for client
- `POST /v1/2fa/verify-setup` - Verify 2FA setup
- `POST /v1/2fa/login-with-2fa` - Login with 2FA
- `GET /v1/2fa/status/{client_id}` - Get 2FA status
- `POST /v1/2fa/disable` - Disable 2FA
- `POST /v1/2fa/regenerate-backup-codes` - Regenerate backup codes
- `GET /v1/2fa/test-token/{client_id}/{token}` - Test 2FA token
- `GET /v1/2fa/demo-setup` - Demo 2FA setup

### Password Management (6 endpoints)
- `POST /v1/password/validate` - Validate password strength
- `POST /v1/password/generate` - Generate secure password
- `GET /v1/password/policy` - Get password policy
- `POST /v1/password/change` - Change password
- `GET /v1/password/strength-test` - Password strength testing tool
- `GET /v1/password/security-tips` - Password security best practices

### Client Portal (1 endpoint)
- `POST /v1/client/login` - Client authentication

### Reports (1 endpoint)
- `GET /v1/reports/job/{job_id}/export.csv` - Export job report

---

## 🤖 Agent Service Endpoints (5 Total)

### Core (2 endpoints)
- `GET /` - Service information
- `GET /health` - Health check

### AI Processing (2 endpoints)
- `POST /match` - AI-powered candidate matching
- `GET /analyze/{candidate_id}` - Detailed candidate analysis

### Diagnostics (1 endpoint)
- `GET /test-db` - Database connectivity test

---

## 🔐 Authentication & Security

### API Authentication
```bash
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### Client Portal Access
```
Username: TECH001
Password: demo123
```

### Security Features
- ✅ Rate limiting (60 requests/minute)
- ✅ Two-factor authentication (TOTP)
- ✅ Password policies and validation
- ✅ Input validation (XSS/SQL injection protection)
- ✅ Security headers (CSP, XSS protection, Frame Options)
- ✅ Content Security Policy management
- ✅ Penetration testing endpoints

---

## 📈 Performance Metrics

### Response Times
- **Gateway API**: <100ms average
- **Agent AI Processing**: <50ms average
- **Database Queries**: <20ms average
- **Portal Loading**: <200ms average

### System Resources
- **CPU Usage**: <30% average
- **Memory Usage**: <60% average
- **Database Connections**: 5-10 active
- **Concurrent Users**: Multi-user support

### Availability
- **Uptime Target**: 99.9%
- **Current Uptime**: 99.9%
- **Last Downtime**: None in past 30 days
- **Auto-Recovery**: Enabled

---

## 🧪 Testing & Validation

### Endpoint Testing
```bash
# Health checks
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health

# API testing with authentication
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

### Test Suite Results
- ✅ All 53 endpoints functional
- ✅ Database connectivity verified
- ✅ Authentication working
- ✅ Rate limiting active
- ✅ Security features operational

---

## 🔄 Deployment Pipeline

### Auto-Deployment
- **Source**: GitHub repository (https://github.com/shashankmishraa/BHIV-HR-Platform)
- **Trigger**: Push to main branch
- **Platform**: Render Cloud
- **Region**: Oregon, US West
- **SSL**: Automatic HTTPS certificates
- **Database**: PostgreSQL 17 with 11 tables and 25+ indexes
- **Real Data**: 31 candidates from actual resume processing

### Recent Deployments
- **Latest**: January 3, 2025 - 53 endpoints verified (48 Gateway + 5 Agent)
- **Previous**: January 2, 2025 - Security enhancements and database consolidation
- **Database Schema**: Consolidated to 11 tables with comprehensive indexing
- **Real Data**: 31 candidates from processed resumes (30 PDF + 1 DOCX)
- **Status**: All deployments successful with 99.9% uptime

---

## 📞 Support & Monitoring

### Health Check URLs
- Gateway: https://bhiv-hr-gateway-46pz.onrender.com/health
- Agent: https://bhiv-hr-agent-m1me.onrender.com/health
- Detailed: https://bhiv-hr-gateway-46pz.onrender.com/health/detailed

### Monitoring Dashboard
- Metrics: https://bhiv-hr-gateway-46pz.onrender.com/metrics
- Dashboard: https://bhiv-hr-gateway-46pz.onrender.com/metrics/dashboard

### Documentation
- API Docs: https://bhiv-hr-gateway-46pz.onrender.com/docs
- Agent Docs: https://bhiv-hr-agent-m1me.onrender.com/docs

---

**BHIV HR Platform v3.1.0** - Enterprise recruiting solution with 53 endpoints, advanced security, and global deployment.

*Status: 🟢 All Systems Operational | Cost: $0/month | Uptime: 99.9%*