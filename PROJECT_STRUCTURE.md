# 🏗️ BHIV HR Platform - Project Structure

## 📁 Current Folder Organization

```
bhiv-hr-platform/
├── 📋 PROJECT_STRUCTURE.md          # This file - Complete architecture guide
├── 📋 README.md                     # Main project documentation
├── 📋 DEPLOYMENT_STATUS.md          # Current deployment status

├── 🐳 docker-compose.production.yml # Docker orchestration
├── 📊 .env.example                  # Environment template
│
├── 🔧 services/                     # Microservices Architecture
│   ├── 🌐 gateway/                  # API Gateway Service (Port 8000)
│   │   ├── 📱 app/
│   │   │   ├── main.py              # FastAPI app (49 endpoints)
│   │   │   ├── monitoring.py        # Advanced monitoring system
│   │   │   └── __init__.py          # Package initialization
│   │   ├── 📋 requirements.txt      # Python dependencies
│   │   ├── 🐳 Dockerfile           # Container configuration
│   │   └── 📊 logs/                # Application logs
│   │
│   ├── 🔧 shared/                   # ✅ Enhanced Monitoring Infrastructure
│   │   ├── logging_config.py        # Centralized structured logging
│   │   ├── health_checks.py         # Comprehensive health validation
│   │   └── error_tracking.py        # Advanced error analysis
│   │
│   ├── 🎯 portal/                   # HR Dashboard (Port 8501)
│   │   ├── app.py                   # Main Streamlit application
│   │   ├── batch_upload.py          # ✅ FIXED - Batch upload functionality
│   │   ├── 📋 requirements.txt      # Dependencies
│   │   └── 🐳 Dockerfile           # Container config
│   │
│   ├── 👥 client_portal/            # Client Interface (Port 8502)
│   │   ├── app.py                   # Client-facing portal
│   │   ├── auth_service.py          # ⚠️ REDUNDANT - 300+ lines for simple login
│   │   ├── 📋 requirements.txt      # Dependencies
│   │   └── 🐳 Dockerfile           # Container config
│   │
│   ├── 🤖 agent/                    # AI Matching Engine (Port 9000)
│   │   ├── app.py                   # AI matching service
│   │   ├── 📋 requirements.txt      # Dependencies
│   │   └── 🐳 Dockerfile           # Container config
│   │
│   ├── 🗄️ db/                       # Database Schema
│   │   ├── init_complete.sql        # ✅ Complete database setup
│   │   └── 🐳 Dockerfile           # Database container
│   │
│   └── 🔧 semantic_engine/          # ⚠️ UNUSED - Legacy AI service
│       └── semantic_processor.py    # ⚠️ Not integrated
│
├── 🛠️ tools/                        # Data Processing Tools
│   ├── comprehensive_resume_extractor.py  # Resume processing
│   ├── dynamic_job_creator.py       # Job creation utility
│   ├── database_sync_manager.py     # Database synchronization
│   └── auto_sync_watcher.py         # Auto-sync monitoring
│
├── 🧪 tests/                        # Test Suite
│   ├── test_endpoints.py            # API functionality tests
│   ├── test_security.py             # Security validation tests
│   ├── test_client_portal.py        # Portal integration tests
│   ├── test_enhanced_monitoring.py  # ✅ Full monitoring test suite
│   ├── test_enhanced_monitoring_simple.py # ✅ Simplified monitoring tests (6/6 passed)
│   └── test_final_verification.py   # Complete system tests
│
├── 📊 data/                         # Data Storage
│   └── candidates.csv               # ✅ Real extracted candidate data (68+ records)
│
├── 📁 resume/                       # Resume Files Storage (31 files)
│   ├── *.pdf                       # ✅ 30 PDF resume files processed
│   └── *.docx                      # ✅ 1 DOCX file processed
│
├── 📚 docs/                         # Documentation
│   ├── 📁 archive/                 # Archived documentation
│   ├── 📁 guides/                  # User guides
│   │   └── LIVE_DEMO.md            # Live platform demo guide
│   ├── BIAS_ANALYSIS.md            # AI bias analysis & mitigation
│   ├── CURRENT_FEATURES.md         # ✅ Complete feature list
│   ├── ENHANCED_MONITORING_RESOLUTION.md # ✅ Enterprise monitoring system
│   ├── QUICK_START_GUIDE.md        # ✅ 5-minute setup guide
│   ├── REFLECTION.md               # ✅ Daily development reflections
│   ├── SECURITY_AUDIT.md           # Security assessment
│   ├── SERVICES_GUIDE.md           # Service architecture
│   ├── USER_GUIDE.md               # Complete user manual
│   └── batch_upload_verification_guide.md  # Batch upload guide
│
├── ⚙️ config/                       # Configuration Files
│   ├── .env.render                 # ✅ Render platform config
│   ├── production.env              # Production settings
│   └── render-deployment.yml       # ✅ Render deployment config
│
├── 🚀 scripts/                      # Deployment Scripts
│   ├── unified-deploy.sh            # ✅ Unified deployment
│   └── health-check.sh              # ✅ Health monitoring
│
├── 📁 deployment/                   # ✅ Deployment Documentation
│   ├── DEPLOYMENT_GUIDE.md          # General deployment guide
│   └── RENDER_DEPLOYMENT_GUIDE.md   # Render-specific guide
│
├── 📋 .env                          # ✅ Local environment config
└── 📋 .env.example                  # Environment template
```

