# 📁 BHIV HR Platform - Complete Project Structure

**Generated**: January 2025  
**Architecture**: Microservices (5 Services + Database)  
**Status**: ✅ Production Ready  
**Deployment**: Live on Render + Local Development

---

## 🏗️ Project Overview

### **System Architecture**
- **Microservices**: 5 independent services
- **Database**: PostgreSQL 17 with 17 tables
- **Authentication**: Triple-layer (API Key + Client JWT + Candidate JWT)
- **AI Engine**: Phase 3 semantic matching
- **Deployment**: Production on Render + Local Docker
- **Total Endpoints**: 61 (55 Gateway + 6 Agent)

---

## 📂 Complete Directory Structure

```
bhiv-hr-platform/
├── services/                    # Microservices Architecture
│   ├── gateway/                # API Gateway Service (Port 8000)
│   │   ├── app/               # Application core
│   │   │   ├── main.py        # FastAPI application (2000+ lines, 55 endpoints)
│   │   │   ├── monitoring.py  # Prometheus metrics & health checks
│   │   │   └── __init__.py    # Package initialization
│   │   ├── routes/            # Route modules
│   │   │   └── auth.py        # 2FA authentication routes (4 endpoints)
│   │   ├── logs/              # Application logs
│   │   ├── semantic_engine/   # Shared semantic engine
│   │   ├── dependencies.py    # Triple authentication system
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Dependencies (FastAPI 0.115.6)
│   ├── agent/                  # AI Matching Engine Service (Port 9000)
│   │   ├── app.py             # FastAPI AI service (600+ lines, 6 endpoints)
│   │   ├── semantic_engine/   # Phase 3 AI engine
│   │   │   ├── __init__.py    # Package initialization
│   │   │   └── phase3_engine.py # Production semantic engine
│   │   ├── Dockerfile         # Container configuration
│   │   ├── README.md          # Service documentation
│   │   └── requirements.txt   # AI/ML dependencies
│   ├── portal/                 # HR Dashboard Service (Port 8501)
│   │   ├── app.py             # Streamlit interface (1500+ lines)
│   │   ├── batch_upload.py    # Batch processing functionality
│   │   ├── config.py          # Configuration management
│   │   ├── file_security.py   # File security validation
│   │   ├── components/        # UI components
│   │   ├── Dockerfile         # Container configuration
│   │   ├── README.md          # Service documentation
│   │   └── requirements.txt   # Streamlit 1.41.1 dependencies
│   ├── client_portal/          # Client Interface Service (Port 8502)
│   │   ├── app.py             # Client interface (800+ lines)
│   │   ├── auth_service.py    # Enterprise authentication
│   │   ├── config.py          # Configuration management
│   │   ├── Dockerfile         # Container configuration
│   │   ├── README.md          # Service documentation
│   │   └── requirements.txt   # Streamlit dependencies
│   ├── candidate_portal/       # Candidate Interface Service (Port 8503)
│   │   ├── app.py             # Job seeker interface
│   │   ├── config.py          # Configuration management
│   │   ├── Dockerfile         # Container configuration
│   │   ├── README.md          # Service documentation
│   │   └── requirements.txt   # Streamlit dependencies
│   ├── semantic_engine/        # Shared Phase 3 AI Engine
│   │   ├── __init__.py        # Package initialization
│   │   └── phase3_engine.py   # Production semantic engine
│   └── db/                     # Database Schema & Configuration
│       ├── consolidated_schema.sql # Complete schema v4.1.0 (17 tables)
│       ├── Dockerfile         # Database container
│       └── README.md          # Database documentation
├── docs/                       # Complete Documentation Suite
│   ├── architecture/          # System architecture documentation
│   │   ├── PROJECT_STRUCTURE.md      # This file - complete structure
│   │   ├── SERVICES_ARCHITECTURE_SUMMARY.md # Services architecture
│   │   ├── DEPLOYMENT_STATUS.md      # Current deployment status
│   │   └── PROJECT_ORGANIZATION.md   # Project organization
│   ├── api/                   # API documentation
│   │   └── API_DOCUMENTATION.md      # Complete API reference
│   ├── database/              # Database documentation
│   │   ├── CONNECTION_DIAGRAM.md     # Database connections
│   │   ├── DBEAVER_SETUP_GUIDE.md    # Database setup guide
│   │   └── QUICK_QUERIES.sql         # Common queries
│   ├── deployment/            # Deployment guides
│   │   └── RENDER_DEPLOYMENT_GUIDE.md # Complete deployment guide
│   ├── security/              # Security documentation
│   │   ├── SECURITY_AUDIT.md         # Security analysis
│   │   └── BIAS_ANALYSIS.md          # Bias mitigation
│   ├── testing/               # Testing documentation
│   │   └── TESTING_STRATEGY.md       # Testing strategies
│   ├── reports/               # Analysis reports
│   │   ├── PRODUCTION_READINESS_REPORT.md # Production verification
│   │   ├── COMPREHENSIVE_CODEBASE_AUDIT_OCTOBER_2025.md # Code audit
│   │   ├── COMPREHENSIVE_VALIDATION_REPORT.md # Validation report
│   │   ├── DOCUMENTATION_SYNC_SUMMARY.md # Documentation sync
│   │   └── SCHEMA_COMPARISON_REPORT.md # Database schema analysis
│   ├── QUICK_START_GUIDE.md   # Get started in 5 minutes
│   ├── CURRENT_FEATURES.md    # Complete feature list
│   ├── USER_GUIDE.md          # Complete user manual
│   ├── SERVICES_GUIDE.md      # Services guide
│   ├── LIVE_DEMO.md           # Live demo information
│   ├── REFLECTION.md          # Development reflections
│   ├── CHANGELOG.md           # Change log
│   ├── AUDIT_SUMMARY.md       # Audit summary
│   └── README.md              # Documentation index
├── tests/                      # Comprehensive Test Suite
│   ├── api/                   # API testing
│   │   ├── test_endpoints.py  # Core API tests (300+ lines)
│   │   └── comprehensive_endpoint_testing.py # All endpoints
│   ├── integration/           # Integration testing
│   │   ├── test_client_portal.py # Client portal tests
│   │   └── test_candidate_portal.py # Candidate portal tests
│   ├── security/              # Security testing
│   │   └── test_security.py   # Security validation
│   └── run_all_tests.py       # Complete test suite runner
├── deployment/                 # Deployment Configuration
│   ├── docker/                # Docker configurations
│   │   └── docker-compose.production.yml # Local development setup
│   ├── scripts/               # Deployment scripts
│   │   ├── health-check.sh    # Health check script
│   │   ├── quick-deploy.sh    # Quick deployment
│   │   └── unified-deploy.sh  # Unified deployment
│   ├── README.md              # Deployment documentation
│   └── render-deployment.yml  # Render platform configuration
├── tools/                      # Data Processing & Management Tools
│   ├── dynamic_job_creator.py # Job creation tool (19 jobs created)
│   ├── database_sync_manager.py # Database synchronization
│   ├── comprehensive_resume_extractor.py # Resume processing (27 files)
│   └── auto_sync_watcher.py   # Auto synchronization watcher
├── config/                     # Configuration Management
│   ├── environments/          # Environment-specific configs
│   ├── .env.render           # Render platform configuration
│   └── production.env        # Production settings
├── data/                       # Production Data
│   └── candidates.csv        # Candidate data (31 candidates)
├── assets/                     # Static Assets
│   └── resumes/               # Resume files (27 files)
│       ├── AdarshYadavResume.pdf
│       ├── Anmol_Resume.pdf
│       ├── Anurag_CV.pdf
│       ├── ArulselvamJeganResume.pdf
│       ├── Ashmit Professional Resume.pdf
│       ├── ASMA_RESUME.pdf
│       ├── Devendra_resume_vit_vellore (2).pdf
│       ├── Final M.D Resume-document.pdf
│       ├── Hiten_Vishwakarma_CV.pdf
│       ├── Kamana_Shukla_Resume.pdf
│       ├── Kamran Idris Test Task.pdf
│       ├── Kunal_Pal_Resume-3.pdf
│       ├── Manal-Resume.pdf
│       ├── Mishti Agrawal.pdf
│       ├── Neha Gujar -CV.pdf
│       ├── Nitesh Cv.pdf
│       ├── Rashpal Resume .pdf
│       ├── Resume (6).pdf
│       ├── Resume vijay.pdf
│       ├── Resume_pdf-1.pdf
│       ├── Resume.pdf
│       ├── ResumeDataEng.pdf
│       ├── RUTUJA JS CV..pdf
│       ├── Sharan_Resume (2).pdf
│       ├── SoniYadav_Resume.pdf
│       ├── Sushant_Jadhav_Data_Analyst_Resume (1).pdf
│       ├── Ulkesh Sagwekar_Resume.pdf
│       ├── Vinayak's Resume.pdf
│       ├── Yash - CV.docx
│       └── Yash resume1.pdf
├── scripts/                    # Utility Scripts
│   ├── deployment/            # Deployment scripts
│   ├── maintenance/           # Maintenance scripts
│   └── local-deploy.cmd       # Local deployment (Windows)
├── src/                        # Shared Source Code
│   ├── common/                # Common utilities
│   │   └── __init__.py        # Package initialization
│   ├── models/                # Shared data models
│   │   └── __init__.py        # Package initialization
│   └── utils/                 # Utility functions
│       └── __init__.py        # Package initialization
├── lib/                        # External libraries
├── .env                        # Environment variables (local)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                   # Main project documentation
```

