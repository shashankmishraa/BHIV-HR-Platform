# 🔧 BHIV HR Platform - Services Guide

## 🏗️ Microservices Architecture Overview

The BHIV HR Platform consists of 5 core microservices, each with specific responsibilities and clear interfaces.

## 🌐 Gateway Service (Port 8000)

### 📍 Location: `/services/gateway/`
### 🎯 Purpose: Central API hub and request routing

#### Key Files:
- `app/main.py` - Main FastAPI application with 48 endpoints
- `client_auth.py` - Client authentication utilities
- `app/db/schemas.py` - Pydantic models for validation

#### API Endpoints (50 total):
```
Core API (7 endpoints):
├── GET  /           - Service information
├── GET  /health     - Health check
├── GET  /test-candidates - Database connectivity test
├── GET  /metrics    - Prometheus metrics
├── GET  /health/detailed - Detailed health check
├── GET  /metrics/dashboard - Metrics dashboard
└── GET  /candidates/stats - Candidate statistics

Job Management (2 endpoints):
├── GET  /v1/jobs    - List all jobs
└── POST /v1/jobs    - Create new job

Candidate Management (5 endpoints):
├── GET  /v1/candidates - List all candidates (paginated)
├── GET  /v1/candidates/{id} - Get specific candidate
├── GET  /v1/candidates/search - Search candidates with filters
├── POST /v1/candidates/bulk - Bulk upload candidates
└── GET  /v1/candidates/job/{job_id} - Get candidates for specific job

AI Matching (1 endpoint):
└── GET  /v1/match/{job_id}/top - Get top candidate matches for job

Assessment & Workflow (6 endpoints):
├── GET  /v1/feedback - Get all feedback records
├── POST /v1/feedback - Submit values assessment
├── GET  /v1/interviews - Get all interviews
├── POST /v1/interviews - Schedule interview
├── GET  /v1/offers - Get all job offers
└── POST /v1/offers - Create job offer

Security Testing (11 endpoints):
├── GET  /v1/security/rate-limit-status - Check rate limit status
├── GET  /v1/security/blocked-ips - View blocked IPs
├── POST /v1/security/test-input-validation - Test input validation
├── POST /v1/security/test-email-validation - Test email validation
├── POST /v1/security/test-phone-validation - Test phone validation
├── GET  /v1/security/security-headers-test - Test security headers
├── GET  /v1/security/penetration-test-endpoints - Penetration testing endpoints
├── GET  /v1/security/csp-policies - Current CSP policies
├── GET  /v1/security/csp-violations - View CSP violations
├── POST /v1/security/csp-report - CSP violation reporting
└── POST /v1/security/test-csp-policy - Test CSP policy

Two-Factor Authentication (8 endpoints):
├── POST /v1/2fa/setup - Setup 2FA for client
├── POST /v1/2fa/verify-setup - Verify 2FA setup
├── POST /v1/2fa/login-with-2fa - Login with 2FA
├── GET  /v1/2fa/status/{client_id} - Get 2FA status
├── POST /v1/2fa/disable - Disable 2FA
├── POST /v1/2fa/regenerate-backup-codes - Regenerate backup codes
├── GET  /v1/2fa/test-token/{client_id}/{token} - Test 2FA token
└── GET  /v1/2fa/demo-setup - Demo 2FA setup

Password Management (6 endpoints):
├── POST /v1/password/validate - Validate password strength
├── POST /v1/password/generate - Generate secure password
├── GET  /v1/password/policy - Get password policy
├── POST /v1/password/change - Change password
├── GET  /v1/password/strength-test - Password strength testing tool
└── GET  /v1/password/security-tips - Password security best practices

Client Portal (1 endpoint):
└── POST /v1/client/login - Client authentication

Reports (1 endpoint):
└── GET  /v1/reports/job/{job_id}/export.csv - Export job report
```

#### Dependencies:
- FastAPI 0.115.6
- SQLAlchemy 2.0.36
- psycopg2-binary 2.9.10
- Pydantic 2.10.3

## 🤖 Agent Service (Port 9000)

### 📍 Location: `/services/agent/`
### 🎯 Purpose: AI-powered candidate matching and semantic analysis

#### Key Files:
- `app.py` - AI matching algorithms and endpoints

