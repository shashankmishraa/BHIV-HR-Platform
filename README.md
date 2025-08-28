# 🎯 BHIV HR Platform - Values-Driven Recruiting with MDVP

A containerized HR platform with API Gateway, Client Portal, AI Agent, and PostgreSQL database, built with **Minimum Daily Value Push (MDVP)** methodology.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (for cloning)

### 1. Clone and Start
```bash
git clone <repository-url>
cd bhiv-hr-platform
docker compose up --build
```

### 2. Access Services
- **🎯 Client Portal**: http://localhost:8501 (Main UI)
- **📚 API Gateway**: http://localhost:8000 (Swagger UI: /docs)
- **🤖 Talah AI Agent**: http://localhost:9000 (Swagger UI: /docs)
- **🗄️ Database**: localhost:5432 (user: bhiv_user, pass: bhiv_pass)

## 🏆 Core Values Framework

### Values Assessment Scale (1-5):
- **Integrity**: Moral uprightness and ethical behavior
- **Honesty**: Truthfulness and transparency in communication
- **Discipline**: Self-control, consistency, and commitment to excellence
- **Hard Work**: Dedication, perseverance, and going above expectations
- **Gratitude**: Appreciation, humility, and recognition of others

## 📋 Complete End-to-End Flow

### 1. Create Job Posting
```bash
curl -X POST http://localhost:8000/v1/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "title": "Senior Software Engineer",
    "description": "Looking for experienced developers",
    "client_id": 1
  }'
```

### 2. Upload Enhanced Candidate CVs (Bulk)
```bash
curl -X POST http://localhost:8000/v1/candidates/bulk \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidates": [
      {
        "name": "Adarshyadav",
        "email": "adarshyadav1019@gmail.com",
        "phone": "+91 7738620900",
        "location": "Mumbai",
        "cv_url": "https://example.com/resumes/AdarshYadavResume.pdf",
        "experience_years": 0,
        "education_level": "Masters",
        "technical_skills": "Java, JavaScript, React, SQL, AWS",
        "seniority_level": "Entry-level",
        "status": "applied",
        "job_id": 1
      }
    ]
  }'
```

### 3. Get AI-Powered Top-5 Shortlist
```bash
curl -X GET http://localhost:8000/v1/match/1/top \
  -H "X-API-KEY: myverysecureapikey123"
```

### 4. Submit Values-Based Feedback
```bash
curl -X POST http://localhost:8000/v1/feedback \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "reviewer_name": "HR Manager",
    "feedback_text": "Excellent technical skills and cultural fit",
    "values_scores": {
      "integrity": 5,
      "honesty": 4,
      "discipline": 5,
      "hard_work": 5,
      "gratitude": 4
    },
    "overall_recommendation": "Strongly Recommend"
  }'
```

### 5. Schedule Interview
```bash
curl -X POST http://localhost:8000/v1/interviews \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "interview_date": "2025-09-01T10:00:00Z",
    "interviewer": "Tech Lead"
  }'
```

### 6. Make Job Offer
```bash
curl -X POST http://localhost:8000/v1/offers \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "salary": 120000,
    "status": "sent"
  }'
```

### 7. Export Job Report
```bash
curl -X GET http://localhost:8000/v1/reports/job/1/export.csv \
  -H "X-API-KEY: myverysecureapikey123" \
  -o job_report.csv
```

## 🔧 API Endpoints with Examples

### Jobs Management

#### Create Job Posting
```bash
# POST /v1/jobs
curl -X POST http://localhost:8000/v1/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "title": "Data Scientist",
    "description": "Looking for experienced data scientists with ML expertise",
    "client_id": 1
  }'

# Response:
{
  "message": "Job created successfully",
  "status": "success",
  "job_id": 3
}
```

#### List All Jobs
```bash
# GET /v1/jobs
curl -H "X-API-KEY: myverysecureapikey123" \
  http://localhost:8000/v1/jobs

# Response:
{
  "jobs": [
    {
      "id": 1,
      "title": "Software Engineer",
      "statistics": {
        "candidates": 28,
        "feedback_received": 5,
        "interviews_scheduled": 2,
        "offers_made": 1
      }
    }
  ]
}
```