---

## 🏗️ Service Architecture Details

### **1. Gateway Service (services/gateway/)**
**Purpose**: Central API gateway with authentication and routing  
**Technology**: FastAPI 0.115.6 + Python 3.12.7  
**Port**: 8000  
**Endpoints**: 55 total

```python
# Key Files:
app/main.py              # Main FastAPI application (2000+ lines)
dependencies.py          # Triple authentication system
routes/auth.py          # 2FA authentication routes
app/monitoring.py       # Prometheus metrics & health monitoring
```

**Features**:
- Triple authentication (API Key + Client JWT + Candidate JWT)
- Dynamic rate limiting based on CPU usage
- 2FA TOTP authentication with QR codes
- Comprehensive security testing endpoints
- Values assessment workflow (5-point BHIV values)
- AI matching integration with Agent service
- Candidate portal APIs (registration, login, applications)

### **2. Agent Service (services/agent/)**
**Purpose**: AI-powered semantic candidate matching  
**Technology**: FastAPI 0.115.6 + Python 3.12.7  
**Port**: 9000  
**Endpoints**: 6 total

```python
# Key Files:
app.py                   # Main AI service (600+ lines)
semantic_engine/phase3_engine.py # Phase 3 semantic matching
```

**Features**:
- Phase 3 semantic matching engine
- Advanced candidate analysis
- Batch processing for multiple jobs
- Database connection pooling
- Fallback matching when Phase 3 unavailable

