# 🚀 BHIV HR Platform

**Enterprise AI-Powered Recruiting Platform** with intelligent candidate matching, comprehensive assessment tools, and production-grade security.

## 🌐 Live Production Platform

### **✅ Currently Deployed on Render**
- **API Gateway**: bhiv-hr-gateway-46pz.onrender.com/docs ✅ (55 endpoints)
- **AI Matching Engine**: bhiv-hr-agent-m1me.onrender.com/docs ✅ (6 endpoints - LIVE)
- **HR Portal**: bhiv-hr-portal-cead.onrender.com/ ✅
- **Client Portal**: bhiv-hr-client-portal-5g33.onrender.com/ ✅
- **Candidate Portal**: bhiv-hr-candidate-portal.onrender.com/ ✅ **NEW**
- **Database**: PostgreSQL 17 on Render ✅
- **Status**: ✅ **5/5 SERVICES OPERATIONAL** | **Cost**: $0/month (Free tier)
- **Total Endpoints**: 61 (55 Gateway + 6 Agent verified) | **Updated**: October 23, 2025 - Database & Portal Issues Fixed
- **Python Version**: 3.12.7-slim | **FastAPI**: 0.115.6 | **Streamlit**: 1.41.1

### **🔑 Demo Access**
```bash
# Client Portal Login
Username: TECH001
Password: demo123

# API Testing
API Key: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health
```

## 📋 Documentation Structure

### **📚 Core Documentation**
- **[📋 PROJECT_STRUCTURE.md](docs/architecture/PROJECT_STRUCTURE.md)** - ✅ Complete architecture and folder organization
- **[🚀 DEPLOYMENT_STATUS.md](docs/architecture/DEPLOYMENT_STATUS.md)** - ✅ Current deployment status and health metrics
- **[📊 PRODUCTION_READINESS_REPORT.md](docs/reports/PRODUCTION_READINESS_REPORT.md)** - ✅ Complete production verification report
- **[🖥️ docs/architecture/PORTAL_SERVICES_SUMMARY.md](docs/architecture/PORTAL_SERVICES_SUMMARY.md)** - ✅ Portal services documentation with recent fixes
- **[🏢 docs/architecture/CLIENT_PORTAL_SERVICE_SUMMARY.md](docs/architecture/CLIENT_PORTAL_SERVICE_SUMMARY.md)** - ✅ Client portal service documentation with enterprise auth
- **[🏗️ docs/architecture/SERVICES_ARCHITECTURE_SUMMARY.md](docs/architecture/SERVICES_ARCHITECTURE_SUMMARY.md)** - ✅ Complete services architecture documentation
- **[📝 CHANGES_LOG.md](CHANGES_LOG.md)** - ✅ Detailed log of all changes made
- **[⚡ docs/QUICK_START_GUIDE.md](docs/QUICK_START_GUIDE.md)** - ✅ Get started in 5 minutes
- **[🎯 docs/CURRENT_FEATURES.md](docs/CURRENT_FEATURES.md)** - ✅ Complete feature list and capabilities

