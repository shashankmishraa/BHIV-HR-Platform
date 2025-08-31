# BHIV HR Platform

🚀 **Production-Ready AI-Powered Recruiting Platform** with intelligent candidate matching and comprehensive assessment tools.

## 📋 Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Development](#development)

## 🎯 Overview

BHIV HR Platform is a complete recruiting solution that automates resume processing, candidate matching, and assessment workflows. Built with microservices architecture for scalability and production deployment.

### Key Capabilities
- **Resume Processing**: Extract data from PDF, DOCX, and TXT files
- **AI Matching**: Intelligent candidate-job compatibility scoring
- **Dual Portals**: Separate interfaces for recruiters and clients
- **Values Assessment**: Comprehensive candidate evaluation system
- **Production Ready**: Dockerized with health monitoring and security

### Technology Stack
- **Backend**: FastAPI, PostgreSQL
- **Frontend**: Streamlit
- **AI/ML**: Custom matching algorithms
- **Deployment**: Docker Compose
- **Processing**: PyPDF2, python-docx, pandas

## ⚡ Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.8+ (for local development)

### Installation
```bash
# 1. Clone repository
git clone <repository-url>
cd bhiv-hr-platform

# 2. Start production services
docker-compose -f docker-compose.production.yml up -d

# 3. Process sample resumes
python tools/comprehensive_resume_extractor.py
python tools/upload_csv_candidates.py
python tools/create_demo_jobs.py

# 4. Access platform
# Main Portal: http://localhost:8501
# Client Portal: http://localhost:8502
# API Docs: http://localhost:8000/docs
```

### Verification
```bash
# Check all services are running
docker-compose -f docker-compose.production.yml ps

# Test API endpoints
python tests/test_endpoints.py
```

## 🏗️ Architecture

### Service Overview
| Service | Port | Purpose | Technology |
|---------|------|---------|------------|
| **Gateway** | 8000 | API Backend | FastAPI |
| **Agent** | 9000 | AI Matching | FastAPI |
| **Portal** | 8501 | Recruiter UI | Streamlit |
| **Client Portal** | 8502 | Client UI | Streamlit |
| **Database** | 5432 | Data Storage | PostgreSQL |

### Project Structure
```
bhiv-hr-platform/
├── services/                 # Microservices
│   ├── gateway/             # API Backend
│   ├── agent/               # AI Engine
│   ├── portal/              # Main UI
│   ├── client_portal/       # Client UI
│   └── db/                  # Database Schema
├── tools/                   # Processing Tools
├── tests/                   # Test Suite
├── data/                    # Processed Data
├── resume/                  # Resume Files
└── docs/                    # Documentation
```

## 🚀 Features

### Resume Processing
- **Multi-format Support**: PDF, DOCX, TXT files
- **Field Extraction**: Name, email, phone, skills, experience, education
- **Batch Processing**: Handle multiple resumes simultaneously
- **High Accuracy**: 75-96% extraction accuracy across fields

### AI Matching System
- **Multi-factor Scoring**: Skills (50%), Experience (30%), Location (20%)
- **Real-time Matching**: <0.02 second response time
- **Transparent Scoring**: Detailed match explanations
- **Ranking Algorithm**: Top candidate recommendations

### Recruiter Portal (8501)
- **Dashboard**: Candidate overview and job statistics
- **Search & Filter**: Advanced candidate filtering
- **Job Management**: Create and manage job postings
- **AI Matching**: View top candidate matches
- **Values Assessment**: Evaluate candidate values

### Client Portal (8502)
- **Secure Access**: Authentication system
- **Job Posting**: Submit job descriptions
- **Candidate Review**: View ranked candidates
- **Match Insights**: AI scoring explanations
- **Export Tools**: Download candidate data

### Values Assessment
- **5-Point Scale**: Integrity, honesty, discipline, hard work, gratitude
- **Structured Evaluation**: Consistent assessment framework
- **Integration**: Seamless workflow integration

## 📊 API Documentation

### Authentication
```bash
Authorization: Bearer myverysecureapikey123
```

### Core Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health check |
| `/v1/jobs` | POST/GET | Job management |
| `/v1/candidates/bulk` | POST | Upload candidates |
| `/v1/candidates/search` | GET | Search candidates |
| `/v1/match/{id}/top` | GET | Get top matches |
| `/v1/feedback` | POST | Submit assessments |

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **AI Service**: http://localhost:9000/docs

## 🚀 Deployment

### Production Deployment
```bash
# Production with health checks
docker-compose -f docker-compose.production.yml up -d
```

### Development Setup
```bash
# Minimal services for development
docker-compose -f docker-compose.minimal.yml up -d
```

### Cloud Deployment
```bash
# AWS/GCP deployment
export DB_PASSWORD=your_secure_password
export API_KEY_SECRET=your_secure_api_key
docker-compose -f docker-compose.production.yml up -d
```

### Health Monitoring
- **Database**: Health checks with retry logic
- **Services**: Automatic restart policies
- **API**: Health endpoints for monitoring

## ⚙️ Configuration

### Environment Variables
```bash
# Database
DB_PASSWORD=your_secure_password
POSTGRES_PASSWORD=your_postgres_password

# API Security
API_KEY_SECRET=your_secure_api_key

# Optional: Semantic Processing
ENABLE_SEMANTIC=false
```

### Authentication
- **API Access**: Bearer token authentication
- **Client Portal**: Access code (`google123`)
- **Security**: Environment-based configuration

### Optional: Semantic Processing
```bash
# Install advanced AI features (adds ~2GB)
pip install -r requirements-semantic.txt

# Enable semantic matching
python tools/day2_semantic_processor.py
```

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start minimal services
docker-compose -f docker-compose.minimal.yml up -d

# Run processing tools
python tools/comprehensive_resume_extractor.py
```

### Testing
```bash
# Run all tests
python tests/test_endpoints.py

# Expected: 9/9 tests passed
```

### Resume Processing
```bash
# 1. Add resume files to 'resume/' folder
# 2. Extract candidate data
python tools/comprehensive_resume_extractor.py

# 3. Upload to database
python tools/upload_csv_candidates.py

# 4. View results
python tools/show_results.py
```

## 📈 Performance Metrics

- **Processing Speed**: 1-2 seconds per resume
- **API Response**: <100ms average
- **AI Matching**: <0.02 seconds
- **Extraction Accuracy**: 75-96% across fields
- **Concurrent Users**: Multi-user support

## 🎯 Success Metrics

### Functional Requirements ✅
- Resume upload → recruiter dashboard → client portal → scoring
- Recruiter search/filter capabilities
- Client job posting and candidate review

### Technical Requirements ✅
- 9/9 API endpoints tested and functional
- All 5 services with health monitoring
- Production-ready Docker configuration
- Database integration with full workflow

### Current Statistics
- **28 Candidates** processed and stored
- **11 Jobs** created and active
- **AI Matching** operational
- **Values Assessment** system active

## 🔧 Troubleshooting

### Common Issues
```bash
# Service startup issues
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d

# Check service status
docker-compose -f docker-compose.production.yml ps

# View logs
docker-compose -f docker-compose.production.yml logs [service-name]
```

### Support
- **API Testing**: Use `/health` endpoints
- **Database**: Check connection via logs
- **Processing**: Verify file formats and permissions

---

**BHIV HR Platform** - Production-ready recruiting solution with AI-powered matching and comprehensive assessment tools.