### **3. HR Portal Service (services/portal/)**
**Purpose**: HR dashboard and workflow management  
**Technology**: Streamlit 1.41.1 + Python 3.12.7  
**Port**: 8501

```python
# Key Files:
app.py                   # Main Streamlit interface (1500+ lines)
batch_upload.py         # Batch candidate upload
config.py               # Configuration management
file_security.py        # File security validation
```

**Features**:
- 10-step HR workflow process
- Real-time job monitoring
- AI-powered candidate shortlisting
- Values assessment interface
- Comprehensive export system
- Batch operations with security

### **4. Client Portal Service (services/client_portal/)**
**Purpose**: Enterprise client interface  
**Technology**: Streamlit 1.41.1 + Python 3.12.7  
**Port**: 8502

```python
# Key Files:
app.py                   # Client interface (800+ lines)
auth_service.py         # Enterprise authentication
config.py               # Configuration management
```

**Features**:
- Enterprise JWT authentication
- Job posting and management
- Candidate review interface
- Interview scheduling
- Analytics and reporting

### **5. Candidate Portal Service (services/candidate_portal/)**
**Purpose**: Job seeker interface  
**Technology**: Streamlit 1.41.1 + Python 3.12.7  
**Port**: 8503

```python
# Key Files:
app.py                   # Candidate interface
config.py               # Configuration management
```

**Features**:
- Candidate registration and login
- Profile management
- Job search and application
- Application tracking
- Status notifications

### **6. Database (services/db/)**
**Purpose**: Data storage and management  
**Technology**: PostgreSQL 17  
**Port**: 5432

```sql
# Key Files:
consolidated_schema.sql  # Complete schema v4.1.0 (17 tables)
```

**Features**:
- 17 tables (12 core + 5 system)
- Phase 3 learning engine support
- Comprehensive indexing
- Audit logging triggers
- Generated columns for calculations

---

## 📊 Database Schema v4.1.0

### **Core Tables (12)**
```sql
candidates              -- Candidate profiles with authentication
jobs                   -- Job postings from clients and HR
feedback               -- Values assessment (5-point BHIV values)
interviews             -- Interview scheduling and management
offers                 -- Job offer management
users                  -- Internal HR users with 2FA support
clients                -- External client companies with JWT auth
audit_logs             -- Security and compliance tracking
rate_limits            -- API rate limiting by IP and endpoint
csp_violations         -- Content Security Policy monitoring
matching_cache         -- AI matching results cache
company_scoring_preferences -- Phase 3 learning engine
```

### **System Tables (5)**
```sql
client_auth            -- Enhanced authentication
client_sessions        -- Session management
schema_version         -- Version tracking (v4.1.0)
pg_stat_statements     -- Performance monitoring
pg_stat_statements_info -- Statistics metadata
```

---

## 🔧 Configuration Management

### **Environment Files**
```bash
.env.example                    # Template for local development
config/.env.render             # Render platform configuration
config/production.env          # Production settings
```

### **Deployment Configuration**
```bash
deployment/docker/docker-compose.production.yml  # Local Docker setup
deployment/render-deployment.yml                 # Render platform config
deployment/scripts/                              # Deployment automation
```

---

## 🧪 Testing Infrastructure

