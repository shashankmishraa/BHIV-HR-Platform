# 🎯 BHIV HR Platform - Complete Usage Guide

## 🚀 Quick Start (5 Minutes)

### 1. Start the Platform
```bash
git clone <repository-url>
cd bhiv-hr-platform
docker compose up --build
```

### 2. Access Services
- **Portal**: http://localhost:8501 (Main UI)
- **API**: http://localhost:8000/docs (API Documentation)
- **AI Agent**: http://localhost:9000/docs (AI Documentation)

---

## 🏢 API Gateway Functions (Port 8000)

### Core Job Management
```bash
# Create Job
curl -X POST http://localhost:8000/v1/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{"title": "Software Engineer", "description": "Python developer needed", "client_id": 1}'

# List All Jobs
curl -H "X-API-KEY: myverysecureapikey123" http://localhost:8000/v1/jobs
```

### Enhanced Candidate Management
```bash
# Upload Enhanced Candidates (11 fields)
curl -X POST http://localhost:8000/v1/candidates/bulk \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidates": [{
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0123",
      "location": "Mumbai",
      "experience_years": 3,
      "education_level": "Masters",
      "technical_skills": "Python, React, SQL",
      "seniority_level": "Mid-level",
      "cv_url": "https://example.com/cv.pdf",
      "status": "applied",
      "job_id": 1
    }]
  }'

# Get Candidates for Job
curl -H "X-API-KEY: myverysecureapikey123" http://localhost:8000/v1/candidates/job/1
```

### Values Assessment
```bash
# Submit Values Feedback
curl -X POST http://localhost:8000/v1/feedback \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidate_id": 1,
    "reviewer_name": "HR Manager",
    "feedback_text": "Strong technical skills",
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

### Interview & Offer Management
```bash
# Schedule Interview
curl -X POST http://localhost:8000/v1/interviews \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "interview_date": "2025-02-01T10:00:00Z",
    "interviewer": "Tech Lead"
  }'

# Make Job Offer
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

### Analytics & Reporting
```bash
# Get Platform Statistics
curl -H "X-API-KEY: myverysecureapikey123" http://localhost:8000/candidates/stats

# Export Job Report (CSV)
curl -H "X-API-KEY: myverysecureapikey123" \
  http://localhost:8000/v1/reports/job/1/export.csv -o report.csv
```

---

## 🤖 Talah AI Agent Functions (Port 9000)

### Individual Candidate Analysis
```bash
# Analyze Single Candidate
curl -X POST http://localhost:9000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }'

# Response includes:
# - Overall score (0-100)
# - Technical skills assessment
# - Values prediction
# - AI recommendations
# - Confidence level
```

### AI-Powered Matching
```bash
# Get Top-5 Candidates for Job
curl -H "X-API-KEY: myverysecureapikey123" \
  http://localhost:8000/v1/match/1/top

# Returns:
# - Ranked top 5 candidates
# - AI scores for each
# - Skills match percentage
# - Values alignment scores
# - Recommendation strength
```

### Bulk Analysis
```bash
# Analyze All Candidates for Job
curl -X POST http://localhost:9000/match \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}'

# Provides comprehensive analysis of all candidates
```

---

## 🎯 Client Portal Functions (Port 8501)

### Dashboard Overview
**Access**: http://localhost:8501

**Main Features**:
- Real-time candidate statistics
- Job pipeline visualization
- Values distribution charts
- Quick action buttons

### Job Management
1. **Create New Job**
   - Click "Create Job" button
   - Fill job details (title, description, client)
   - Submit to create job posting

2. **View Job Statistics**
   - See candidate counts per job
   - Track interview and offer status
   - Monitor hiring pipeline

### Candidate Management
1. **Upload Candidates**
   - Use "Upload Candidates" section
   - Upload CSV with enhanced fields
   - Bulk import with validation

2. **View Candidate Profiles**
   - Browse enhanced candidate data
   - See technical skills, seniority, education
   - Review location and experience details

### AI-Powered Shortlisting
1. **Generate AI Shortlist**
   - Select job from dropdown
   - Click "Generate Shortlist"
   - View top-5 ranked candidates with scores

2. **Review AI Analysis**
   - See overall candidate scores
   - Review technical skills assessment
   - Check values alignment predictions

### Values Assessment
1. **Submit Candidate Feedback**
   - Select candidate and reviewer
   - Rate on 5 core values (1-5 scale)
   - Add text feedback and recommendation
   - Submit for permanent record

2. **View Values Reports**
   - Individual candidate values profiles
   - Team values distribution charts
   - Historical assessment trends

### Interview & Offer Tracking
1. **Schedule Interviews**
   - Select candidate and interviewer
   - Set date/time
   - Track interview status