### Candidates Management

#### Upload Candidates (Bulk)
```bash
# POST /v1/candidates/bulk
curl -X POST http://localhost:8000/v1/candidates/bulk \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidates": [
      {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "cv_url": "https://example.com/alice-cv.pdf",
        "phone": "+1-555-0123",
        "experience_years": 3,
        "status": "applied",
        "job_id": 1
      }
    ]
  }'

# Response:
{
  "message": "Candidates uploaded successfully",
  "status": "success",
  "candidates_added": 1
}
```

### AI Matching (Talah Agent)

#### Get Top-5 Candidates with AI Scoring
```bash
# GET /v1/match/{job_id}/top
curl -H "X-API-KEY: myverysecureapikey123" \
  http://localhost:8000/v1/match/1/top

# Response:
{
  "job_id": 1,
  "top_candidates": [
    {
      "id": 31,
      "name": "Adarshyadav",
      "score": 95,
      "values_alignment": 4.8,
      "skills_match": 92,
      "recommendation_strength": "High"
    }
  ],
  "ai_analysis": "Analyzed 28 candidates using advanced ML algorithms"
}
```

### Values Assessment

#### Submit Values-Based Feedback
```bash
# POST /v1/feedback
curl -X POST http://localhost:8000/v1/feedback \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidate_id": 31,
    "reviewer_name": "Sarah Wilson",
    "feedback_text": "Outstanding candidate with strong technical skills",
    "values_scores": {
      "integrity": 5,
      "honesty": 5,
      "discipline": 4,
      "hard_work": 5,
      "gratitude": 4
    },
    "overall_recommendation": "Strongly Recommend"
  }'

# Response:
{
  "message": "Values feedback submitted successfully",
  "status": "success",
  "feedback_id": 3,
  "values_summary": {
    "average_score": 4.6
  }
}
```

## 🐳 Docker Services

```yaml
services:
  db:          # PostgreSQL database (port 5432)
  gateway:     # FastAPI Gateway (port 8000) - services/gateway/
  agent:       # Talah AI Agent (port 9000) - services/agent/
  portal:      # Streamlit Portal (port 8501) - services/portal/
```

## 📁 Project Structure

```
bhiv-hr-platform/
├── services/           # Microservices
│   ├── gateway/       # API Gateway (FastAPI)
│   ├── agent/         # Talah AI Agent
│   ├── portal/        # Client Portal (Streamlit)
│   └── db/            # Database initialization
├── data/              # Data files and logs
├── resume/            # Resume storage
├── scripts/           # Utility scripts
├── config/            # Configuration files
├── docs/              # Documentation
└── tests/             # Test files
```

## 🎯 Client Portal Examples

### Using the Web Interface (http://localhost:8501)

#### 1. Create Job Position
```
🏢 Create New Job Position
┌─────────────────────────────────────────────────┐
│ Job Title: [Senior Python Developer           ] │
│ Department: [Engineering ▼]                    │
│ Location: [Remote                             ] │
│ Experience: [Senior ▼]                         │
│ Client ID: [1]                                 │
│                                                │
│ Description:                                   │
│ ┌─────────────────────────────────────────────┐ │
│ │ We are looking for a senior Python         │ │
│ │ developer with 5+ years experience...      │ │
│ └─────────────────────────────────────────────┘ │
│                                                │
│           [🚀 Create Job]                      │
└─────────────────────────────────────────────────┘

Result: ✅ Job created successfully! Job ID: 3
```

#### 2. Upload Candidates (CSV Format)
```
📤 Bulk Candidate Upload
┌─────────────────────────────────────────────────┐
│ Job ID: [3]                                     │
│                                                │
│ Expected CSV Format:                           │
│ name,email,cv_url,phone,experience_years,status │
│                                                │
│ Choose File: [candidates.csv] [Browse...]       │
│                                                │
│           [📤 Upload Candidates]                │
└─────────────────────────────────────────────────┘

Result: ✅ Successfully uploaded 25 candidates for Job ID: 3
```