### **Test Categories**
```python
tests/api/test_endpoints.py              # Core API functionality (300+ lines)
tests/api/comprehensive_endpoint_testing.py # All 61 endpoints
tests/integration/test_client_portal.py  # Client portal integration
tests/integration/test_candidate_portal.py # Candidate portal integration
tests/security/test_security.py         # Security validation
tests/run_all_tests.py                  # Complete test suite
```

### **Testing Coverage**
- **API Testing**: All 61 endpoints verified
- **Integration Testing**: Portal functionality
- **Security Testing**: Authentication and validation
- **Performance Testing**: Response times and load

---

## 🛠️ Development Tools

### **Data Processing Tools**
```python
tools/dynamic_job_creator.py           # Job creation (19 jobs created)
tools/comprehensive_resume_extractor.py # Resume processing (27 files)
tools/database_sync_manager.py         # Database synchronization
tools/auto_sync_watcher.py             # Auto synchronization
```

### **Deployment Tools**
```bash
scripts/local-deploy.cmd               # Local deployment (Windows)
deployment/scripts/health-check.sh     # Health monitoring
deployment/scripts/quick-deploy.sh     # Quick deployment
deployment/scripts/unified-deploy.sh   # Unified deployment
```

---

## 📚 Documentation Structure

### **Architecture Documentation**
- **PROJECT_STRUCTURE.md**: Complete project structure (this file)
- **SERVICES_ARCHITECTURE_SUMMARY.md**: Services architecture details
- **DEPLOYMENT_STATUS.md**: Current deployment status

### **User Documentation**
- **QUICK_START_GUIDE.md**: Get started in 5 minutes
- **USER_GUIDE.md**: Complete user manual
- **CURRENT_FEATURES.md**: Feature list and capabilities

### **Technical Documentation**
- **API_DOCUMENTATION.md**: Complete API reference
- **SECURITY_AUDIT.md**: Security analysis
- **TESTING_STRATEGY.md**: Testing approaches

---

## 🚀 Production Deployment

### **Live Services (5/5 Operational)**
- ✅ **Gateway**: bhiv-hr-gateway-46pz.onrender.com
- ✅ **Agent**: bhiv-hr-agent-m1me.onrender.com
- ✅ **HR Portal**: bhiv-hr-portal-cead.onrender.com
- ✅ **Client Portal**: bhiv-hr-client-portal-5g33.onrender.com
- ✅ **Candidate Portal**: bhiv-hr-candidate-portal.onrender.com

### **System Metrics**
- **Total Endpoints**: 61 (55 Gateway + 6 Agent)
- **Database Tables**: 17 (PostgreSQL 17)
- **Real Data**: 31 candidates, 19 jobs, 27 resume files
- **Monthly Cost**: $0 (Free tier deployment)
- **Uptime**: 99.9% (all services operational)

---

## 🔄 Local Development Setup

### **Prerequisites**
- Docker & Docker Compose
- Python 3.12.7
- Git

### **Quick Start**
```bash
# Clone repository
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform

# Environment setup
cp .env.example .env
# Edit .env with your configuration

# Start all services
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Verify services
curl http://localhost:8000/health    # Gateway
curl http://localhost:9000/health    # AI Agent
open http://localhost:8501           # HR Portal
open http://localhost:8502           # Client Portal
open http://localhost:8503           # Candidate Portal
```

---

## 📈 Performance & Monitoring

### **Current Performance**
- **API Response Time**: <100ms average
- **AI Matching Speed**: <0.02 seconds (with caching)
- **Database Queries**: <50ms typical response time
- **Resume Processing**: 1-2 seconds per file
- **Concurrent Users**: Multi-user support enabled

### **Monitoring Endpoints**
```bash
# Production monitoring
curl https://bhiv-hr-gateway-46pz.onrender.com/metrics
curl https://bhiv-hr-gateway-46pz.onrender.com/health/detailed

# Local monitoring
curl http://localhost:8000/metrics
curl http://localhost:8000/health/detailed
```

---

## 🔒 Security Features

### **Authentication Layers**
1. **API Key Authentication**: Production API access
2. **Client JWT**: Enterprise client authentication  
3. **Candidate JWT**: Job seeker authentication
4. **2FA TOTP**: Two-factor authentication
5. **Rate Limiting**: Dynamic rate limiting
6. **CSP Policies**: Content Security Policy

### **Security Implementation**
- Input validation and sanitization
- XSS/SQL injection protection
- Password strength validation
- Audit logging and monitoring
- Session management
- Penetration testing endpoints

---

**BHIV HR Platform Project Structure v3.0.0** - Complete microservices architecture with Phase 3 AI, triple authentication, and comprehensive documentation.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: January 2025 | **Status**: ✅ Production Ready | **Services**: 5/5 Live | **Files**: 100+ | **Lines of Code**: 10,000+