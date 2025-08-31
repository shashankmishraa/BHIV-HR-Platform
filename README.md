# BHIV HR Platform

🚀 **AI-Powered Recruiting Platform** with intelligent candidate matching, resume processing, and values-based assessment.

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Beginner's Guide](#beginners-guide)
- [Project Structure](#project-structure)
- [Resume Processing](#resume-processing)
- [Portal Functions](#portal-functions)
- [API Endpoints](#api-endpoints)
- [Development Commands](#development-commands)
- [Troubleshooting](#troubleshooting)

## ⚡ Quick Start

```bash
# 1. Start essential services
docker-compose -f docker-compose.minimal.yml up -d

# 2. Process resumes
python tools/comprehensive_resume_extractor.py

# 3. Upload candidates
python tools/upload_csv_candidates.py

# 4. Access the platform
# Portal: http://localhost:8501
# API Docs: http://localhost:8000/docs
# AI Service: http://localhost:9000/docs
```

## 📚 Beginner's Guide

### Prerequisites
- **Docker & Docker Compose** (for containerized deployment)
- **Python 3.8+** (for local development)
- **Git** (for version control)

### Step-by-Step Setup

#### 1. Clone & Setup
```bash
# Clone the repository
git clone <repository-url>
cd bhiv-hr-platform

# Copy environment template
cp .env.example .env
```

#### 2. Start the Platform
```bash
# Option A: Minimal setup (recommended for beginners)
docker-compose -f docker-compose.minimal.yml up -d

# Option B: Full setup (all services)
docker-compose up -d
```

#### 3. Verify Installation
```bash
# Check if services are running
docker-compose ps

# Test all endpoints
python tests/test_endpoints.py
```

#### 4. Process Your First Resumes
```bash
# Place PDF/DOCX files in the 'resume' folder
# Then run the comprehensive extractor
python tools/comprehensive_resume_extractor.py

# Upload processed candidates to database
python tools/upload_csv_candidates.py
```

#### 5. Create Demo Jobs
```bash
# Create sample job postings
python tools/create_demo_jobs.py
```

## 📁 Project Structure

```
bhiv-hr-platform/
├── 🚀 services/              # Core Microservices
│   ├── gateway/             # FastAPI Backend (Port 8000)
│   ├── agent/               # AI Matching Service (Port 9000)
│   ├── portal/              # Streamlit Frontend (Port 8501)
│   └── db/                  # PostgreSQL Database Schema
├── 📄 resume/               # Resume Files (PDF, DOCX, TXT)
├── 🔧 scripts/              # Core Processing Scripts
│   ├── enhanced_resume_processor.py  # Legacy processor
│   └── init_tables.py       # Database initialization
├── 📊 data/                 # Processed Data & Outputs
│   └── candidates.csv       # Extracted candidate data
├── 🧪 tests/                # Testing Suite
│   ├── test_endpoints.py    # API testing (9/9 PASSED)
│   └── test_*.py           # Additional tests
├── 🛠️ tools/                # Utility & Processing Tools
│   ├── comprehensive_resume_extractor.py  # Main extractor
│   ├── precise_resume_extractor.py       # Precise extraction
│   ├── pdf_to_csv.py                     # Basic PDF converter
│   ├── create_demo_jobs.py               # Demo data creation
│   ├── upload_csv_candidates.py          # Database upload
│   └── show_results.py                   # Results summary
├── 🐳 docker-compose.yml    # Full deployment configuration
├── 🐳 docker-compose.minimal.yml # Essential services only
├── ⚙️ .env                  # Environment variables
└── 📋 .env.example         # Environment template
```

## 📄 Resume Processing

### Supported File Types
- **PDF** (.pdf) - Primary format
- **Microsoft Word** (.docx, .doc)
- **Text Files** (.txt)

### Processing Commands

#### Comprehensive Extraction (Recommended)
```bash
# Process all files in resume folder with deep analysis
python tools/comprehensive_resume_extractor.py

# Features:
# ✅ Scans all file types automatically
# ✅ Deep content analysis
# ✅ Enhanced field extraction
# ✅ Detailed processing statistics
```

#### Precise Extraction
```bash
# Individual file processing with detailed logging
python tools/precise_resume_extractor.py

# Features:
# ✅ Individual file analysis
# ✅ Step-by-step extraction logging
# ✅ Field-by-field validation
```

#### Basic PDF Conversion
```bash
# Simple PDF to CSV conversion
python tools/pdf_to_csv.py

# Features:
# ✅ Quick processing
# ✅ Basic field extraction
# ✅ Lightweight operation
```

### Extracted Fields
- **Name** - Candidate full name
- **Email** - Contact email address
- **Phone** - Phone number (multiple formats)
- **Location** - City/State/Country
- **Designation** - Job title/role
- **Skills** - Technical skills (comma-separated)
- **Experience** - Years of experience or "Fresher"
- **Education** - Highest degree (PhD, Masters, Bachelors, etc.)
- **Resume Name** - Original filename

### Processing Statistics
- **Names**: 100% extraction rate
- **Emails**: 75-85% when present
- **Phones**: 80-90% various formats
- **Skills**: 95%+ comprehensive database
- **Education**: 95%+ broad keyword coverage

## 🌐 Portal Functions

### Web Portal (Port 8501) - http://localhost:8501
**Main User Interface - Streamlit Application**

#### Dashboard Features
- **Candidate Overview**: Total candidates, recent additions
- **Job Management**: Active jobs, application statistics
- **Matching Results**: AI-powered candidate recommendations
- **Values Assessment**: Integrity, honesty, discipline scoring

#### Job Creation & Management
```
✅ Create new job postings
✅ Set job requirements and skills
✅ Define experience levels
✅ Location preferences
✅ Salary ranges
```

#### Candidate Search & Filtering
```
✅ Search by skills (Python, Java, React, etc.)
✅ Filter by experience level
✅ Location-based filtering
✅ Education level filtering
✅ Availability status
```

#### AI Matching Interface
```
✅ Top candidate recommendations
✅ Compatibility scoring
✅ Skills match percentage
✅ Experience alignment
✅ Location compatibility
```

#### Values Assessment Forms
```
✅ Integrity assessment (1-5 scale)
✅ Honesty evaluation
✅ Discipline rating
✅ Hard work assessment
✅ Gratitude measurement
```

### API Gateway (Port 8000) - http://localhost:8000/docs
**FastAPI Backend - Swagger Documentation**

#### Interactive API Documentation
```
✅ Complete endpoint documentation
✅ Request/response schemas
✅ Authentication examples
✅ Try-it-out functionality
✅ Model definitions
```

#### Health Monitoring
```
✅ Service health checks
✅ Database connectivity
✅ Performance metrics
✅ Error logging
```

### AI Service (Port 9000) - http://localhost:9000/docs
**AI Matching Engine - FastAPI Service**

#### Matching Algorithm Interface
```
✅ Candidate-job compatibility scoring
✅ Skills matching algorithms
✅ Experience level assessment
✅ Location preference matching
✅ Multi-factor scoring system
```

#### Algorithm Details
- **Skills Matching**: 50% weight
- **Experience Matching**: 30% weight
- **Location Matching**: 20% weight
- **Response Time**: <0.02 seconds

## 📊 API Endpoints (All Tested ✅)

### Health & Status
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/health` | GET | ✅ HEALTHY | Service health check |
| `/` | GET | ✅ HEALTHY | Root endpoint |

### Job Management
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/v1/jobs` | POST | ✅ PASSED | Create new job |
| `/v1/jobs` | GET | ✅ PASSED | List all jobs |

### Candidate Management
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/v1/candidates/bulk` | POST | ✅ PASSED | Upload candidates |
| `/v1/candidates/job/{id}` | GET | ✅ PASSED | Get job candidates |
| `/v1/candidates/search` | GET | ✅ PASSED | Search & filter |

### AI Matching
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/v1/match/{id}/top` | GET | ✅ PASSED | Top 5 matches |

### Assessment & Workflow
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/v1/feedback` | POST | ✅ PASSED | Values assessment |
| `/v1/interviews` | POST | ✅ PASSED | Schedule interviews |
| `/v1/offers` | POST | ✅ PASSED | Job offers |

### Statistics
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/candidates/stats` | GET | ✅ PASSED | Platform statistics |

## 🔑 Authentication

**API Key for Testing:**
```
Authorization: Bearer myverysecureapikey123
```

## 💻 Development Commands

### Platform Management
```bash
# Start all services
docker-compose up -d

# Start minimal services only
docker-compose -f docker-compose.minimal.yml up -d

# Stop all services
docker-compose down

# View service logs
docker-compose logs -f [service-name]

# Restart specific service
docker-compose restart [service-name]
```

### Resume Processing Workflow
```bash
# 1. Add resume files to 'resume' folder
# 2. Run comprehensive extraction
python tools/comprehensive_resume_extractor.py

# 3. Review extracted data
python tools/show_results.py

# 4. Upload to database
python tools/upload_csv_candidates.py

# 5. Create demo jobs (optional)
python tools/create_demo_jobs.py
```

### Testing & Validation
```bash
# Test all API endpoints (9/9 tests)
python tests/test_endpoints.py

# Validate data extraction
python tools/show_results.py

# Check service health
curl http://localhost:8000/health
curl http://localhost:9000/health
```

### Database Operations
```bash
# Initialize database tables
python scripts/init_tables.py

# Upload candidate data
python tools/upload_csv_candidates.py

# Create sample jobs
python tools/create_demo_jobs.py
```

## 🔧 Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Check if ports are available
netstat -an | findstr :8000
netstat -an | findstr :8501
netstat -an | findstr :9000

# Stop conflicting services
docker-compose down
docker system prune -f
```

#### Resume Processing Errors
```bash
# Check file permissions
dir resume\

# Verify file formats
python tools/precise_resume_extractor.py

# Test with single file
python tools/show_results.py
```

#### Database Connection Issues
```bash
# Check database status
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Portal Access Issues
```bash
# Check if Streamlit is running
curl http://localhost:8501

# Restart portal service
docker-compose restart portal

# Check portal logs
docker-compose logs portal
```

### Service Status Verification
```bash
# Test all endpoints
python tests/test_endpoints.py

# Expected output: 9/9 tests passed
# - Health: 4/4 services healthy
# - Authentication: PASSED
# - Jobs: PASSED
# - Candidates: PASSED
# - AI Matching: PASSED
# - Feedback: PASSED
# - Interviews: PASSED
# - Offers: PASSED
# - Statistics: PASSED
```

## 📊 System Status
- **28 Candidates** processed with comprehensive extraction
- **8 Active Jobs** across departments
- **Multiple File Types** supported (PDF, DOCX, TXT)
- **9/9 API Endpoints** fully functional ✅
- **Web Portal** fully operational ✅
- **AI Matching** algorithm active ✅
- **Database** connected and responsive ✅

## 🛠️ Tech Stack
- **Backend**: FastAPI, PostgreSQL
- **AI/ML**: Custom matching algorithm, Python ML libraries
- **Frontend**: Streamlit
- **Processing**: PyPDF2, python-docx, pandas
- **Deployment**: Docker Compose
- **Authentication**: Bearer token system
- **Database**: PostgreSQL with custom schema

## 📈 Performance Metrics
- **Processing Speed**: ~1-2 seconds per resume
- **Extraction Accuracy**: 75-96% across different fields
- **Supported Formats**: PDF, DOCX, DOC, TXT
- **API Response Time**: <100ms for most endpoints
- **AI Matching Speed**: <0.02 seconds
- **Concurrent Users**: Supports multiple simultaneous users

## 🎯 Core Features

### Job Creation
```bash
curl -X POST http://localhost:8000/v1/jobs \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{"title": "AI Engineer", "client_id": 1}'
```

### Candidate Search
```bash
curl -H "Authorization: Bearer myverysecureapikey123" \
  "http://localhost:8000/v1/candidates/search?skills=Python&job_id=1"
```

### AI Matching
```bash
curl -H "Authorization: Bearer myverysecureapikey123" \
  "http://localhost:8000/v1/match/1/top"
```

## 🌐 Access Points
- **🖥️ Web Portal**: http://localhost:8501 (Main Interface) ✅
- **📚 API Documentation**: http://localhost:8000/docs (Swagger UI) ✅
- **🤖 AI Service**: http://localhost:9000/docs (Matching Engine) ✅
- **💾 Database**: localhost:5432 (PostgreSQL) ✅

## 🚀 Quick Commands Reference

| Task | Command |
|------|---------|
| Start platform | `docker-compose -f docker-compose.minimal.yml up -d` |
| Process resumes | `python tools/comprehensive_resume_extractor.py` |
| Upload candidates | `python tools/upload_csv_candidates.py` |
| Test all APIs | `python tests/test_endpoints.py` |
| Create demo jobs | `python tools/create_demo_jobs.py` |
| View results | `python tools/show_results.py` |
| Stop platform | `docker-compose down` |

## 🎉 Success Indicators
- ✅ All 9 API endpoints tested and working
- ✅ Web portal accessible at port 8501
- ✅ API documentation available at port 8000
- ✅ AI service running at port 9000
- ✅ Database connected and operational
- ✅ Resume processing functional
- ✅ Candidate matching algorithm active
- ✅ Values assessment system operational