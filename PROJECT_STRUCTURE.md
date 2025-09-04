# PROJECT_STRUCTURE.md

## Directory Structure

```
BHIV-HR-Platform/
├── services/                    # Microservices Architecture
│   ├── gateway/                # API Gateway Service
│   │   ├── app/
│   │   │   ├── main.py        # FastAPI application with 43 endpoints
│   │   │   └── __init__.py
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Python dependencies
│   ├── agent/                 # AI Matching Engine
│   │   ├── app.py            # SBERT-based semantic matching
│   │   ├── Dockerfile        # Container configuration
│   │   └── requirements.txt  # AI/ML dependencies
│   ├── portal/               # HR Dashboard (Streamlit)
│   │   ├── app.py           # Main dashboard interface
│   │   ├── batch_upload.py  # Resume batch processing
│   │   ├── Dockerfile       # Container configuration
│   │   └── requirements.txt # Streamlit dependencies
│   ├── client_portal/       # Client Interface (Streamlit)
│   │   ├── app.py          # Client dashboard
│   │   ├── auth_service.py # Authentication logic
│   │   ├── Dockerfile      # Container configuration
│   │   └── requirements.txt # Client portal dependencies
│   └── db/                 # Database Schema & Migrations
│       ├── init.sql       # Database initialization
│       └── schema.sql     # Table definitions
├── tools/                  # Data Processing & Utilities
│   ├── comprehensive_resume_extractor.py  # Resume parsing engine
│   ├── dynamic_job_creator.py            # Job posting generator
│   ├── database_sync_manager.py          # Database synchronization
│   ├── auto_sync_watcher.py             # File system monitoring
│   ├── create_demo_jobs.py              # Demo data creation
│   └── show_results.py                  # Results visualization
├── tests/                  # Test Suite
│   ├── test_endpoints.py              # API endpoint testing
│   ├── test_security.py               # Security validation
│   ├── test_client_portal.py          # Portal integration tests
│   ├── test_comprehensive_diagnostic.py # System diagnostics
│   ├── test_aggressive_diagnostic.py   # Performance testing
│   ├── test_week2_enterprise.py       # Enterprise features
│   └── test_structured_api.py         # API structure validation
├── scripts/                # Deployment & Automation
│   ├── unified-deploy.sh   # Deployment automation
│   └── health-check.sh     # Health monitoring
├── docs/                   # Documentation
│   ├── BIAS_ANALYSIS.md    # AI bias analysis & mitigation
│   ├── SECURITY_AUDIT.md   # Security assessment
│   ├── USER_GUIDE.md       # Complete user manual
│   └── SERVICES_GUIDE.md   # Service architecture guide
├── data/                   # Sample Data & Assets
│   ├── candidates.csv      # Sample candidate data
│   ├── jobs.csv           # Sample job postings
│   └── resumes/           # Sample resume files
├── config/                 # Configuration Files
│   ├── production.env      # Production environment variables
│   └── development.env     # Development configuration
├── docker-compose.production.yml  # Docker orchestration
├── render.yaml            # Render deployment configuration
├── README.md             # Main project documentation
├── REFLECTION.md         # Daily development reflections
├── PROJECT_STRUCTURE.md  # This file
└── DEPLOYMENT_STATUS.md  # Current deployment status
```

## Component Overview

### Core Services

#### 1. API Gateway (`services/gateway/`)
- **Technology**: FastAPI 3.1.0
- **Purpose**: Central REST API backend with 43 endpoints
- **Key Features**:
  - Authentication & authorization (JWT, API keys)
  - Rate limiting (60 requests/minute)
  - Input validation & security headers
  - 2FA support (TOTP compatible)
  - Comprehensive error handling
- **Database**: PostgreSQL integration with SQLAlchemy
- **Port**: 8000

#### 2. AI Matching Engine (`services/agent/`)
- **Technology**: FastAPI 2.1.0 + SBERT
- **Purpose**: Semantic candidate-job matching
- **Key Features**:
  - SBERT-based similarity scoring
  - Bias mitigation algorithms
  - Real-time matching (<0.02s response)
  - Dynamic skill categorization
  - Performance optimization
- **Port**: 9000

#### 3. HR Portal (`services/portal/`)
- **Technology**: Streamlit
- **Purpose**: HR dashboard and management interface
- **Key Features**:
  - Candidate search & filtering
  - Job management interface
  - AI matching visualization
  - Batch resume upload
  - Analytics dashboard