#### Features:
- Semantic candidate matching using SBERT
- Multi-factor scoring (Skills 50% + Experience 30% + Location 20%)
- Real-time candidate ranking
- Transparent scoring explanations

#### API Endpoints (6 total):
```
Core (2 endpoints):
├── GET  /           - Service information
└── GET  /health     - Health check

AI Processing (3 endpoints):
├── POST /match      - AI-powered candidate matching
├── POST /batch-match - Batch candidate matching
└── GET  /analyze/{candidate_id} - Detailed candidate analysis

Diagnostics (1 endpoint):
└── GET  /test-db    - Database connectivity test
```

#### Dependencies:
- FastAPI 0.115.6
- httpx 0.28.1
- psycopg2-binary 2.9.10
- pydantic 2.10.3

## 👥 Portal Service (Port 8501)

### 📍 Location: `/services/portal/`
### 🎯 Purpose: HR team interface and candidate management

#### Key Files:
- `app.py` - Main Streamlit HR interface
- `batch_upload.py` - Batch processing module

#### Features:
- **Dashboard**: Real-time candidate and job statistics
- **Search & Filter**: Advanced candidate filtering with AI
- **Job Management**: Create and manage job postings
- **AI Matching**: View top candidate matches with scoring
- **Values Assessment**: 5-point scale evaluation system
- **Batch Upload**: Drag-and-drop resume processing
- **Reports**: Export candidates and analytics data

#### Pages:
```
HR Portal Navigation:
├── 🏢 Create Job           - Job posting interface
├── 🔍 Search & Filter      - Candidate search with filters
├── 📊 Submit Values        - Values assessment form
├── 📈 View Dashboard       - Analytics and metrics
├── 🎯 View Top-5 Shortlist - AI-powered candidate ranking
├── 📤 Upload Candidates    - Bulk candidate upload
├── 📁 Batch Upload         - Resume file processing
├── 📅 Interview Management - Interview scheduling
└── 🔄 Live Client Jobs     - Real-time job monitoring
```

#### Dependencies:
- Streamlit 1.41.1
- pandas 2.3.2
- httpx 0.28.1
- requests 2.32.3

## 🏢 Client Portal Service (Port 8502)

### 📍 Location: `/services/client_portal/`
### 🎯 Purpose: Client interface for job posting and candidate review

#### Key Files:
- `app.py` - Main Streamlit client interface
- `auth_service.py` - Enterprise authentication service

#### Features:
- **Enterprise Authentication**: bcrypt + JWT + PostgreSQL
- **Job Posting**: Complete job creation workflow
- **Candidate Review**: AI-matched candidate evaluation
- **Match Results**: Advanced AI scoring and ranking
- **Reports & Analytics**: Real-time pipeline data and exports
- **Multi-Client Support**: Isolated client environments

#### Authentication Features:
```
Enterprise Security:
├── 🔐 bcrypt Password Hashing    - Secure password storage
├── 🎫 JWT Token Authentication   - Stateless session management
├── 🛡️ Account Lockout Protection - Brute force prevention
├── 📊 PostgreSQL Integration     - Persistent client storage
├── 🔄 Session Management         - Token expiration and renewal
└── 📋 Audit Trail               - Login and activity logging
```

#### Pages:
```
Client Portal Navigation:
├── 📝 Job Posting         - Create and post new jobs
├── 👥 Candidate Review    - Review AI-matched candidates
├── 🎯 Match Results       - Advanced AI matching analysis
└── 📊 Reports & Analytics - Pipeline data and exports
```

#### Dependencies:
- Streamlit 1.41.1
- pandas 2.3.2
- bcrypt 4.1.2
- PyJWT 2.8.0
- sqlalchemy 2.0.36
- psycopg2-binary 2.9.10

## 🗄️ Database Service (Port 5432)

### 📍 Location: `/services/db/`
### 🎯 Purpose: PostgreSQL data storage and management

#### Key Files:
- `init.sql` - Database initialization scripts

#### Database Schema (11 tables):
```
Core Tables:
├── candidates        - Candidate information and profiles
├── jobs             - Job postings and requirements
├── client_auth      - Client authentication data
├── client_sessions  - JWT session management
├── feedback         - Values assessment data
├── interviews       - Interview scheduling
├── offers           - Job offers and status
├── candidate_skills - Skills mapping and proficiency
├── job_skills       - Required skills for jobs
├── match_results    - AI matching results and scores
└── system_metrics   - Performance and usage metrics

Indexes: 25+ optimized indexes for performance
Triggers: Audit logging and data validation
Views: Materialized views for analytics
```