#### 3. View AI Shortlist
```
🎯 AI-Powered Candidate Shortlist
┌─────────────────────────────────────────────────┐
│ Job ID: [3] [🤖 Generate Shortlist]             │
└─────────────────────────────────────────────────┘

🤖 AI Analysis Complete! Top-5 candidates:

▼ #1 - Alice Johnson (Overall Score: 95)
  ├── Technical Score: 92/100
  ├── Values Alignment: 4.8/5 ⭐
  ├── Skills: Python, Django, PostgreSQL
  ├── Cultural Fit: Excellent
  └── [📞 Contact Alice]

▼ #2 - Bob Smith (Overall Score: 89)
  ├── Technical Score: 87/100
  ├── Values Alignment: 4.5/5 ⭐
  ├── Skills: Python, FastAPI, Docker
  └── [📞 Contact Bob]
```

#### 4. Submit Values Feedback
```
📊 Values-Based Candidate Assessment
┌─────────────────────────────────────────────────┐
│ Candidate: [Alice Johnson]                      │
│ Job ID: [3]                                     │
│ Reviewer: [Sarah Wilson - HR Manager]           │
│                                                │
│ 🏆 Values Assessment (1-5 scale):              │
│                                                │
│ Integrity:    ●●●●●○ (5/5)                     │
│ Honesty:      ●●●●●○ (5/5)                     │
│ Discipline:   ●●●●○○ (4/5)                     │
│ Hard Work:    ●●●●●○ (5/5)                     │
│ Gratitude:    ●●●●○○ (4/5)                     │
│                                                │
│ Overall: [Strongly Recommend ▼]                │
│                                                │
│           [📤 Submit Assessment]                │
└─────────────────────────────────────────────────┘

Result: ✅ Values assessment submitted! Average: 4.6/5
```

## 🔐 Security & Authentication Examples

### API Key Authentication
All API endpoints require `X-API-KEY` header:

#### ✅ Correct Authentication
```bash
# Successful request with API key
curl -H "X-API-KEY: myverysecureapikey123" \
  http://localhost:8000/v1/jobs

# Response: 200 OK
{
  "jobs": [...],
  "status": "success"
}
```

#### ❌ Missing Authentication
```bash
# Request without API key
curl http://localhost:8000/v1/jobs

# Response: 401 Unauthorized
{
  "error": "Missing or invalid API key",
  "message": "Please provide X-API-KEY header"
}
```

### Environment Variables Setup
```env
# Production .env Example
DATABASE_URL=postgresql://bhiv_user:STRONG_PASSWORD@db:5432/bhiv_hr
API_KEY=your-secure-api-key-here-min-32-chars
POSTGRES_USER=bhiv_user
POSTGRES_PASSWORD=STRONG_PASSWORD_HERE
POSTGRES_DB=bhiv_hr
```

## 📊 Dashboard Features with Examples

### Real-time Analytics

#### Candidate Pipeline Visualization
```
Applied (56) → Screened (28) → Interviewed (5) → Offered (2) → Hired (1)
   100%           50%            9%           4%        2%
```

#### Values Distribution Chart
```
Integrity:    ████████████████████ 4.2/5
Honesty:      ██████████████████████ 4.5/5
Discipline:   ███████████████ 3.8/5
Hard Work:    ████████████████████ 4.1/5
Gratitude:    ███████████████████ 4.0/5
```

### Values-Based Reporting Examples

#### Individual Candidate Profile
```
Candidate: Adarshyadav (ID: 31)
┌─────────────┬───────┬──────────────────────────────┐
│ Value       │ Score │ Assessment Notes             │
├─────────────┼───────┼──────────────────────────────┤
│ Integrity   │ 5/5   │ Honest in technical approach │
│ Honesty     │ 5/5   │ Transparent communication    │
│ Discipline  │ 4/5   │ Consistent work patterns     │
│ Hard Work   │ 5/5   │ Goes above expectations      │
│ Gratitude   │ 4/5   │ Appreciates team feedback    │
└─────────────┴───────┴──────────────────────────────┘
Overall Average: 4.6/5 - Strongly Recommended
```

