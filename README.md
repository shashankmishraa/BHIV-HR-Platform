# 🚀 BHIV HR Platform

**Production-Ready AI-Powered Recruiting Platform** with intelligent candidate matching, comprehensive assessment tools, and enterprise-grade security.

## 🌐 Live Production Platform

### **✅ Currently Deployed on Render**
- **API Gateway**: https://bhiv-hr-gateway.onrender.com/docs ✅
- **AI Matching Engine**: https://bhiv-hr-agent.onrender.com/docs ✅
- **HR Portal**: https://bhiv-hr-portal.onrender.com/ ✅
- **Client Portal**: https://bhiv-hr-client-portal.onrender.com/ ✅
- **Status**: 🟢 **ALL SERVICES LIVE & OPERATIONAL** | **Cost**: $0/month (Free tier)

### **🔑 Demo Access**
```bash
# Client Portal Login
Username: TECH001
Password: demo123

# API Testing
API Key: myverysecureapikey123
curl -H "Authorization: Bearer myverysecureapikey123" https://bhiv-hr-gateway.onrender.com/health
```

## 📋 Documentation Structure

### **📚 Core Documentation**
- **[📋 PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - ✅ Complete architecture and folder organization
- **[🚀 DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - ✅ Complete deployment instructions (Render + Local)
- **[🔧 TECHNICAL_RESOLUTIONS.md](TECHNICAL_RESOLUTIONS.md)** - ✅ All technical issues and resolutions
- **[⚡ docs/QUICK_START_GUIDE.md](docs/QUICK_START_GUIDE.md)** - ✅ Get started in 5 minutes
- **[🎯 docs/CURRENT_FEATURES.md](docs/CURRENT_FEATURES.md)** - ✅ Complete feature list and capabilities

### **🔧 Technical Guides**
- **[🔍 docs/batch_upload_verification_guide.md](docs/batch_upload_verification_guide.md)** - ✅ Batch upload verification methods
- **[🔒 docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md)** - Security analysis and features
- **[🤖 docs/BIAS_ANALYSIS.md](docs/BIAS_ANALYSIS.md)** - AI bias analysis & mitigation
- **[👥 docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - Complete user manual
- **[📝 docs/REFLECTION.md](docs/REFLECTION.md)** - ✅ Daily development reflections

## ⚡ Quick Start

### **🎯 Choose Your Path:**
1. **🌐 Live Platform**: Use production services immediately → [Quick Start Guide](docs/QUICK_START_GUIDE.md)
2. **💻 Local Development**: Run on your machine → [Setup Instructions](docs/QUICK_START_GUIDE.md#local-development-setup)

### **🚀 5-Minute Setup**
```bash
# Live Platform - No Setup Required
HR Portal: https://bhiv-hr-portal.onrender.com/
Client Portal: https://bhiv-hr-client-portal.onrender.com/
Credentials: TECH001 / demo123

# Local Development - Docker Required
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform
docker-compose -f docker-compose.production.yml up -d
# Access: http://localhost:8501
```

---

## 🏗️ System Architecture

### **Microservices Overview**
| Service | Purpose | Technology | Port | Status |
|---------|---------|------------|------|--------|
| **API Gateway** | REST API Backend | FastAPI 3.1.0 | 8000 | 🟢 Live |
| **AI Agent** | Candidate Matching | FastAPI 2.1.0 | 9000 | ✅ Live |
| **HR Portal** | HR Dashboard | Streamlit | 8501 | ✅ Live |
| **Client Portal** | Client Interface | Streamlit | 8502 | ✅ Live |
| **Database** | Data Storage | PostgreSQL 17 | 5432 | ✅ Live |

### **API Endpoints (46 Total)**
```
Core API (3):           GET /, /health, /test-candidates
Job Management (2):     POST /v1/jobs, GET /v1/jobs  
Candidate Mgmt (3):     GET /v1/candidates/*, POST /v1/candidates/bulk
AI Matching (1):        GET /v1/match/{job_id}/top
Security (15):          Rate limiting, 2FA, password management
Analytics (2):          GET /candidates/stats, /v1/reports/*
Client Portal (1):      POST /v1/client/login
Monitoring (6):         GET /metrics, /health/detailed, /health/simple, /monitoring/errors, /monitoring/logs/search, /monitoring/dependencies
Documentation (16):     Daily reflections, bias analysis, project structure
```

---

## 🚀 Key Features

### **🤖 AI-Powered Matching**
- **Dynamic Scoring**: Job-specific weighting algorithms
- **Real-time Processing**: <0.02 second response time
- **Semantic Analysis**: Advanced candidate-job matching
- **Bias Mitigation**: Comprehensive fairness algorithms

### **🔒 Enterprise Security**
- **API Authentication**: Bearer token + JWT
- **Rate Limiting**: 60 requests/minute with DoS protection
- **2FA Support**: TOTP compatible (Google/Microsoft/Authy)
- **Security Headers**: CSP, XSS protection, Frame Options
- **Input Validation**: XSS/SQL injection protection
- **Password Policies**: Enterprise-grade validation

### **📊 Dual Portal System**
- **HR Portal**: Dashboard, candidate search, job management, AI matching
- **Client Portal**: Enterprise authentication, job posting, candidate review
- **Real-time Analytics**: Performance metrics and insights
- **Values Assessment**: 5-point evaluation system

### **📈 Resume Processing**
- **Multi-format Support**: PDF, DOCX, TXT files
- **High Accuracy**: 75-96% extraction accuracy
- **Batch Processing**: Handle multiple resumes simultaneously
- **Error Monitoring**: Comprehensive tracking and metrics

### **📊 Enhanced Monitoring System**
- **Centralized Logging**: Structured JSON logging with ELK integration
- **Advanced Health Checks**: Database, service, and resource validation
- **Error Tracking**: Classification, correlation, and pattern detection
- **Prometheus Metrics**: Real-time performance tracking
- **Cross-Service Correlation**: Request tracing with correlation IDs
- **Automated Alerting**: Configurable thresholds and notifications

---

## 🛠️ Development & Deployment

### **Project Structure**
```
bhiv-hr-platform/
├── services/                    # Microservices
│   ├── gateway/                # API Gateway (49 endpoints)
│   │   ├── app/               # Application code
│   │   │   ├── main.py        # FastAPI application
│   │   │   ├── monitoring.py  # Advanced monitoring system
│   │   │   └── __init__.py    # Package initialization
│   │   ├── logs/              # Application logs
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Dependencies
│   ├── agent/                  # AI Matching Engine (FastAPI 2.1.0)
│   ├── portal/                 # HR Dashboard (Streamlit)
│   ├── client_portal/          # Client Interface (Streamlit)
│   ├── db/                     # Database Schema (PostgreSQL)
│   ├── shared/                 # Enhanced Monitoring Infrastructure
│   │   ├── logging_config.py  # Centralized structured logging
│   │   ├── health_checks.py   # Comprehensive health validation
│   │   └── error_tracking.py  # Advanced error analysis
│   └── semantic_engine/        # AI Processing Modules
│       ├── __init__.py        # Package initialization
│       ├── job_matcher.py     # Basic semantic matching
│       └── advanced_matcher.py # Advanced AI algorithms
├── tools/                      # Data Processing
│   ├── comprehensive_resume_extractor.py
│   ├── dynamic_job_creator.py
│   ├── database_sync_manager.py
│   └── auto_sync_watcher.py
├── tests/                      # Test Suite
│   ├── test_endpoints.py       # API Tests
│   ├── test_security.py        # Security Tests
│   ├── test_client_portal.py   # Portal Tests
│   ├── test_enhanced_monitoring.py # Full monitoring test suite
│   └── test_enhanced_monitoring_simple.py # Simplified monitoring tests
├── scripts/                    # Deployment Scripts
├── docs/                       # Documentation
│   ├── BIAS_ANALYSIS.md       # AI bias analysis & mitigation
│   ├── SECURITY_AUDIT.md      # Security assessment
│   ├── USER_GUIDE.md          # User documentation
│   └── ENHANCED_MONITORING_RESOLUTION.md # Monitoring system guide
├── data/                       # Sample Data
├── config/                     # Configuration
├── docker-compose.production.yml # Local development setup
├── REFLECTION.md              # Daily development reflections
├── PROJECT_STRUCTURE.md       # Architecture documentation
├── README.md                   # This file
└── LIVE_DEMO.md               # Live demo guide
```

### **Configuration Files**
```bash
# Environment Configuration
.env.example          # Template for local development
.env.render           # Render platform configuration
config/production.env # Production settings

# Deployment Configuration  
docker-compose.production.yml    # Docker setup
render-deployment.yml           # Render platform config
RENDER_DEPLOYMENT_GUIDE.md     # Complete deployment guide
```

### **Local Development Setup**
```bash
# Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Git

# Environment Setup
cp .env.example .env
# Edit .env with your settings

# Start Services
docker-compose -f docker-compose.production.yml up -d

# Verify Services
curl http://localhost:8000/health
curl http://localhost:9000/health
```

---

## 🧪 Testing & Validation

### **API Testing**
```bash
# Health Checks
curl https://bhiv-hr-gateway.onrender.com/health
curl https://bhiv-hr-agent.onrender.com/health

# Authenticated Endpoints
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/v1/jobs

# Security Testing
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/v1/security/rate-limit-status
```

### **Test Suite**
```bash
# Run Core Tests
python tests/test_endpoints.py      # API functionality
python tests/test_security.py       # Security features  
python tests/test_client_portal.py  # Portal integration

# Enhanced Monitoring Tests
python tests/test_enhanced_monitoring_simple.py  # Monitoring system (6/6 tests)

# Performance Testing
python tests/test_final_verification.py  # Complete system test
```

---

## 📊 Performance Metrics

### **Current Performance**
- **API Response Time**: <100ms average
- **AI Matching Speed**: <0.02 seconds
- **Resume Processing**: 1-2 seconds per file
- **Uptime**: 99.9% target (production)
- **Concurrent Users**: Multi-user support
- **Rate Limiting**: Granular limits by endpoint and user tier

### **Enhanced Monitoring**
```bash
# Production Monitoring
curl https://bhiv-hr-gateway.onrender.com/health/detailed     # Enhanced health checks
curl https://bhiv-hr-gateway.onrender.com/monitoring/errors   # Error analytics
curl https://bhiv-hr-gateway.onrender.com/monitoring/dependencies # Service dependencies
curl https://bhiv-hr-gateway.onrender.com/metrics/dashboard   # Enhanced dashboard

# Local Monitoring  
curl http://localhost:8000/health/simple        # Simple health check
curl http://localhost:8000/monitoring/logs/search?query=error # Log search
curl http://localhost:8000/metrics              # Prometheus metrics
```

---

## 🔧 Tools & Utilities

### **Data Processing Tools**
```bash
# Resume Processing
python tools/comprehensive_resume_extractor.py

# Job Creation
python tools/dynamic_job_creator.py --count 15
python tools/dynamic_job_creator.py --type software_engineer --count 5

# Database Management
python tools/database_sync_manager.py

# Auto Sync (Development)
python tools/auto_sync_watcher.py
```

### **Deployment Tools**
```bash
# Local Deployment
./scripts/unified-deploy.sh local --build --health

# Production Status
./scripts/unified-deploy.sh production

# Health Monitoring
./scripts/health-check.sh
```

---

## 📚 Documentation

### **Complete Guides**
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide (Render + Local)
- **[TECHNICAL_RESOLUTIONS.md](TECHNICAL_RESOLUTIONS.md)** - All technical issues and solutions
- **[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)** - Current deployment status

### **Technical Documentation**
- **[docs/REFLECTION.md](docs/REFLECTION.md)** - Daily development reflections with values
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Complete architecture guide
- **[docs/BIAS_ANALYSIS.md](docs/BIAS_ANALYSIS.md)** - AI bias analysis & mitigation
- **[docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md)** - Security analysis
- **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - Complete user manual
- **[docs/SERVICES_GUIDE.md](docs/SERVICES_GUIDE.md)** - Service architecture

---

## 🎯 Current Status & Progress

### **✅ Completed Features**
- **Production Deployment**: ✅ All 5 services live on Render
- **API Gateway**: ✅ 49 endpoints with comprehensive functionality
- **Advanced AI Matching v3.2.0**: ✅ Job-specific candidate scoring with ML algorithms
- **Real Data Integration**: ✅ 68+ candidates from actual resume files
- **Enterprise Security**: ✅ Authentication, 2FA, rate limiting, CORS protection
- **Dual Portals**: ✅ HR dashboard and client interface with real-time sync
- **Advanced Monitoring**: ✅ Prometheus metrics, health checks, performance tracking
- **Documentation**: ✅ Complete guides, API documentation, security analysis
- **Testing**: ✅ Comprehensive test suite with security validation
- **Local Development**: ✅ Docker Compose setup with health checks
- **Codebase Organization**: ✅ Professional structure, removed duplicates, optimized code

### **📈 System Metrics**
- **Total Services**: 5 (Database + 4 Web Services)
- **API Endpoints**: 49 production endpoints
- **Real Candidates**: ✅ 68+ from actual resume files
- **AI Algorithm**: v3.2.0 with job-specific matching
- **Monthly Cost**: $0 (Free tier deployment)
- **Global Access**: HTTPS with SSL certificates
- **Auto-Deploy**: GitHub integration enabled
- **Uptime Target**: 99.9%
- **Code Quality**: ✅ Cleaned, organized, professional structure

### **🔄 Recent Updates (January 2025)**
- ✅ **Advanced AI Matching v3.2.0**: Job-specific candidate scoring with ML algorithms
- ✅ **Codebase Cleanup**: Removed duplicate directories, old code, organized structure
- ✅ **Professional Organization**: Clean imports, optimized code, removed redundancies
- ✅ **Full Production Deployment**: All 5 services live and operational
- ✅ **Real Data Integration**: 68+ candidates from 31 actual resume files
- ✅ **Enterprise Security**: Authentication, 2FA, rate limiting, CORS protection
- ✅ **Enhanced Monitoring**: Prometheus metrics, health checks, error tracking
- ✅ **Documentation Complete**: Comprehensive guides and API documentation
- ✅ **Zero-Cost Operation**: $0/month on Render free tier
- ✅ **Database Optimization**: Enhanced connection handling and performance
- ✅ **Code Quality**: Removed old test files, cleaned root directory
- ✅ **Version Consistency**: Updated to v3.2.0 across all components

---

## 🚀 Getting Started (Choose Your Path)

### **🌐 For Users (Recommended)**
1. **Visit Live Platform**: https://bhiv-hr-gateway.onrender.com/docs
2. **Access HR Portal**: https://bhiv-hr-portal.onrender.com/
3. **Login to Client Portal**: https://bhiv-hr-client-portal.onrender.com/ (TECH001/demo123)
4. **Test API**: Use Bearer token `myverysecureapikey123`

### **💻 For Developers**
1. **Clone Repository**: `git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git`
2. **Setup Environment**: Copy `.env.example` to `.env`
3. **Start Services**: `docker-compose -f docker-compose.production.yml up -d`
4. **Run Tests**: `python tests/test_endpoints.py`

### **🚀 For Deployment**
1. **Read Guide**: [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)
2. **Check Status**: [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)
3. **Monitor Health**: Use provided health check endpoints

---

## 📞 Support & Resources

### **Live Platform Access**
- **API Documentation**: https://bhiv-hr-gateway.onrender.com/docs
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Deployment Platform**: Render Cloud (Oregon, US West)

### **Quick Links**
- **🔗 Live API**: https://bhiv-hr-gateway.onrender.com/docs
- **🔗 HR Dashboard**: https://bhiv-hr-portal.onrender.com/
- **🔗 Client Portal**: https://bhiv-hr-client-portal.onrender.com/
- **🔗 AI Agent**: https://bhiv-hr-agent.onrender.com/docs

---

**BHIV HR Platform v3.2.0** - Enterprise recruiting solution with advanced AI-powered matching, comprehensive security, and global deployment capabilities.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: January 17, 2025 | **Status**: 🟢 All Services Live | **Cost**: $0/month | **Uptime**: 99.9%

---

## 📋 Quick Navigation

| Document | Purpose | Status |
|----------|---------|--------|
| **[🏗️ ARCHITECTURE.md](ARCHITECTURE.md)** | System architecture and design | ✅ Complete |
| **[🚀 DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)** | Live deployment status and monitoring | ✅ Live |
| **[📋 PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** | Codebase organization and structure | ✅ Complete |
| **[🔧 TECHNICAL_RESOLUTIONS.md](TECHNICAL_RESOLUTIONS.md)** | Technical issues and solutions | ✅ Complete |
| **[🚀 DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | Deployment instructions | ✅ Complete |