#### Features:
- PostgreSQL 17 for latest performance
- Encrypted credential storage with bcrypt
- Comprehensive foreign key relationships
- 25+ optimized indexes for query performance
- Audit triggers and logging
- Health check monitoring
- Connection pooling (pool_size=10)
- Real data: 31 candidates from actual resumes

## 🧠 Semantic Engine

### 📍 Location: `/services/semantic_engine/`
### 🎯 Purpose: Advanced semantic processing for intelligent matching

#### Key Files:
- `semantic_processor.py` - SBERT-based semantic analysis

#### Features:
- Sentence-BERT (SBERT) processing
- Semantic similarity calculation
- Enhanced candidate matching
- Transparent scoring explanations

## 🔄 Service Communication

### Internal Communication Flow:
```
Client Portal (8502) 
    ↓ HTTP/REST
Gateway (8000)
    ↓ HTTP/REST  
Agent (9000) ← Semantic Engine
    ↓ SQL
Database (5432)
    ↑ HTTP/REST
Portal (8501)
```

### Authentication Flow:
```
Client Login → auth_service.py → bcrypt verification → JWT generation → PostgreSQL session storage → Authorized access
```

### Data Processing Flow:
```
Resume Upload → comprehensive_resume_extractor.py → candidates.csv → database_sync_manager.py → PostgreSQL → API Gateway → AI Matching
```

## 🛡️ Security Architecture

### Service-Level Security:
- **Gateway**: API key authentication, CORS protection
- **Client Portal**: Enterprise authentication with bcrypt + JWT
- **Portal**: Session-based access control
- **Agent**: Internal service communication
- **Database**: Encrypted connections, credential hashing

### Network Security:
- Docker network isolation
- Port-based service separation
- Health check endpoints
- Secure environment variables

## 📊 Monitoring & Health Checks

### Health Endpoints:
```
Service Health Checks:
├── http://localhost:8000/health  - Gateway status
├── http://localhost:9000/health  - Agent status
├── http://localhost:8501         - Portal accessibility
├── http://localhost:8502         - Client Portal accessibility
└── Database connection checks    - PostgreSQL connectivity
```

### Monitoring Features:
- Automatic service restart on failure
- Health check intervals
- Log aggregation
- Resource usage monitoring

## 🚀 Deployment Configuration

### Docker Compose Services:
```yaml
services:
  gateway:    # API Gateway (8000)
  agent:      # AI Matching (9000)  
  portal:     # HR Portal (8501)
  client_portal: # Client Portal (8502)
  db:         # PostgreSQL (5432)
```

### Environment Variables:
- `DATABASE_URL` - PostgreSQL connection string
- `API_KEY_SECRET` - API authentication key
- `JWT_SECRET` - JWT token signing key
- `CORS_ORIGINS` - Allowed CORS origins

## 🔧 Service Management Commands

### Start All Services:
```bash
docker-compose -f docker-compose.production.yml up -d
```

### Check Service Status:
```bash
docker-compose -f docker-compose.production.yml ps
```

### View Service Logs:
```bash
docker logs bhivhraiplatform-gateway-1
docker logs bhivhraiplatform-client_portal-1
docker logs bhivhraiplatform-portal-1
docker logs bhivhraiplatform-agent-1
docker logs bhivhraiplatform-db-1
```

### Restart Individual Service:
```bash
docker restart bhivhraiplatform-[service-name]-1
```

### Scale Services:
```bash
docker-compose -f docker-compose.production.yml up -d --scale gateway=2
```

## 🎯 Service Performance

### Response Times:
- **Gateway**: <100ms average
- **Agent**: <0.02s for AI matching
- **Portal**: Real-time UI updates
- **Client Portal**: <200ms for authentication
- **Database**: <50ms for queries

### Throughput:
- **Concurrent Users**: Multi-user support
- **API Requests**: 1000+ requests/minute
- **Resume Processing**: 1-2 seconds per file
- **AI Matching**: 10+ candidates in <0.02s

---

**🔧 Services Guide** - Comprehensive microservices documentation for BHIV HR Platform architecture.