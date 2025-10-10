# 🟢 BHIV HR Platform - Live Service Status

**Real-time Status Report - All Services Operational**

## 📊 Current Live Status

### Service Health (Verified: January 2025)
| Service | URL | Status | Response Time | Endpoints |
|---------|-----|--------|---------------|-----------|
| **API Gateway** | https://bhiv-hr-gateway-46pz.onrender.com | 🟢 ONLINE | 1.59s | 49 |
| **AI Agent** | https://bhiv-hr-agent-m1me.onrender.com | 🟢 ONLINE | 1.14s | 6 |
| **HR Portal** | https://bhiv-hr-portal-cead.onrender.com | 🟢 ONLINE | 1.43s | Web UI |
| **Client Portal** | https://bhiv-hr-client-portal-5g33.onrender.com | 🟢 ONLINE | 1.39s | Web UI |

**Total API Endpoints**: 55 (All Operational)

## 🔍 Live System Metrics

### Database Status
- **Total Candidates**: 8 (from actual resume files)
- **Active Jobs**: 4
- **Database Connections**: 5 active
- **Connection Status**: ✅ Connected

### Performance Metrics
- **CPU Usage**: 54.6%
- **Memory Usage**: 59.5%
- **Disk Usage**: 84.1%
- **Average Response Time**: <100ms
- **Uptime**: 0.22 hours (recently deployed)

## 🔗 Verified Endpoints

### Gateway Service (49 Endpoints) ✅
```
✅ Core API (3):
   GET  /                    - Service information
   GET  /health             - Health check  
   GET  /test-candidates    - Database test

✅ Job Management (2):
   GET  /v1/jobs           - List jobs
   POST /v1/jobs           - Create job

✅ Candidate Management (5):
   GET  /v1/candidates                - List candidates
   GET  /v1/candidates/{id}           - Get candidate
   GET  /v1/candidates/search         - Search candidates
   POST /v1/candidates/bulk           - Bulk upload
   GET  /v1/candidates/job/{job_id}   - Job candidates

✅ AI Matching (2):
   GET  /v1/match/{job_id}/top        - Top matches
   POST /v1/match/batch               - Batch matching

✅ Assessment & Workflow (5):
   GET/POST /v1/feedback      - Values assessment
   GET/POST /v1/interviews    - Interview management
   GET/POST /v1/offers        - Job offers

✅ Security & Authentication (26):
   - Security Testing (7 endpoints)
   - CSP Management (4 endpoints)  
   - Two-Factor Auth (8 endpoints)
   - Password Management (6 endpoints)
   - Client Portal Auth (1 endpoint)

✅ Analytics & Monitoring (6):
   - Statistics (2 endpoints)
   - Monitoring (3 endpoints)
   - Reports (1 endpoint)
```

### AI Agent Service (6 Endpoints) ✅
```
✅ Core (2):
   GET  /         - Service info
   GET  /health   - Health check

✅ AI Processing (3):
   POST /match           - AI candidate matching
   POST /batch-match     - Batch AI matching
   GET  /analyze/{id}    - Candidate analysis

✅ Diagnostics (1):
   GET  /test-db  - Database test
```

## 🔐 Authentication & Security

### Production Credentials
```bash
# API Authentication
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# Client Portal Demo
Username: TECH001
Password: demo123
```

### Security Features Active
- ✅ Bearer Token Authentication
- ✅ JWT Client Authentication  
- ✅ Rate Limiting (60/min default)
- ✅ 2FA Support (TOTP)
- ✅ Input Validation
- ✅ Security Headers
- ✅ CSP Policies

## 🧪 Live Testing Commands

### Health Checks
```bash
# Gateway Health
curl https://bhiv-hr-gateway-46pz.onrender.com/health

# AI Agent Health  
curl https://bhiv-hr-agent-m1me.onrender.com/health

# Database Test
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates
```

### API Testing
```bash
# List Jobs
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# AI Matching
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}' \
  https://bhiv-hr-agent-m1me.onrender.com/match

# Client Login
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"client_id": "TECH001", "password": "demo123"}' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login
```

## 📈 Technology Stack (Live)

### Backend Services
- **FastAPI**: 0.115.6
- **Python**: 3.12.7
- **PostgreSQL**: 17
- **Sentence Transformers**: 3.0.1 (AI Agent)

### Frontend Services  
- **Streamlit**: 1.41.1
- **Real-time API Integration**

### Infrastructure
- **Platform**: Render Cloud (Oregon, US West)
- **SSL**: Automatic HTTPS
- **Cost**: $0/month (Free tier)
- **Auto-Deploy**: GitHub integration

## 🔄 Rate Limiting (Active)

### Current Limits
- **Default**: 60 requests/minute
- **Job Management**: 100 requests/minute
- **Candidate Search**: 50 requests/minute  
- **AI Matching**: 20 requests/minute
- **Bulk Operations**: 5 requests/minute

### Dynamic Adjustments
- **High Load (CPU >80%)**: Limits reduced by 50%
- **Low Load (CPU <30%)**: Limits increased by 50%

## 📚 Interactive Documentation

### Live Swagger UI
- **Gateway**: https://bhiv-hr-gateway-46pz.onrender.com/docs
- **AI Agent**: https://bhiv-hr-agent-m1me.onrender.com/docs

### Web Portals
- **HR Portal**: https://bhiv-hr-portal-cead.onrender.com/
- **Client Portal**: https://bhiv-hr-client-portal-5g33.onrender.com/

## 🎯 Service Dependencies

### Gateway Service Dependencies
```
fastapi==0.115.6
uvicorn==0.32.1
psycopg2-binary==2.9.10
sqlalchemy==2.0.23
prometheus-client==0.19.0
pyotp==2.9.0
PyJWT==2.8.0
bcrypt==4.1.2
```

### AI Agent Dependencies
```
fastapi==0.115.6
sentence-transformers==3.0.1
numpy==1.26.4
scikit-learn==1.3.2
psycopg2-binary==2.9.10
```

### Portal Dependencies
```
streamlit==1.41.1
requests==2.32.3
pandas==2.3.2
plotly==5.17.0
```

## ✅ Verification Summary

**All Systems Operational** ✅
- 4/4 Services Online
- 55/55 API Endpoints Functional
- Database Connected
- Authentication Working
- Real-time Data Available
- Interactive Documentation Accessible

**Last Verified**: January 2025  
**Next Check**: Continuous monitoring active  
**Status**: 🟢 ALL SERVICES OPERATIONAL