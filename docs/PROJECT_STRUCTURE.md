# BHIV HR Platform - Project Structure

## 📁 Complete Directory Structure

```
bhiv-hr-platform/
├── 📁 services/                    # Microservices Architecture
│   ├── 📁 gateway/                # API Gateway Service (Port 8000)
│   │   ├── 📁 app/
│   │   │   ├── __init__.py        # Package initialization
│   │   │   ├── main.py           # 40-endpoint FastAPI application
│   │   │   └── client_auth.py    # Authentication utilities
│   │   ├── Dockerfile            # Gateway container configuration
│   │   └── requirements.txt      # Gateway dependencies
│   │
│   ├── 📁 agent/                  # AI Matching Service (Port 9000)
│   │   ├── app.py               # Dynamic AI matching engine
│   │   ├── Dockerfile           # Agent container configuration
│   │   └── requirements.txt     # Agent dependencies
│   │
│   ├── 📁 portal/                 # HR Portal Service (Port 8501)
│   │   ├── app.py               # Streamlit HR interface
│   │   ├── batch_upload.py      # Batch processing functionality
│   │   ├── Dockerfile           # Portal container configuration
│   │   └── requirements.txt     # Portal dependencies
│   │
│   ├── 📁 client_portal/          # Client Portal Service (Port 8502)
│   │   ├── app.py               # Streamlit client interface
│   │   ├── auth_service.py      # Enterprise authentication
│   │   ├── Dockerfile           # Client portal container
│   │   └── requirements.txt     # Client portal dependencies
│   │
│   ├── 📁 db/                     # Database Configuration
│   │   └── init_complete.sql    # Complete PostgreSQL schema
│   │
│   └── 📁 semantic_engine/        # AI Processing Engine
│       └── semantic_processor.py # SBERT integration
│
├── 📁 tools/                      # Processing & Automation Tools
│   ├── comprehensive_resume_extractor.py  # Resume parsing (75-96% accuracy)
│   ├── create_demo_jobs.py               # Demo job creation
│   ├── database_sync_manager.py          # Database synchronization
│   ├── auto_sync_watcher.py              # Automatic file watching
│   ├── show_results.py                   # Results visualization
│   └── test_global_matching.py           # Matching algorithm testing
│
├── 📁 tests/                      # Complete Test Suite
│   ├── test_endpoints.py                 # API endpoint testing
│   ├── test_security.py                  # Security feature testing
│   ├── test_client_portal.py             # Client portal testing
│   ├── test_complete_enterprise_api.py   # Enterprise API testing
│   ├── test_structured_api.py            # API structure testing
│   ├── test_week2_all_ports.bat          # Multi-port testing script
│   └── test_week2_enterprise.py          # Enterprise feature testing
│
├── 📁 scripts/                    # Deployment & Operations
│   ├── deploy.sh                         # Local deployment script
│   ├── deploy-cloud.sh                   # Cloud deployment script
│   ├── health-check.sh                   # System health monitoring
│   └── unified-deploy.sh                 # Unified deployment script
│
├── 📁 resume/                     # Resume Files (31 files)
│   ├── AdarshYadavResume.pdf
│   ├── Anmol_Resume.pdf
│   ├── [... 29 more resume files]
│   └── Yash resume1.pdf
│
├── 📁 data/                       # Processed Data
│   └── candidates.csv            # Extracted candidate data (539 records)
│
├── 📁 docs/                       # Documentation
│   ├── DEPLOYMENT.md             # Deployment instructions
│   ├── FILE_ORGANIZATION.md      # File organization guide
│   ├── PROJECT_STRUCTURE.md      # This file
│   ├── REFLECTION.md             # Daily development reflections
│   ├── SECURITY_AUDIT.md         # Security analysis and audit
│   ├── SERVICES_GUIDE.md         # Services configuration guide
│   ├── USER_GUIDE.md             # User manual with screenshots
│   └── BIAS_ANALYSIS.md          # AI bias analysis and mitigation
│
├── 📁 config/                     # Configuration Files
│   └── production.env            # Production environment variables
│
├── 🐳 docker-compose.production.yml      # Production Docker configuration
├── 📋 requirements.txt                   # Main project dependencies
├── 🔧 .env                              # Environment variables
├── 📝 .env.example                      # Environment template
└── 📖 README.md                         # Main project documentation
```

## 🏗️ Architecture Overview

### Service Layer (Port-based Architecture)
- **Gateway (8000)**: FastAPI with 40 endpoints, JWT auth, rate limiting
- **Agent (9000)**: AI matching engine with SBERT integration
- **Portal (8501)**: HR Streamlit interface with dashboard
- **Client Portal (8502)**: Enterprise client interface with 2FA
- **Database (5432)**: PostgreSQL with complete schema

### Data Flow Architecture
```
Resume Files → Tools → Database → API Gateway → Portals
     ↓           ↓         ↓           ↓          ↓
   31 PDFs → Extraction → 539 Records → 40 APIs → 2 UIs
```

### Security Architecture
```
Client Request → Rate Limiting → JWT Auth → API Processing → Response
                      ↓              ↓            ↓
                 DoS Protection → Token Validation → Secure Headers
```

