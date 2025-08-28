# 🏗️ BHIV HR Platform - Project Structure

## 📁 Directory Organization

```
bhiv-hr-platform/
├── 📚 docs/                          # Documentation
│   ├── Shashank Mishra Task 2.pdf   # Original task requirements
│   ├── API_DOCUMENTATION.md         # API endpoint documentation
│   └── DEPLOYMENT_GUIDE.md          # Deployment instructions
│
├── 🐳 services/                      # Microservices
│   ├── gateway/                      # API Gateway Service
│   │   ├── app/                      # Application code
│   │   │   ├── api/                  # API routes
│   │   │   │   ├── routes_candidates.py
│   │   │   │   ├── routes_feedback.py
│   │   │   │   ├── routes_interviews.py
│   │   │   │   ├── routes_jobs.py
│   │   │   │   ├── routes_match.py
│   │   │   │   ├── routes_offers.py
│   │   │   │   └── routes_reports.py
│   │   │   ├── core/                 # Core functionality
│   │   │   │   ├── config.py
│   │   │   │   └── security.py
│   │   │   ├── db/                   # Database models
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── crud.py
│   │   │   ├── services/             # Business logic
│   │   │   │   ├── ai_agent_client.py
│   │   │   │   ├── reporting.py
│   │   │   │   └── values_scoring.py
│   │   │   └── main.py               # FastAPI application
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── agent/                        # Talah AI Agent Service
│   │   ├── app.py                    # AI agent application
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── portal/                       # Streamlit Client Portal
│   │   ├── app.py                    # Portal application
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── db/                          # Database Service
│       └── init.sql                 # Database initialization
│
├── 📊 data/                         # Data files
│   ├── processed_candidates.csv     # Processed candidate data
│   ├── processed_files.json        # File processing log
│   ├── sample_candidates.csv       # Sample data
│   └── checking.txt                # Data validation logs
│
├── 📄 resume/                       # Resume storage
│   ├── AdarshYadavResume.pdf
│   ├── Anurag_CV.pdf
│   ├── [... other resume files ...]
│   └── Yash resume1.pdf
│
├── 🔧 scripts/                      # Utility scripts
│   ├── auto_upload_resumes.py      # Automated resume processing
│   ├── init_tables.py              # Database table creation
│   ├── resume_processor.py         # Resume parsing logic
│   ├── test_api.py                 # API testing script
│   ├── upload_now.py               # Manual upload script
│   ├── monitor_resumes.bat         # Resume monitoring (Windows)
│   ├── process_resumes.bat         # Resume processing (Windows)
│   ├── run-local.bat               # Local development (Windows)
│   ├── start.bat                   # Start services (Windows)
│   └── stop.bat                    # Stop services (Windows)
│
├── ⚙️ config/                       # Configuration files
│   ├── .env.example                # Environment variables template
│   └── resume_requirements.txt     # Resume processing dependencies
│
├── 🧪 tests/                        # Test files
│   └── [test files will be added here]
│
├── 🐳 docker-compose.yml            # Docker orchestration
├── 📝 README.md                     # Main documentation
├── 🏆 Reflection.md                 # Values reflection
├── 🏗️ PROJECT_STRUCTURE.md          # This file
└── 🔐 .env                          # Environment variables (local)
```

## 🎯 Service Architecture

### **API Gateway** (`services/gateway/`)
- **Purpose**: Central API hub for all HR operations
- **Technology**: FastAPI with SQLAlchemy
- **Port**: 8000
- **Features**:
  - Job management endpoints
  - Candidate processing
  - Values-based feedback system
  - Interview scheduling
  - Offer management
  - CSV report generation
  - Real-time analytics

### **Talah AI Agent** (`services/agent/`)
- **Purpose**: AI-powered candidate analysis and matching
- **Technology**: FastAPI with ML algorithms
- **Port**: 9000
- **Features**:
  - Resume analysis
  - Candidate scoring (0-100)
  - Values alignment prediction (1-5)
  - Top-5 candidate shortlisting
  - Bias detection and fair evaluation

### **Client Portal** (`services/portal/`)
- **Purpose**: User-friendly web interface for recruiters
- **Technology**: Streamlit
- **Port**: 8501
- **Features**:
  - Job creation interface
  - Bulk candidate upload
  - AI shortlist visualization
  - Values assessment forms
  - Real-time dashboard
  - Analytics and reporting

### **Database** (`services/db/`)
- **Purpose**: Data persistence layer
- **Technology**: PostgreSQL
- **Port**: 5432
- **Tables**:
  - `clients` - Client organizations
  - `jobs` - Job postings
  - `candidates` - Candidate profiles
  - `feedback` - Values-based assessments
  - `interviews` - Interview scheduling
  - `offers` - Job offers

## 📊 Data Flow

```
Resume Upload → Processing → Database → AI Analysis → Portal Display
     ↓              ↓           ↓           ↓            ↓
   PDF/DOC    →  CSV Data  →  PostgreSQL → Scoring  →  Dashboard
```

## 🔧 Development Workflow

### **Local Development**
1. **Setup**: `docker compose up --build`
2. **Development**: Edit files in respective service directories
3. **Testing**: Use scripts in `scripts/` directory
4. **Data**: Sample data available in `data/` directory

### **File Organization Benefits**
- **Separation of Concerns**: Each service has its own directory
- **Easy Maintenance**: Related files grouped together
- **Scalability**: Easy to add new services or components
- **Documentation**: Clear structure for new developers
- **Deployment**: Docker services map directly to directories

## 🚀 Quick Start Commands

```bash
# Start all services
docker compose up --build

# Process resumes
python scripts/resume_processor.py

# Test API endpoints
python scripts/test_api.py

# Initialize database tables
python scripts/init_tables.py
```

## 📈 MDVP Compliance

This structure supports **Minimum Daily Value Push** by:
- **Day 1**: Core services in `services/` directory
- **Day 2**: Values system in `gateway/app/api/routes_feedback.py`
- **Day 3**: Complete workflow with all endpoints
- **Day 4**: Documentation and deployment ready

## 🏆 Values Integration

Each service incorporates the core values:
- **Integrity**: Honest API responses and data handling
- **Honesty**: Transparent error messages and documentation
- **Discipline**: Consistent code structure and patterns
- **Hard Work**: Comprehensive feature implementation
- **Gratitude**: User-focused design and helpful documentation

---

*This structure ensures maintainability, scalability, and professional development practices while supporting the complete BHIV HR Platform functionality.*