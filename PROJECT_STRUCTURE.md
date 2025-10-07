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
│   │   │   ├── main.py              # FastAPI app (48 endpoints)
│   │   │   ├── monitoring.py        # Advanced monitoring system
│   │   │   └── __init__.py          # Package initialization
│   │   ├── 📋 requirements.txt      # Python dependencies
│   │   ├── 🐳 Dockerfile           # Container configuration
│   │   └── 📊 logs/                # Application logs
│   │
│   ├── 🎯 portal/                   # HR Dashboard (Port 8501)
│   │   ├── app.py                   # Main Streamlit application
│   │   ├── batch_upload.py          # ✅ Batch upload functionality
│   │   ├── 📋 requirements.txt      # Dependencies
│   │   └── 🐳 Dockerfile           # Container config
│   │
│   ├── 👥 client_portal/            # Client Interface (Port 8502)
│   │   ├── app.py                   # Client-facing portal
│   │   ├── auth_service.py          # Authentication service
│   │   ├── 📋 requirements.txt      # Dependencies
│   │   └── 🐳 Dockerfile           # Container config
│   │
│   ├── 🤖 agent/                    # AI Matching Engine (Port 9000)
│   │   ├── app.py                   # AI matching service (5 endpoints)
│   │   ├── 📋 requirements.txt      # Dependencies
│   │   └── 🐳 Dockerfile           # Container config
│   │
│   └── 🗄️ db/                       # Database Schema
│       ├── consolidated_schema.sql  # ✅ Complete database setup
│       └── 🐳 Dockerfile           # Database container
│
├── 📚 docs/                         # Documentation (Organized)
│   ├── 📁 deployment/              # Deployment guides
│   │   ├── DEPLOYMENT_GUIDE.md     # General deployment guide
│   │   └── RENDER_DEPLOYMENT_GUIDE.md # Render-specific guide
│   ├── 📁 security/                # Security & Analysis
│   │   ├── SECURITY_AUDIT.md       # Security assessment
│   │   └── BIAS_ANALYSIS.md        # AI bias analysis & mitigation
│   ├── 📁 testing/                 # Testing Documentation
│   │   ├── COMPLETE_API_TESTING_GUIDE.md # API testing guide
│   │   └── TESTING_STRATEGY.md     # Testing strategies
│   ├── 📁 guides/                  # User guides
│   │   └── LIVE_DEMO.md            # Live platform demo guide
│   ├── CURRENT_FEATURES.md         # ✅ Complete feature list
│   ├── QUICK_START_GUIDE.md        # ✅ 5-minute setup guide
│   ├── REFLECTION.md               # ✅ Daily development reflections
│   ├── SERVICES_GUIDE.md           # Service architecture
│   └── USER_GUIDE.md               # Complete user manual
│
├── 🧪 tests/                        # Essential Tests Only
│   ├── 📁 unit/                    # Unit tests
│   ├── 📁 integration/             # Integration tests
│   ├── 📁 security/                # Security tests
│   ├── test_endpoints.py           # Core API tests
│   ├── test_security.py            # Security validation
│   ├── test_client_portal.py       # Portal tests
│   └── run_all_tests.py            # Test runner
│
├── 🚀 scripts/                      # Organized Scripts
│   ├── 📁 deployment/              # Deployment scripts
│   │   ├── unified-deploy.sh       # ✅ Unified deployment
│   │   └── health-check.sh         # ✅ Health monitoring
│   ├── 📁 maintenance/             # Maintenance utilities
│   │   ├── render-environment-audit.py # Environment audit
│   │   └── production-validation.py # Production validation
│   ├── apply_database_schema_fixes.py # Database fixes
│   ├── setup-environment.py        # Environment setup
│   └── update_documentation.py     # Documentation updates
│
├── 🛠️ tools/                        # Data Processing Tools
│   ├── dynamic_job_creator.py      # Job creation utility
│   ├── database_sync_manager.py    # Database synchronization
│   └── auto_sync_watcher.py        # Auto-sync monitoring
│
├── ⚙️ config/                       # Configuration Files
│   ├── 📁 environments/            # Environment configs
│   ├── .env.render                 # ✅ Render platform config
│   ├── production.env              # Production settings
│   └── render-deployment.yml       # ✅ Render deployment config
│
├── 📊 data/                         # Data Storage
│   └── candidates.csv              # ✅ Real extracted candidate data
│
├── 📁 resume/                       # Resume Files Storage (31 files)
│   ├── *.pdf                      # ✅ 30 PDF resume files processed
│   └── *.docx                     # ✅ 1 DOCX file processed
│
├── 📁 environments/                 # Environment Templates
│   ├── local/                     # Local development
│   ├── production/                 # Production settings
│   ├── shared/                     # Shared configurations
│   └── staging/                    # Staging environment
│
├── 📋 .env                         # ✅ Local environment config
└── 📋 .env.example                 # Environment template
```

## 🔄 Recent Updates (October 2025)

### ✅ **Codebase Restructure & Optimization**
- **File Elimination**: ✅ Removed 55+ redundant analysis/audit files
- **Professional Structure**: ✅ Organized docs/, tests/, scripts/ by category
- **Clean Architecture**: ✅ Streamlined project structure following best practices
- **API Documentation**: ✅ Complete documentation for all 53 endpoints (48 Gateway + 5 Agent)
- **Code Quality**: ✅ Production-ready with comprehensive error handling
- **Essential Testing**: ✅ Focused test suite with unit, integration, and security tests

### ✅ **Enhanced Features**
- **AI Matching Engine**: ✅ Differentiated scoring algorithm with optimized performance
- **Advanced Security**: ✅ 2FA, CSP policies, comprehensive input validation
- **Portal Integration**: ✅ Real-time sync between HR and Client portals
- **Monitoring System**: ✅ Prometheus metrics, health checks, performance tracking
- **Database Optimization**: ✅ Proper constraints, indexing, and real data (112K+ candidates)
- **Production Deployment**: ✅ All 5 services live and operational on Render

## 📊 Service Architecture

| Service | Technology | Port | Status | Purpose |
|---------|------------|------|--------|---------|
| **API Gateway** | FastAPI 3.1.0 | 8000 | 🟢 Live | REST API Backend |
| **HR Portal** | Streamlit | 8501 | 🟢 Live | HR Dashboard |
| **Client Portal** | Streamlit | 8502 | 🟢 Live | Client Interface |
| **AI Agent** | FastAPI 2.1.0 | 9000 | 🟢 Live | Candidate Matching |
| **Database** | PostgreSQL 17 | 5432 | 🟢 Live | Data Storage |

## 🔧 Key Directories Explained

### `/services/` - Microservices
- **gateway/**: Central API with 46 endpoints, monitoring, security
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

- **Total Services**: 5 (Database + 4 Web Services)
- **API Endpoints**: 53 interactive endpoints (48 Gateway + 5 Agent) - 100% functional
- **Test Coverage**: Essential test suites (unit, integration, security)
- **Documentation**: Organized by category (deployment, security, testing)
- **Resume Processing**: ✅ 31 files successfully processed
- **Candidate Database**: ✅ 112K+ candidates with complete real data
- **Code Quality**: ✅ Production-ready with comprehensive error handling
- **Project Structure**: ✅ Professional organization, 55+ redundant files eliminated
- **File Organization**: ✅ Clean structure following industry best practices

## 🔄 Workflow Integration

```
Client Portal → API Gateway → Database ← HR Portal
     ↓              ↓           ↓         ↓
Job Posting → Job Storage → AI Matching → Candidate Review
     ↓              ↓           ↓         ↓
Resume Upload → Processing → Extraction → Assessment
```

This structure supports the complete HR workflow from job posting to candidate hiring with real-time synchronization and comprehensive reporting.