## 📊 Component Details

### Gateway Service (services/gateway/)
**Purpose**: Central API hub with 40 endpoints
**Technology**: FastAPI 3.1.0
**Features**: 
- Core API (3 endpoints)
- Job Management (2 endpoints)  
- Candidate Management (3 endpoints)
- AI Matching (1 endpoint)
- Assessment & Workflow (3 endpoints)
- Analytics (2 endpoints)
- Client Portal API (1 endpoint)
- Security Testing (7 endpoints)
- CSP Management (4 endpoints)
- 2FA (8 endpoints)
- Password Management (6 endpoints)

### AI Agent Service (services/agent/)
**Purpose**: Semantic candidate matching
**Technology**: FastAPI 2.1.0 + SBERT
**Features**:
- Dynamic job-candidate matching
- Multi-factor scoring algorithm
- <0.02s response time
- Bias detection and mitigation

### HR Portal (services/portal/)
**Purpose**: Recruiter dashboard and workflow
**Technology**: Streamlit
**Features**:
- Candidate search and filtering
- AI-powered shortlisting
- Values assessment (5-point scale)
- Batch upload functionality
- Real-time analytics dashboard

### Client Portal (services/client_portal/)
**Purpose**: Enterprise client interface
**Technology**: Streamlit + Enterprise Auth
**Features**:
- Secure client authentication (JWT + bcrypt)
- Job posting interface
- Candidate review workflow
- AI match results visualization
- Analytics and reporting

### Database Layer (services/db/)
**Purpose**: Data persistence and schema management
**Technology**: PostgreSQL 15
**Schema**: Complete normalized schema with:
- Candidates table (539 records)
- Jobs table with requirements
- Assessments and feedback
- User authentication data

## 🔧 Tools & Utilities

### Resume Processing Pipeline
1. **comprehensive_resume_extractor.py**: SBERT-powered extraction (75-96% accuracy)
2. **database_sync_manager.py**: Automated database synchronization
3. **auto_sync_watcher.py**: Real-time file monitoring
4. **show_results.py**: Results visualization and validation

### Testing Framework
- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-service communication
- **Security Tests**: Penetration testing and vulnerability assessment
- **Performance Tests**: Load testing and benchmarking

### Deployment Pipeline
- **Local Development**: Docker Compose with hot reload
- **Production Deployment**: Multi-stage Docker builds
- **Cloud Deployment**: AWS/GCP ready with infrastructure scripts
- **Health Monitoring**: Automated health checks and alerting

## 📈 Performance Characteristics

### Processing Performance
- **Resume Processing**: 1-2 seconds per file
- **API Response Time**: <100ms average
- **AI Matching**: <0.02 seconds per job
- **Database Queries**: Optimized with indexing
- **Concurrent Users**: Multi-user support with connection pooling

### Scalability Design
- **Horizontal Scaling**: Microservices can scale independently
- **Database Scaling**: Read replicas and connection pooling
- **Caching Layer**: Redis integration ready
- **Load Balancing**: Docker Swarm and Kubernetes ready

## 🔒 Security Architecture

### Authentication & Authorization
- **JWT Tokens**: Secure API access with expiration
- **bcrypt Hashing**: Password security with salt
- **2FA Support**: TOTP integration with backup codes
- **Rate Limiting**: DoS protection with configurable limits

### Data Protection
- **Input Validation**: XSS and SQL injection prevention
- **Security Headers**: CSP, XSS Protection, Frame Options
- **HTTPS Enforcement**: TLS 1.3 with HSTS
- **Data Encryption**: At-rest and in-transit encryption

## 🎯 Quality Assurance

### Code Quality
- **Type Hints**: Full Python type annotation
- **Documentation**: Comprehensive inline and external docs
- **Error Handling**: Graceful degradation and user-friendly messages
- **Logging**: Structured logging with different levels

### Testing Coverage
- **Unit Tests**: 85%+ coverage on core functions
- **Integration Tests**: End-to-end workflow validation
- **Security Tests**: Automated vulnerability scanning
- **Performance Tests**: Load testing with realistic data

## 🚀 Deployment Strategy

### Development Environment
```bash
docker-compose -f docker-compose.production.yml up -d
```

### Production Environment
```bash
./scripts/unified-deploy.sh production
```

### Cloud Deployment
```bash
./scripts/deploy-cloud.sh aws  # or gcp
```

## 📋 Maintenance & Operations

### Monitoring
- **Health Checks**: Automated service health monitoring
- **Metrics Collection**: Performance and usage metrics
- **Log Aggregation**: Centralized logging with search
- **Alerting**: Automated alerts for critical issues

### Backup & Recovery
- **Database Backups**: Automated daily backups
- **Configuration Backups**: Version-controlled configs
- **Disaster Recovery**: Multi-region deployment ready
- **Data Migration**: Automated migration scripts

---

**Total Files**: 47 essential files
**Total Lines of Code**: ~15,000 lines
**Services**: 5 microservices
**Endpoints**: 40 API endpoints
**Test Coverage**: 85%+
**Documentation**: 100% coverage

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*