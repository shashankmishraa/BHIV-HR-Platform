# 📁 BHIV HR Platform - File Organization Guide

## 🏗️ Project Structure Overview

The BHIV HR Platform follows a microservices architecture with clear separation of concerns and organized file structure for maintainability and scalability.

## 📂 Directory Structure

### 🔧 `/services/` - Microservices Architecture
Contains all containerized services that make up the platform.

#### 🌐 `/services/gateway/` - API Gateway Service (Port 8000)
```
gateway/
├── app/
│   ├── main.py              # Main FastAPI application with 16 endpoints
│   ├── db/
│   │   └── schemas.py       # Pydantic models for API validation
│   └── services/
│       └── values_scoring.py # Values assessment logic
├── client_auth.py           # Client authentication utilities
├── Dockerfile              # Container configuration
└── requirements.txt         # Python dependencies
```
**Purpose**: Central API hub handling all HTTP requests, authentication, and routing.

#### 🤖 `/services/agent/` - AI Matching Service (Port 9000)
```
agent/
├── app.py                   # AI matching algorithms and semantic processing
├── Dockerfile              # Container configuration
└── requirements.txt         # AI/ML dependencies
```
**Purpose**: Handles candidate-job matching using AI algorithms and semantic analysis.

#### 👥 `/services/portal/` - HR Portal Service (Port 8501)
```
portal/
├── app.py                   # Streamlit HR interface with dashboard
├── batch_upload.py          # Batch resume processing module
├── Dockerfile              # Container configuration
└── requirements.txt         # Streamlit dependencies
```
**Purpose**: HR team interface for candidate management, job creation, and analytics.

#### 🏢 `/services/client_portal/` - Client Portal Service (Port 8502)
```
client_portal/
├── app.py                   # Streamlit client interface
├── auth_service.py          # Enterprise authentication service
├── app_fixed.py            # Backup/fixed version
├── Dockerfile              # Container configuration
└── requirements.txt         # Client portal dependencies
```
**Purpose**: Client interface for job posting, candidate review, and reports.

#### 🗄️ `/services/db/` - Database Configuration
```
db/
└── init.sql                 # Database initialization scripts
```
**Purpose**: PostgreSQL database setup and initial schema.

#### 🧠 `/services/semantic_engine/` - Semantic Processing
```
semantic_engine/
└── semantic_processor.py    # SBERT-based semantic analysis
```
**Purpose**: Advanced semantic processing for intelligent candidate matching.

### 🛠️ `/tools/` - Processing & Automation Tools
```
tools/
├── comprehensive_resume_extractor.py  # Main resume processing engine
├── database_sync_manager.py          # Database synchronization
├── auto_sync_watcher.py              # File monitoring and auto-processing
├── create_demo_jobs.py               # Demo data generation
└── show_results.py                   # Results display utility
```
**Purpose**: Automation tools for resume processing, data sync, and system maintenance.

### 🧪 `/tests/` - Test Suite
```
tests/
└── test_endpoints.py         # API endpoint testing (9/9 tests passing)
```
**Purpose**: Comprehensive testing suite for API validation and system verification.

### 📊 `/data/` - Processed Data
```
data/
└── candidates.csv            # Extracted and processed candidate data
```
**Purpose**: Stores processed candidate information in structured format.

### 📄 `/resume/` - Resume Files Storage
```
resume/
├── *.pdf                     # PDF resume files (31 files)
└── *.docx                    # Word document resumes
```
**Purpose**: Raw resume file storage for processing and extraction.

### ⚙️ `/config/` - Configuration Files
```
config/
└── production.env            # Production environment variables
```
**Purpose**: Environment-specific configuration and settings.

### 🚀 `/scripts/` - Deployment Scripts
```
scripts/
├── deploy.sh                 # Local deployment automation
├── deploy-cloud.sh           # Cloud deployment (AWS/GCP)
└── health-check.sh           # System health monitoring
```
**Purpose**: Deployment automation and system monitoring scripts.

### 📚 `/docs/` - Documentation
```
docs/
├── DEPLOYMENT.md             # Deployment instructions
├── REFLECTION.md             # Project reflection and insights
└── FILE_ORGANIZATION.md      # This file - project structure guide
```
**Purpose**: Comprehensive project documentation and guides.

## 🔗 Key Files in Root Directory

### 🐳 Container Orchestration
- `docker-compose.production.yml` - Production service orchestration
- `Dockerfile` (per service) - Individual service containers

### 📋 Dependencies
- `requirements.txt` - Global Python dependencies
- `requirements-semantic.txt` - Optional semantic processing dependencies

### 🔐 Environment & Security
- `.env` - Environment variables (not in version control)
- `.env.example` - Environment template

### 📖 Documentation
- `README.md` - Main project documentation
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `GCP_DEPLOYMENT_GUIDE.md` - Google Cloud deployment
- `IMPLEMENTATION_GUIDE.md` - Implementation details

## 🏷️ File Naming Conventions

### Service Files
- `app.py` - Main application entry point
- `main.py` - FastAPI main application
- `requirements.txt` - Python dependencies per service
- `Dockerfile` - Container configuration per service

### Tool Files
- `*_extractor.py` - Data extraction utilities
- `*_manager.py` - Management and sync utilities
- `*_watcher.py` - Monitoring and automation
- `test_*.py` - Test files

### Configuration Files
- `*.env` - Environment configuration
- `*.yml` - Docker Compose configuration
- `*.md` - Documentation files

## 🔄 Data Flow Architecture

```
Resume Files (📄) 
    ↓ (tools/comprehensive_resume_extractor.py)
Processed Data (📊) 
    ↓ (tools/database_sync_manager.py)
PostgreSQL Database (🗄️)
    ↓ (services/gateway/app/main.py)
API Gateway (🌐)
    ↓ (services/agent/app.py)
AI Matching (🤖)
    ↓ (services/portal/ & services/client_portal/)
User Interfaces (👥🏢)
```

## 🛡️ Security Architecture

### Authentication Flow
```
Client Portal (🏢) 
    ↓ (auth_service.py)
bcrypt + JWT (🔐)
    ↓ (PostgreSQL)
Secure Sessions (🛡️)
    ↓ (API Gateway)
Authorized Access (✅)
```

### File Security
- Environment variables in `.env` (excluded from version control)
- Encrypted password storage with bcrypt
- JWT token-based authentication
- PostgreSQL with secure connections

## 📈 Scalability Considerations

### Horizontal Scaling
- Each service can be scaled independently
- Database can be replicated for read operations
- Load balancer can be added in front of gateway

### Vertical Scaling
- Services designed for multi-core processing
- Database optimized for concurrent connections
- File processing can handle large batches

## 🔧 Maintenance Guidelines

### Regular Tasks
1. **Resume Processing**: Run `comprehensive_resume_extractor.py` for new files
2. **Database Sync**: Execute `database_sync_manager.py` for consistency
3. **Health Checks**: Monitor service status via health endpoints
4. **Log Monitoring**: Check Docker logs for errors

### File Management
- Keep resume files organized in `/resume/` directory
- Archive old processed data periodically
- Backup database regularly
- Update dependencies in requirements.txt files

## 🎯 Best Practices

### Development
- Follow microservices principles
- Maintain clear separation of concerns
- Use consistent naming conventions
- Document all major functions

### Deployment
- Use Docker Compose for orchestration
- Implement health checks for all services
- Monitor resource usage
- Maintain environment-specific configurations

### Security
- Never commit `.env` files
- Use strong JWT secrets
- Implement proper input validation
- Regular security updates

---

**📁 File Organization Guide** - Comprehensive structure documentation for BHIV HR Platform microservices architecture.