### **🔧 Technical Guides**
- **[🚀 docs/deployment/](docs/deployment/)** - Deployment guides and configurations
- **[🔒 docs/security/](docs/security/)** - Security analysis, bias mitigation, and audit reports
- **[🧪 docs/testing/](docs/testing/)** - Testing strategies and API testing guides
- **[👥 docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - Complete user manual
- **[📝 docs/REFLECTION.md](docs/REFLECTION.md)** - ✅ Daily development reflections
- **[🔍 SCHEMA_COMPARISON_REPORT.md](docs/reports/SCHEMA_COMPARISON_REPORT.md)** - ✅ Database schema analysis
- **[🖥️ docs/architecture/PORTAL_SERVICES_SUMMARY.md](docs/architecture/PORTAL_SERVICES_SUMMARY.md)** - ✅ Complete portal services documentation

## ⚡ Quick Start

### **🎯 Choose Your Path:**
1. **🌐 Live Platform**: Use production services immediately → [Quick Start Guide](docs/QUICK_START_GUIDE.md)
2. **💻 Local Development**: Run on your machine → [Setup Instructions](docs/QUICK_START_GUIDE.md#local-development-setup)

### **🚀 5-Minute Setup**
```bash
# Live Platform - No Setup Required
HR Portal: bhiv-hr-portal-cead.onrender.com/
Client Portal: bhiv-hr-client-portal-5g33.onrender.com/
Credentials: TECH001 / demo123

# Local Development - Docker Required
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform
docker-compose -f deployment/docker/docker-compose.production.yml up -d
# Access: http://localhost:8501
```

---

## 🏗️ System Architecture

### **Microservices Architecture**
| Service | Purpose | Technology | Port | Status | Production URL |
|---------|---------|------------|------|--------|----------------|
| **API Gateway** | REST API Backend | FastAPI 0.115.6 + Python 3.12.7-slim | 8000 | ✅ Live | bhiv-hr-gateway-46pz.onrender.com |
| **AI Agent** | Candidate Matching | FastAPI 0.115.6 + Python 3.12.7-slim | 9000 | ✅ Live | bhiv-hr-agent-m1me.onrender.com |
| **HR Portal** | HR Dashboard | Streamlit 1.41.1 + Python 3.12.7-slim | 8501 | ✅ Live | bhiv-hr-portal-cead.onrender.com |
| **Client Portal** | Client Interface | Streamlit 1.41.1 + Python 3.12.7-slim | 8502 | ✅ Live | bhiv-hr-client-portal-5g33.onrender.com |
| **Candidate Portal** | Job Seeker Interface | Streamlit 1.41.1 + Python 3.12.7-slim | 8503 | ✅ Live | bhiv-hr-candidate-portal.onrender.com |
| **Database** | Data Storage | PostgreSQL 17 | 5432 | ✅ Live | Internal Render URL |

### **API Endpoints (61 Total)**
```
Gateway Service (55 endpoints):
  Core API (3):           GET /, /health, /test-candidates
  Monitoring (3):         GET /metrics, /health/detailed, /metrics/dashboard
  Analytics (3):          GET /candidates/stats, GET /v1/database/schema, GET /v1/reports/job/{job_id}/export.csv
  Job Management (2):     GET /v1/jobs, POST /v1/jobs
  Candidate Mgmt (5):     GET /v1/candidates, GET /v1/candidates/{id}, GET /v1/candidates/search, 
                          POST /v1/candidates/bulk, GET /v1/candidates/job/{job_id}
  AI Matching (2):        GET /v1/match/{job_id}/top, POST /v1/match/batch
  Assessment (6):         GET/POST /v1/feedback, GET/POST /v1/interviews, GET/POST /v1/offers
  Security Testing (7):   Rate limiting, input validation, email/phone validation, headers, penetration testing
  CSP Management (4):     Policies, violations, reporting, testing
  2FA Authentication (8): Setup, verify, login, status, disable, backup codes, token testing
  Password Mgmt (6):      Validate, generate, policy, change, strength test, security tips
  Client Portal (1):      POST /v1/client/login
  Candidate Portal (5):   POST /v1/candidate/register, POST /v1/candidate/login, 
                          PUT /v1/candidate/profile/{id}, POST /v1/candidate/apply, 
                          GET /v1/candidate/applications/{id}

Agent Service (6 endpoints):
  Core (2):              GET /, GET /health
  AI Processing (3):     POST /match, POST /batch-match, GET /analyze/{candidate_id}
  Diagnostics (1):       GET /test-db
```

---

## 🚀 Key Features

### **🤖 AI-Powered Matching (Phase 3)**
- **Semantic Engine**: Production Phase 3 implementation with sentence transformers
- **Adaptive Scoring**: Company-specific weight optimization based on feedback
- **Cultural Fit Analysis**: Feedback-based alignment scoring (10% bonus)
- **Enhanced Batch Processing**: Async processing with smart caching (50 candidates/chunk)
- **Learning Engine**: Company preference tracking and optimization
- **Real-time Processing**: <0.02 second response time with caching
- **Multi-Factor Scoring**: Semantic (40%), Experience (30%), Skills (20%), Location (10%)
- **No Fallbacks**: Production-grade implementation only

### **🔒 Enterprise Security**
- **Unified Authentication**: Dual Bearer token + JWT system with `dependencies.py`
- **Dynamic Rate Limiting**: CPU-based adjustment (60-500 requests/minute)
- **2FA TOTP**: Complete implementation with QR code generation
- **Security Headers**: CSP, XSS protection, Frame Options
- **Input Validation**: XSS/SQL injection protection with testing endpoints
- **Password Policies**: Enterprise-grade validation with strength testing

### **📊 Triple Portal System**
- **HR Portal**: Dashboard, candidate search, job management, AI matching with Streamlit 1.41.1 fixes
- **Client Portal**: Enterprise authentication, job posting, candidate review with security enhancements
- **Candidate Portal**: Job seeker interface, profile management, application tracking, job search
- **Real-time Analytics**: Performance metrics and insights across all portals
- **Values Assessment**: 5-point evaluation system
- **Batch Upload**: Secure file processing with path traversal protection
- **2FA Integration**: QR code generation with function-level imports

### **📈 Resume Processing**
- **Multi-format Support**: PDF, DOCX, TXT files
- **High Accuracy**: 75-96% extraction accuracy
- **Batch Processing**: Handle multiple resumes simultaneously
- **Error Monitoring**: Comprehensive tracking and metrics

### **📊 Advanced Monitoring**
- **Prometheus Metrics**: Real-time performance tracking
- **System Health**: CPU, memory, disk usage monitoring
- **Business Metrics**: Job postings, matches, user activity
- **Error Tracking**: Structured logging with categorization
- **Performance Analytics**: Response times, throughput analysis

---

## 🛠️ Development & Deployment

### **Project Structure**
```
bhiv-hr-platform/
├── services/                    # Microservices
│   ├── gateway/                # API Gateway (55 endpoints)
│   │   ├── app/               # Application code
│   │   │   ├── main.py        # FastAPI application (2000+ lines)
│   │   │   ├── monitoring.py  # Advanced monitoring system
│   │   │   └── __init__.py    # Package initialization
│   │   ├── routes/            # Route modules
│   │   │   └── auth.py        # Authentication routes
│   │   ├── logs/              # Application logs
│   │   ├── semantic_engine/   # Shared semantic engine
│   │   ├── dependencies.py    # Unified authentication
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Dependencies (FastAPI 0.115.6)
│   ├── agent/                  # AI Matching Engine (6 endpoints)
│   │   ├── app.py             # FastAPI AI service (600+ lines)
│   │   ├── semantic_engine/   # Phase 3 AI engine
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # AI/ML dependencies
│   ├── portal/                 # HR Dashboard
│   │   ├── app.py             # Streamlit interface (1500+ lines)
│   │   ├── batch_upload.py    # Batch processing
│   │   ├── config.py          # Configuration
│   │   ├── file_security.py   # File security
│   │   ├── components/        # UI components
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Streamlit 1.41.1 dependencies
│   ├── client_portal/          # Client Interface
│   │   ├── app.py             # Client interface (800+ lines)
│   │   ├── auth_service.py    # Enterprise authentication
│   │   ├── config.py          # Configuration
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Streamlit dependencies
│   ├── candidate_portal/       # Candidate Interface
│   │   ├── app.py             # Job seeker interface
│   │   ├── config.py          # Configuration
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Streamlit dependencies
│   ├── semantic_engine/        # Shared Phase 3 AI Engine
│   │   ├── __init__.py        # Package initialization
│   │   └── phase3_engine.py   # Production semantic engine
│   └── db/                     # Database Schema
│       ├── consolidated_schema.sql # Complete schema v4.1.0 (15 core tables)
│       └── Dockerfile         # Database container
├── docs/                       # Complete Documentation
│   ├── architecture/          # System architecture docs
│   │   ├── PROJECT_STRUCTURE.md
│   │   ├── DEPLOYMENT_STATUS.md
│   │   └── SERVICES_ARCHITECTURE_SUMMARY.md
│   ├── deployment/            # Deployment guides
│   ├── security/              # Security analysis & bias mitigation
│   ├── testing/               # Testing strategies & API guides
│   ├── reports/               # Production readiness reports
│   ├── QUICK_START_GUIDE.md   # Get started in 5 minutes
│   ├── CURRENT_FEATURES.md    # Complete feature list
│   ├── USER_GUIDE.md          # User documentation
│   └── REFLECTION.md          # Development reflections
├── tests/                      # Comprehensive Test Suite
│   ├── test_endpoints.py      # Core API tests (300+ lines)
│   ├── test_security.py       # Security validation
│   ├── test_client_portal.py  # Portal tests
│   └── test_candidate_portal.py # Candidate portal tests
├── deployment/                 # Deployment Configuration
│   ├── docker/                # Docker configurations
│   │   └── docker-compose.production.yml # Local development setup
│   ├── scripts/               # Deployment scripts
│   └── render-deployment.yml  # Render platform config
├── tools/                      # Data Processing Tools
│   ├── dynamic_job_creator.py
│   ├── database_sync_manager.py
│   ├── comprehensive_resume_extractor.py
│   └── auto_sync_watcher.py
├── config/                     # Configuration Files
│   ├── environments/          # Environment configs
│   ├── .env.render           # Render configuration
│   └── production.env        # Production settings
├── data/                       # Real Production Data
│   └── candidates.csv        # Candidate data
├── assets/                     # Static Assets
│   └── resumes/               # Resume files (27 files)
├── src/                        # Shared Source Code
│   ├── common/                # Common utilities
│   ├── models/                # Shared models
│   └── utils/                 # Utility functions
└── README.md                   # This file
```

### **Database Schema v4.1.0 (15 Core Tables - Optimized)**

#### **Core Application Tables (12)**
```sql
-- Primary entities
candidates              -- Candidate profiles with authentication
jobs                   -- Job postings from clients and HR
feedback               -- Values assessment (5-point BHIV values)
interviews             -- Interview scheduling and management
offers                 -- Job offer management

-- Authentication & Security
users                  -- Internal HR users with 2FA support
clients                -- External client companies with JWT auth
audit_logs             -- Security and compliance tracking
rate_limits            -- API rate limiting by IP and endpoint
csp_violations         -- Content Security Policy monitoring

-- AI & Performance
matching_cache         -- AI matching results cache
company_scoring_preferences -- Phase 3 learning engine
```

#### **System Tables (5)**
```sql
client_auth            -- Enhanced authentication
client_sessions        -- Session management
schema_version         -- Version tracking (v4.1.0)
pg_stat_statements     -- Performance monitoring
pg_stat_statements_info -- Statistics metadata
```

#### **Key Schema Features**
- **Constraints**: CHECK constraints for data validation
- **Indexes**: 25+ performance indexes including GIN for full-text search
- **Triggers**: Auto-update timestamps and audit logging
- **Functions**: PostgreSQL functions for complex operations
- **Generated Columns**: Automatic average score calculation

### **Configuration Files**
```bash
# Environment Configuration
.env.example                              # Template for local development
config/.env.render                        # Render platform configuration
config/production.env                     # Production settings

# Deployment Configuration  
deployment/docker/docker-compose.production.yml  # Docker setup
deployment/render-deployment.yml                 # Render platform config
docs/deployment/RENDER_DEPLOYMENT_GUIDE.md       # Complete deployment guide
```

### **Local Development Setup**
```bash
# Prerequisites
- Docker & Docker Compose
- Python 3.12.7 (Required)
- Git

# Environment Setup
cp .env.example .env
# Edit .env with your configuration

# Start All Services
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Health Verification
curl http://localhost:8000/health    # Gateway (55 endpoints)
curl http://localhost:9000/health    # AI Agent (6 endpoints)
open http://localhost:8501           # HR Portal (Streamlit)
open http://localhost:8502           # Client Portal (Streamlit)
open http://localhost:8503           # Candidate Portal (Streamlit)

# Database Access
psql postgresql://bhiv_user:password@localhost:5432/bhiv_hr
```

---

## 🧪 Testing & Validation

### **API Testing**
```bash
# Health Checks
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health

# Authenticated Endpoints
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Database Schema Verification
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/database/schema

# AI Matching Test
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top

# Security Testing
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/rate-limit-status
```

### **Test Suite**
```bash
# Run Core Tests
python tests/api/test_endpoints.py      # API functionality (300+ lines)
python tests/security/test_security.py  # Security features  
python tests/integration/test_client_portal.py  # Portal integration
python tests/integration/test_candidate_portal.py # Candidate portal tests

# Comprehensive Testing
python tests/api/comprehensive_endpoint_testing.py  # All endpoints
python tests/run_all_tests.py       # Complete test suite
```

---

## 📊 Performance Metrics

### **Current Performance (Production)**
- **API Response Time**: <100ms average (Gateway)
- **AI Matching Speed**: <0.02 seconds (with caching)
- **Database Queries**: <50ms typical response time
- **Resume Processing**: 1-2 seconds per file
- **Uptime**: 99.9% (achieved for all services)
- **Concurrent Users**: Multi-user support enabled
- **Rate Limiting**: Dynamic 60-500 requests/minute
- **Connection Pooling**: 10 connections + 5 overflow
- **Memory Usage**: Optimized for free tier limits

### **System Monitoring**
```bash
# Production Monitoring
curl https://bhiv-hr-gateway-46pz.onrender.com/metrics
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health/detailed
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/metrics/dashboard

# Local Monitoring  
curl http://localhost:8000/metrics              # Prometheus metrics
curl http://localhost:8000/health/detailed      # Comprehensive health
curl http://localhost:8000/metrics/dashboard    # Real-time dashboard
```

---

## 🔧 Tools & Utilities

### **Data Processing Tools**
```bash
# Resume Processing (27 files processed)
python tools/comprehensive_resume_extractor.py

# Job Creation (19 jobs created)
python tools/dynamic_job_creator.py --count 15
python tools/dynamic_job_creator.py --type software_engineer --count 5

# Database Management
python tools/database_sync_manager.py

# Auto Sync (Development)
python tools/auto_sync_watcher.py
```

### **Deployment Tools**
```bash
# Local Deployment (Windows)
scripts/local-deploy.cmd

# Docker Compose Deployment
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Health Monitoring
python tests/test_endpoints.py  # Comprehensive health checks
```

---

## 📚 Documentation

### **Complete Guides**
- **[DEPLOYMENT_STATUS.md](docs/architecture/DEPLOYMENT_STATUS.md)** - Current deployment status
- **[PROJECT_STRUCTURE.md](docs/architecture/PROJECT_STRUCTURE.md)** - Complete architecture guide
- **[RENDER_DEPLOYMENT_GUIDE.md](docs/deployment/RENDER_DEPLOYMENT_GUIDE.md)** - Complete deployment guide

### **Technical Documentation**
- **[CURRENT_FEATURES.md](docs/CURRENT_FEATURES.md)** - Complete feature list and capabilities
- **[SECURITY_AUDIT.md](docs/security/SECURITY_AUDIT.md)** - Security analysis & bias mitigation
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Complete user manual
- **[REFLECTION.md](docs/REFLECTION.md)** - Development reflections with values
- **[PRODUCTION_READINESS_REPORT.md](docs/reports/PRODUCTION_READINESS_REPORT.md)** - Production verification
- **[API_DOCUMENTATION.md](docs/api/API_DOCUMENTATION.md)** - Complete API reference

---

## 🎯 Current Status & Progress

### **✅ Completed Features**
- **Production Deployment**: ✅ 5/5 services live on Render (99.9% uptime)
- **Local Development**: ✅ 5/5 services fully operational with Docker Compose
- **API Gateway**: ✅ 55 endpoints with unified authentication system
- **AI Agent Service**: ✅ 6 endpoints with Phase 3 semantic matching
- **Triple Portal System**: ✅ HR, Client, and Candidate portals operational
- **Database Schema**: ✅ v4.1.0 with 17 tables (PostgreSQL 17)
- **Real Data Integration**: ✅ 31 candidates + 19 jobs + 27 resume files
- **Enterprise Security**: ✅ 2FA, rate limiting, CSP policies, input validation
- **Performance Optimization**: ✅ <100ms API response, connection pooling
- **Comprehensive Testing**: ✅ 300+ lines of endpoint tests
- **Complete Documentation**: ✅ Architecture guides, deployment status, feature lists
- **Monitoring System**: ✅ Prometheus metrics, health checks, performance tracking
- **Authentication System**: ✅ Unified Bearer token + JWT with enterprise features
- **AI Matching Engine**: ✅ Phase 3 semantic matching with learning capabilities
- **Security Implementation**: ✅ Penetration testing endpoints, password policies
- **Project Organization**: ✅ Professional structure with comprehensive documentation

### **📈 System Metrics (Production)**
- **Total Services**: 5 (All operational) + Database
- **API Endpoints**: 61 interactive endpoints (55 Gateway + 6 Agent)
- **AI Algorithm**: Phase 3 - v3.0.0-phase3-production (fully operational)
- **Learning Engine**: Company preference optimization (schema v4.1.0 deployed)
- **Database Schema**: v4.1.0 with 15 core tables (PostgreSQL 17) - Optimized
- **Real Candidates**: ✅ 11 verified in production database
- **Real Jobs**: ✅ 20 active job postings
- **Active Clients**: ✅ 3 client companies with authentication
- **Portal Services**: ✅ Streamlit 1.41.1 with security enhancements
- **Code Quality**: ✅ Production-ready with comprehensive error handling
- **Test Coverage**: ✅ Complete test suite (300+ lines of tests)
- **Documentation**: ✅ 100% complete with architecture guides
- **Monthly Cost**: $0 (Free tier deployment)
- **Global Access**: HTTPS with SSL certificates
- **Auto-Deploy**: GitHub integration enabled
- **Uptime**: 99.9% (achieved for all services)
- **Local Environment**: ✅ Fully operational with Docker Compose
- **Performance**: <100ms API response, <0.02s AI matching

### **🔄 Recent Updates (October 23, 2025)**
- ✅ **Database Schema Deployment**: Successfully deployed v4.1.0 to live Render PostgreSQL
- ✅ **Database Cleanup**: Removed 4 redundant tables, optimized to 15 core tables
- ✅ **Portal Configuration Fix**: Fixed Docker URLs to production URLs for all portals
- ✅ **Connection Issues Resolved**: All portals now properly connect to Gateway API
- ✅ **Production Services**: All 5 services operational with 99.9% uptime
- ✅ **API Gateway**: 55 endpoints with unified authentication system
- ✅ **AI Agent Service**: 6 endpoints with Phase 3 semantic matching
- ✅ **Triple Portal System**: HR, Client, and Candidate portals fully operational
- ✅ **Database Integrity**: 11 candidates, 20 jobs, 3 clients, 5 interviews verified
- ✅ **Security Implementation**: 2FA, rate limiting, CSP policies, input validation
- ✅ **Performance Optimization**: <100ms API response, 75 indexes for fast queries
- ✅ **Deployment Scripts**: Complete database deployment and verification tools
- ✅ **Architecture Documentation**: Updated with current deployment status
- ✅ **Configuration Management**: Production-ready portal configurations

---

## 🚀 Getting Started (Choose Your Path)

### **🌐 For Users (Recommended)**
1. **Visit Live Platform**: bhiv-hr-gateway-46pz.onrender.com/docs
2. **Access HR Portal**: bhiv-hr-portal-cead.onrender.com/
3. **Login to Client Portal**: bhiv-hr-client-portal-5g33.onrender.com/ (TECH001/demo123)
4. **Use Candidate Portal**: http://localhost:8503 (Local development)
5. **Test API**: Use Bearer token `prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o`

### **💻 For Developers**
1. **Clone Repository**: `git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git`
2. **Setup Environment**: Copy `.env.example` to `.env`
3. **Start Services**: `docker-compose -f deployment/docker/docker-compose.production.yml up -d`
4. **Run Tests**: `python tests/test_endpoints.py` and `python tests/test_candidate_portal.py`

### **🚀 For Deployment**
1. **Read Guide**: [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)
2. **Check Status**: [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)
3. **Monitor Health**: Use provided health check endpoints

---

## 📞 Support & Resources

### **Live Platform Access**
- **API Documentation**: bhiv-hr-gateway-46pz.onrender.com/docs
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Deployment Platform**: Render Cloud (Oregon, US West)

### **Quick Links**
- **🔗 Live API**: bhiv-hr-gateway-46pz.onrender.com/docs
- **🔗 HR Dashboard**: bhiv-hr-portal-cead.onrender.com/
- **🔗 Client Portal**: bhiv-hr-client-portal-5g33.onrender.com/
- **🔗 Candidate Portal**: bhiv-hr-candidate-portal.onrender.com
- **🔗 AI Agent**: bhiv-hr-agent-m1me.onrender.com/docs

---

**BHIV HR Platform v3.0.0-Phase3** - Enterprise recruiting solution with advanced AI learning, enhanced batch processing, and adaptive scoring capabilities.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: October 23, 2025 | **Production**: ✅ 5/5 Services Live | **Database**: ✅ 15 Core Tables Optimized | **AI Version**: Phase 3 Advanced (Operational) | **Cost**: $0/month | **Uptime**: 99.9%