## 🤖 Talah AI Agent Capabilities with Examples

### Advanced Features

#### Resume Analysis Example
```bash
# POST /analyze - Analyze single candidate
curl -X POST http://localhost:9000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 31,
    "name": "Adarshyadav",
    "email": "adarshyadav1019@gmail.com"
  }'

# Response:
{
  "status": "success",
  "analysis": {
    "overall_score": 92,
    "technical_skills": {
      "score": 88,
      "strengths": ["Programming", "Problem Solving"],
      "areas_for_growth": ["Leadership"]
    },
    "values_prediction": {
      "integrity": 4.8,
      "honesty": 4.6,
      "discipline": 4.2,
      "hard_work": 4.7,
      "gratitude": 4.1
    },
    "ai_recommendations": [
      "Strong candidate for technical roles",
      "Consider for senior positions"
    ],
    "confidence_level": "High"
  }
}
```

#### Candidate Scoring Algorithm (0-100)
```
Scoring Breakdown for Adarshyadav:
┌─────────────────────┬───────┬─────────────────────────────┐
│ Factor              │ Score │ Details                     │
├─────────────────────┼───────┼─────────────────────────────┤
│ Technical Skills    │ 88/100│ Strong programming ability  │
│ Experience Match    │ 92/100│ Highly relevant background  │
│ Values Alignment    │ 96/100│ Excellent cultural fit      │
│ Communication       │ 85/100│ Clear, professional style   │
│ Growth Potential    │ 90/100│ Shows learning agility      │
├─────────────────────┼───────┼─────────────────────────────┤
│ OVERALL SCORE       │ 92/100│ Strongly Recommended        │
└─────────────────────┴───────┴─────────────────────────────┘
```

## 🛠️ Development

### Local Development
```bash
# Start services
docker compose up --build

# View logs
docker compose logs -f gateway
docker compose logs -f agent
docker compose logs -f portal

# Stop services
docker compose down
```

### Database Access
```bash
# Connect to PostgreSQL
docker exec -it bhiv-hr-platform-db-1 psql -U bhiv_user -d bhiv_hr

# View tables
\dt

# Query candidates
SELECT * FROM candidates LIMIT 5;

# Exit PostgreSQL
\q
```

### Development Scripts with Examples

#### Enhanced Resume Processing
```bash
# Process resumes with comprehensive data extraction
python scripts/simple_enhanced_processor.py

# Output:
# Processing 27 resumes...
# Processing: AdarshYadavResume.pdf
#   -> Adarshyadav (Entry-level)
# Processing: Anurag_CV.pdf
#   -> Anurag (Entry-level) 
# Processing: ArulselvamJeganResume.pdf
#   -> Arulselvamjegan (Entry-level)
# Saved 27 candidates to enhanced_candidates.csv

# Enhanced Fields Extracted:
# - Basic: name, email, phone, location
# - Professional: experience_years, seniority_level, education_level
# - Technical: technical_skills (categorized by domain)
# - System: cv_url, status, job_id
```

#### Test API Endpoints
```bash
# Run comprehensive API tests
python scripts/test_api.py

# Output:
# 🧪 Testing API Gateway...
# ✅ Health check: PASSED
# ✅ Job creation: PASSED
# ✅ Candidate upload: PASSED
# ✅ AI matching: PASSED
# ✅ Values feedback: PASSED
# 📊 All tests completed: 5/5 PASSED
```

#### Initialize Database Tables
```bash
# Create all required database tables
python scripts/init_tables.py

# Output:
# ⏳ Waiting for database connection...
# ✅ Database connection successful!
# 📋 Creating interviews table...
# 📋 Creating offers table...
# ✅ All tables created successfully!
```