- **Port**: 8501

#### 4. Client Portal (`services/client_portal/`)
- **Technology**: Streamlit
- **Purpose**: Client interface for job posting and candidate review
- **Key Features**:
  - Enterprise authentication
  - Job posting interface
  - Candidate review system
  - Values assessment (5-point scale)
  - Real-time status updates
- **Port**: 8502

### Supporting Infrastructure

#### Database Layer (`services/db/`)
- **Technology**: PostgreSQL 17
- **Schema**: Candidates, Jobs, Matches, Users tables
- **Features**: ACID compliance, indexing, connection pooling

#### Data Processing (`tools/`)
- **Resume Extraction**: Multi-format support (PDF, DOCX, TXT)
- **Job Creation**: Dynamic job posting generation
- **Database Sync**: Real-time data synchronization
- **File Monitoring**: Automated file system watching

#### Testing Suite (`tests/`)
- **API Testing**: Endpoint validation and integration tests
- **Security Testing**: Vulnerability assessment and penetration testing
- **Performance Testing**: Load testing and scalability assessment
- **Enterprise Testing**: 2FA, backup codes, and enterprise features

## Architecture Patterns

### Microservices Design
- **Service Isolation**: Each service runs independently
- **API-First**: RESTful communication between services
- **Database Per Service**: Shared PostgreSQL with service-specific schemas
- **Container-Ready**: Docker containerization for all services

### Security Architecture
- **Defense in Depth**: Multiple security layers
- **Zero Trust**: Authentication required for all endpoints
- **Input Validation**: XSS/SQL injection protection
- **Rate Limiting**: DoS protection and resource management

### AI/ML Pipeline
- **Data Ingestion**: Resume parsing and job posting extraction
- **Feature Engineering**: Skill extraction and categorization
- **Model Inference**: SBERT semantic similarity scoring
- **Bias Mitigation**: Fairness algorithms and threshold adjustment

## Deployment Configuration

### Local Development
```bash
# Start all services
docker-compose -f docker-compose.production.yml up -d

# Access services
HR Portal: http://localhost:8501
Client Portal: http://localhost:8502
API Gateway: http://localhost:8000/docs
AI Agent: http://localhost:9000/docs
```

### Production (Render)
- **Platform**: Render Cloud (Oregon, US West)
- **Configuration**: render.yaml blueprint
- **Services**: 5 web services + PostgreSQL database
- **Cost**: $0/month (Free tier)
- **SSL**: Automatic HTTPS certificates

## Data Flow

### Resume Processing Flow
1. **Upload** → Portal receives resume files
2. **Extract** → comprehensive_resume_extractor.py processes content
3. **Store** → Candidate data saved to PostgreSQL
4. **Index** → SBERT embeddings generated for semantic search

### Job Matching Flow
1. **Job Posted** → Client creates job posting via portal
2. **Analysis** → AI agent extracts job requirements
3. **Matching** → SBERT computes candidate similarities
4. **Ranking** → Bias-adjusted scoring and ranking
5. **Results** → Top matches returned to HR portal

### Authentication Flow
1. **Login** → Client credentials validated
2. **Token** → JWT token generated and returned
3. **Authorization** → Bearer token validates API requests
4. **2FA** → Optional TOTP verification for enhanced security

## Performance Characteristics

### Response Times
- **API Endpoints**: <100ms average
- **AI Matching**: <0.02 seconds per candidate
- **Resume Processing**: 1-2 seconds per file
- **Portal Loading**: 2-3 seconds (cold start)

### Scalability
- **Concurrent Users**: Multi-user support
- **Rate Limits**: 60 requests/minute per IP
- **Database**: Connection pooling and indexing
- **Caching**: In-memory caching for frequent queries

## Development Guidelines

### Code Organization
- **Separation of Concerns**: Clear service boundaries
- **DRY Principle**: Shared utilities and common functions
- **Error Handling**: Comprehensive exception management
- **Documentation**: Inline comments and API documentation

### Testing Strategy
- **Unit Tests**: Individual function validation
- **Integration Tests**: Service-to-service communication
- **Security Tests**: Vulnerability assessment
- **Performance Tests**: Load and stress testing

### Deployment Process
1. **Development** → Local testing with Docker Compose
2. **Testing** → Automated test suite execution
3. **Staging** → Render preview deployments
4. **Production** → Automatic deployment via GitHub integration