2. **Manage Offers**
   - Create salary offers
   - Track offer status (sent/accepted/declined)
   - Monitor offer pipeline

### Reporting & Analytics
1. **Real-time Dashboard**
   - Live candidate pipeline
   - Values distribution visualization
   - Job performance metrics

2. **Export Reports**
   - Download comprehensive CSV reports
   - Include values scores and feedback
   - Generate compliance documentation

---

## 📊 Enhanced Resume Processing

### Automated Processing
```bash
# Process All Resumes (Enhanced)
cd scripts
python simple_enhanced_processor.py

# Extracts 11 fields per resume:
# - Basic: name, email, phone, location
# - Professional: experience_years, seniority_level, education_level
# - Technical: technical_skills (categorized)
# - System: cv_url, status, job_id
```

### Upload Processed Data
```bash
# Upload Enhanced Candidates
python final_upload_test.py

# Uploads all processed candidates with:
# - Technical skills categorization
# - Seniority assessment
# - Education level classification
# - Location intelligence
```

---

## 🔧 System Administration

### Database Management
```bash
# Connect to Database
docker exec -it bhiv-hr-platform-db-1 psql -U bhiv_user -d bhiv_hr

# View Enhanced Schema
\d candidates

# Query Enhanced Data
SELECT name, seniority_level, technical_skills, education_level 
FROM candidates LIMIT 5;
```

### Service Monitoring
```bash
# View Service Logs
docker compose logs -f gateway
docker compose logs -f agent
docker compose logs -f portal

# Check Service Health
curl http://localhost:8000/health
curl http://localhost:9000/health
```

### Data Backup & Restore
```bash
# Backup Database
docker exec bhiv-hr-platform-db-1 pg_dump -U bhiv_user bhiv_hr > backup.sql

# Restore Database
docker exec -i bhiv-hr-platform-db-1 psql -U bhiv_user bhiv_hr < backup.sql
```

---

## 🎯 Complete Workflow Example

### 1. Setup & Data Preparation
```bash
# Start platform
docker compose up --build

# Process resumes
cd scripts && python simple_enhanced_processor.py

# Upload candidates
python final_upload_test.py
```

### 2. Job Creation & Management
```bash
# Create job via API
curl -X POST http://localhost:8000/v1/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{"title": "Senior Developer", "description": "Python expert needed", "client_id": 1}'

# Or use Portal: http://localhost:8501
```

### 3. AI-Powered Candidate Matching
```bash
# Get top candidates
curl -H "X-API-KEY: myverysecureapikey123" \
  http://localhost:8000/v1/match/1/top

# Review in Portal dashboard
```

### 4. Values Assessment
```bash
# Submit values feedback
curl -X POST http://localhost:8000/v1/feedback \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{"candidate_id": 1, "values_scores": {"integrity": 5, "honesty": 4, "discipline": 5, "hard_work": 5, "gratitude": 4}}'
```

### 5. Interview & Offer Process
```bash
# Schedule interview
curl -X POST http://localhost:8000/v1/interviews \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{"candidate_id": 1, "job_id": 1, "interview_date": "2025-02-01T10:00:00Z"}'

# Make offer
curl -X POST http://localhost:8000/v1/offers \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: myverysecureapikey123" \
  -d '{"candidate_id": 1, "job_id": 1, "salary": 120000}'
```

### 6. Reporting & Analytics
```bash
# Export comprehensive report
curl -H "X-API-KEY: myverysecureapikey123" \
  http://localhost:8000/v1/reports/job/1/export.csv -o final_report.csv

# View live dashboard: http://localhost:8501
```

---

## 🏆 Key Benefits

### For Recruiters
- **Enhanced Candidate Profiles**: 11 comprehensive fields per candidate
- **AI-Powered Matching**: Intelligent ranking with confidence scores
- **Values-Based Assessment**: 5-dimension cultural fit evaluation
- **Real-time Analytics**: Live dashboard with pipeline visualization
- **Complete Workflow**: End-to-end process from posting to offer

### For Organizations
- **Technical Skills Intelligence**: Categorized by domain expertise
- **Seniority Assessment**: Entry/Mid/Senior level classifications
- **Location Analytics**: Geographic talent distribution
- **Education Insights**: Degree level tracking and analysis
- **Compliance Reporting**: Comprehensive CSV exports with values data

### For Developers
- **API-First Design**: Complete REST API with Swagger documentation
- **Microservices Architecture**: Scalable, maintainable service separation
- **Docker Deployment**: One-command setup with real data
- **Enhanced Database Schema**: Professional-grade candidate profiles
- **Comprehensive Testing**: End-to-end verification with real candidates

---

*Ready to transform your recruiting with values-driven, AI-powered candidate matching!* 🚀