#### Auto-Upload Resumes
```bash
# Automatically upload processed candidates to database
python scripts/auto_upload_resumes.py

# Output:
# 📂 Reading processed candidates from data/processed_candidates.csv
# 📤 Uploading 28 candidates to Job ID 1...
# ✅ Successfully uploaded: Adarshyadav
# ✅ Successfully uploaded: Anurag
# 📊 Upload complete: 28/28 candidates added
```

## 📈 MDVP (Minimum Daily Value Push) Implementation

This platform was built following MDVP methodology:

### Day 1 - Foundations ✅
- ✅ API Gateway with FastAPI
- ✅ Data models (Clients, Jobs, Candidates, Feedback)
- ✅ Core endpoints (jobs, candidates, matching)
- ✅ Talah AI integration

### Day 2 - Values & Dashboard ✅  
- ✅ Values rubric UI (1-5 scale for all 5 values)
- ✅ Values feedback storage and retrieval
- ✅ Live dashboard with real data
- ✅ Candidate funnel visualization

### Day 3 - Scheduling, Offers, Reporting ✅
- ✅ Interview scheduling endpoints
- ✅ Offer management system
- ✅ CSV report export with values data
- ✅ API key authentication
- ✅ Complete Docker setup

### Day 4 - Enhanced Data & Testing ✅
- ✅ Enhanced resume processing (11 fields per candidate)
- ✅ Comprehensive candidate profiles with technical skills
- ✅ Database schema updates for enhanced fields
- ✅ End-to-end testing with real enhanced data
- ✅ API security hardening
- ✅ Professional documentation updates

## 🎯 Success Metrics

### Technical Achievements
- ✅ **Enhanced Resume Processing**: 11 comprehensive fields per candidate
- ✅ **Real AI Integration**: Talah agent with 27 actual candidate profiles
- ✅ **Advanced Data Extraction**: Technical skills, seniority, education levels
- ✅ **Live Dashboard**: Real-time data with enhanced candidate profiles
- ✅ **Values Framework**: Complete 5-dimension assessment
- ✅ **Comprehensive Database**: Enhanced schema with professional fields
- ✅ **Docker Deployment**: One-command setup with real data
- ✅ **100% API Coverage**: All endpoints tested with enhanced data

### Business Value
- ✅ **Enhanced Candidate Profiles**: 11 fields for better decision making
- ✅ **Technical Skills Analysis**: Categorized by programming, web dev, cloud/DevOps
- ✅ **Seniority Assessment**: Entry-level, Mid-level, Senior classifications
- ✅ **Location Intelligence**: Geographic distribution of talent pool
- ✅ **Education Tracking**: Masters, Bachelors, PhD level analysis
- ✅ **End-to-End Workflow**: Complete recruiter journey with enhanced data
- ✅ **Values-Driven Hiring**: MDVP compliance with comprehensive profiles
- ✅ **AI-Powered Matching**: Intelligent ranking with 27 real candidates
- ✅ **Real-time Analytics**: Data-driven decisions with enhanced metrics

## 🔄 Continuous Integration

### Daily Push Requirements Met
- **Day 1**: Jobs + Candidates creation ✅
- **Day 2**: Values feedback + Dashboard ✅  
- **Day 3**: Interviews + Offers + Reports ✅
- **Day 4**: Security + Documentation ✅

Each day delivered working, deployable features with real business value.

## 📞 Support

For technical support or questions:
- **Email**: support@bhiv-hr.com
- **Documentation**: http://localhost:8000/docs
- **AI Agent Docs**: http://localhost:9000/docs
- **Project Structure**: See PROJECT_STRUCTURE.md

## 📁 File Organization

- **Services**: All microservices in `services/` directory
- **Data**: Processed data and logs in `data/` directory
- **Scripts**: Utility scripts in `scripts/` directory
- **Configuration**: Environment and config files in `config/` directory
- **Documentation**: All docs in `docs/` directory
- **Resumes**: Resume files in `resume/` directory

---

*Built with Integrity, Honesty, Discipline, Hard Work, and Gratitude* 🏆