## 🔄 Recent Updates (January 2025)

### ✅ **Fixed Components**
- **Batch Upload**: ✅ Fixed container paths (/app/resume/) and directory structure
- **API Gateway**: ✅ 49 endpoints with enhanced monitoring and security
- **Database Integration**: ✅ Resolved schema issues and email constraints
- **AI Matching**: ✅ Differentiated scoring with real candidate data
- **Skills Match Error**: ✅ Fixed TypeError in portal displays
- **Mock Data Replacement**: ✅ All 68+ candidates from real resume files
- **Client-HR Sync**: ✅ Real-time job sharing between portals
- **Enhanced Monitoring**: ✅ Enterprise-grade logging, health checks, error tracking

### 🆕 **New Features**
- **Enhanced Monitoring System**: ✅ Centralized logging, health checks, error correlation
- **Structured Logging**: ✅ JSON logging with ELK integration and correlation IDs
- **Advanced Health Checks**: ✅ Database, service, and resource validation
- **Error Tracking**: ✅ Classification, pattern detection, automated alerting
- **Dual Portal System**: ✅ HR and Client portals with real-time sync
- **Values Assessment**: ✅ 5-point evaluation system with feedback
- **Export Reports**: ✅ Comprehensive reports with assessments and shortlists
- **Workflow Organization**: ✅ Step-by-step HR process navigation
- **Dynamic Dashboards**: ✅ Live data from database, no hardcoded values

## 📊 Service Architecture

| Service | Technology | Port | Status | Purpose |
|---------|------------|------|--------|---------|
| **API Gateway** | FastAPI 3.1.0 | 8000 | 🟢 Live | REST API Backend (49 endpoints) |
| **HR Portal** | Streamlit | 8501 | 🟢 Live | HR Dashboard |
| **Client Portal** | Streamlit | 8502 | 🟢 Live | Client Interface |
| **AI Agent** | FastAPI 2.1.0 | 9000 | 🟢 Live | Candidate Matching |
| **Database** | PostgreSQL 17 | 5432 | 🟢 Live | Data Storage |
| **Monitoring** | Shared Infrastructure | - | 🟢 Live | Enterprise Observability |

## 🔧 Key Directories Explained

### `/services/` - Microservices
- **gateway/**: Central API with 49 endpoints, enhanced monitoring, security
- **shared/**: Enterprise monitoring infrastructure (logging, health checks, error tracking)
- **portal/**: HR dashboard with workflow management
- **client_portal/**: Client-facing job posting interface
- **agent/**: AI matching engine with semantic analysis
- **db/**: Database schema and initialization

### `/tools/` - Processing Utilities
- **Resume Extraction**: PDF/DOCX to structured data
- **Job Creation**: Dynamic job posting generation
- **Database Sync**: Real-time data synchronization
- **Auto Monitoring**: Continuous system watching

### `/tests/` - Quality Assurance
- **API Tests**: Endpoint functionality validation
- **Security Tests**: Authentication and authorization
- **Monitoring Tests**: Enhanced monitoring system validation (6/6 passed)
- **Integration Tests**: Cross-service communication
- **System Tests**: End-to-end workflow validation

### `/docs/` - Documentation
- **Technical Guides**: Architecture and implementation
- **User Manuals**: Step-by-step usage instructions
- **Security Analysis**: Bias mitigation and audit reports
- **API Documentation**: Endpoint specifications

## 🚀 Deployment Structure

### **Production Environment**
- **Platform**: Render Cloud (Oregon, US West)
- **Cost**: $0/month (Free tier)
- **SSL**: Automatic HTTPS certificates
- **Monitoring**: Real-time health checks
- **Scaling**: Auto-scaling enabled

### **Local Development**
- **Docker Compose**: Multi-service orchestration
- **Hot Reload**: Development mode with live updates
- **Database**: Local PostgreSQL instance
- **Networking**: Internal service communication

## 📈 Current Metrics

- **Total Services**: 5 (Database + 4 Web Services) + Enhanced Monitoring
- **API Endpoints**: 49 interactive endpoints (enhanced monitoring)
- **Test Coverage**: 6 comprehensive test suites (including monitoring)
- **Documentation**: 9+ detailed guides (including monitoring resolution)
- **Resume Processing**: ✅ 31 files successfully processed
- **Candidate Database**: ✅ 68+ candidates with complete real data
- **Monitoring Coverage**: ✅ 100% enterprise-grade observability

## 🔄 Workflow Integration

```
Client Portal → API Gateway → Database ← HR Portal
     ↓              ↓           ↓         ↓
Job Posting → Job Storage → AI Matching → Candidate Review
     ↓              ↓           ↓         ↓
Resume Upload → Processing → Extraction → Assessment
```

This structure supports the complete HR workflow from job posting to candidate hiring with real-time synchronization and comprehensive reporting.