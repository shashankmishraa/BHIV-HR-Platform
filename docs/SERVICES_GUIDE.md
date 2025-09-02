# 🔧 BHIV HR Platform - Services Guide

## 🏗️ Microservices Architecture Overview

The BHIV HR Platform consists of 5 core microservices, each with specific responsibilities and clear interfaces.

## 🌐 Gateway Service (Port 8000)

### 📍 Location: `/services/gateway/`
### 🎯 Purpose: Central API hub and request routing

#### Key Files:
- `app/main.py` - Main FastAPI application with 16 endpoints
- `client_auth.py` - Client authentication utilities
- `app/db/schemas.py` - Pydantic models for validation

#### API Endpoints (16 total):
```
Core API Endpoints:
├── GET  /           - API root information
├── GET  /health     - Health check
└── GET  /test-candidates - Database connectivity test

Job Management:
├── POST /v1/jobs    - Create new job posting
└── GET  /v1/jobs    - List all active jobs

Candidate Management:
├── GET  /v1/candidates/job/{job_id} - Get candidates by job
├── GET  /v1/candidates/search       - Search & filter candidates
└── POST /v1/candidates/bulk         - Bulk upload candidates

AI Matching Engine:
└── GET  /v1/match/{job_id}/top      - Get AI-matched candidates

Assessment & Workflow:
├── POST /v1/feedback    - Submit values assessment
├── POST /v1/interviews  - Schedule interview
└── POST /v1/offers      - Create job offer

Analytics & Statistics:
└── GET  /candidates/stats - Platform statistics

Client Portal API:
├── POST /v1/client/login - Client authentication
└── GET  /v1/client/jobs  - Get client jobs
```

#### Dependencies:
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- psycopg2-binary 2.9.9
- Pydantic 2.5.0

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

#### API Endpoints:
```
AI Matching:
├── GET  /health     - Health check
├── GET  /match      - Basic matching endpoint
└── POST /analyze    - Advanced semantic analysis
```

#### Dependencies:
- FastAPI 0.104.1
- sentence-transformers (optional)
- scikit-learn
- numpy

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
- Streamlit 1.28.1
- pandas 2.1.3
- httpx 0.25.2
- requests 2.31.0

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
- Streamlit 1.28.1
- pandas 2.1.3
- bcrypt 4.1.2
- PyJWT 2.8.0
- sqlalchemy 2.0.23
- psycopg2-binary 2.9.9

## 🗄️ Database Service (Port 5432)

### 📍 Location: `/services/db/`
### 🎯 Purpose: PostgreSQL data storage and management

#### Key Files:
- `init.sql` - Database initialization scripts

#### Database Schema:
```
Tables:
├── candidates        - Candidate information and profiles
├── jobs             - Job postings and requirements
├── client_auth      - Client authentication data
├── client_sessions  - JWT session management
├── feedback         - Values assessment data
├── interviews       - Interview scheduling
└── offers           - Job offers and status
```

#### Features:
- PostgreSQL 15-alpine for reliability
- Encrypted credential storage
- Foreign key relationships
- Health check monitoring
- Automatic backups

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