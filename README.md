# BHIV HR Platform

AI-powered recruiting platform with candidate matching and values assessment.

## Quick Start

```bash
docker-compose up -d
```

**Access:**
- Portal: http://localhost:8501
- API: http://localhost:8000/docs
- AI Agent: http://localhost:9000/docs

## Project Structure

```
bhiv-hr-platform/
├── services/
│   ├── gateway/          # FastAPI API Gateway
│   │   ├── app/
│   │   │   ├── main.py   # API endpoints
│   │   │   └── db/schemas.py # Pydantic models
│   │   └── Dockerfile
│   ├── agent/           # AI Matching Service
│   │   ├── app.py       # AI matching logic
│   │   └── Dockerfile
│   ├── portal/          # Streamlit Web UI
│   │   ├── app.py       # Web interface
│   │   └── Dockerfile
│   └── db/
│       └── init.sql     # Database schema
├── scripts/             # Processing scripts
├── resume/             # Resume PDFs (25 files)
├── data/               # Processed data
└── docker-compose.yml  # Service orchestration
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/v1/jobs` | POST/GET | Job management |
| `/v1/candidates/bulk` | POST | Upload candidates |
| `/v1/candidates/job/{id}` | GET | List candidates |
| `/v1/candidates/search` | GET | Search & filter |
| `/v1/match/{id}/top` | GET | AI matching |
| `/v1/feedback` | POST | Values assessment |
| `/v1/interviews` | POST | Schedule interviews |
| `/v1/offers` | POST | Job offers |
| `/candidates/stats` | GET | Statistics |

## Core Features

### Search & Filter
```bash
# Search by name
curl -H "Authorization: Bearer <your-api-key>" \
  "http://localhost:8000/v1/candidates/search?q=Hiten&job_id=1"

# Filter by skills - Returns 18 candidates with Python
curl -H "Authorization: Bearer <your-api-key>" \
  "http://localhost:8000/v1/candidates/search?skills=Python&job_id=1"

# Filter by location
curl -H "Authorization: Bearer <your-api-key>" \
  "http://localhost:8000/v1/candidates/search?location=Mumbai&job_id=1"
```

### AI Matching
```bash
curl -H "Authorization: Bearer <your-api-key>" \
  http://localhost:8000/v1/match/1/top
```

### Bulk Upload
```bash
curl -X POST http://localhost:8000/v1/candidates/bulk \
  -H "Authorization: Bearer <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{"candidates": [{"name": "John Doe", "email": "john@example.com", "job_id": 1}]}'
```

## Database Schema

### Jobs Table
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    client_id INTEGER,
    title VARCHAR(255),
    description TEXT,
    department VARCHAR(100),
    location VARCHAR(255),
    experience_level VARCHAR(50),
    employment_type VARCHAR(50),
    requirements TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Candidates Table
```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    job_id INTEGER,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    location VARCHAR(255),
    cv_url TEXT,
    experience_years INTEGER DEFAULT 0,
    education_level VARCHAR(100),
    technical_skills TEXT,
    seniority_level VARCHAR(50),
    status VARCHAR(50) DEFAULT 'applied',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## System Status
- **Candidates**: 81 processed with enhanced data extraction
- **Jobs**: 1 active with comprehensive requirements
- **Resume Files**: 25+ PDFs processed with AI analysis
- **Values Assessments**: Integrated 5-point scoring system
- **Reports**: CSV export with complete candidate lifecycle data
- **MDVP Compliance**: 4/4 days successful value delivery

## Sample Output

**Search Response:**
```json
{
  "search_query": "",
  "filters": {"job_id": 1, "skills": "Python", "location": "", "experience_min": 0},
  "candidates": [
    {
      "id": 16,
      "name": "Rashpal",
      "email": "rashpalsingh43434@gmail.com",
      "phone": "+918828396454",
      "location": "Mumbai",
      "experience_years": 2,
      "technical_skills": "NumPy, Pandas, Go, Python, AI",
      "seniority_level": "Junior",
      "status": "applied"
    }
  ],
  "count": 18,
  "message": "Found 18 candidates"
}
```

## Authentication
All endpoints require Bearer token:
```
Authorization: Bearer <your-secure-api-key>
```

**Security Notes:**
- Generate secure API keys: `openssl rand -hex 32`
- Use environment variables for all secrets
- Enable HTTPS in production
- Implement rate limiting for API endpoints

## Environment Setup

### Required Environment Variables
Create `.env` file in project root:
```bash
# Database Configuration
DATABASE_URL=postgresql://bhiv_user:secure_password_here@db:5432/bhiv_hr
POSTGRES_USER=bhiv_user
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=bhiv_hr

# API Security (Generate with: openssl rand -hex 32)
API_KEY_SECRET=your_secure_api_key_here_min_32_chars
JWT_SECRET_KEY=your_jwt_secret_key_here_min_32_chars

# Application Settings
QUEUE_WORKERS=5
AI_MATCHING_ENABLED=true
ENVIRONMENT=development

# Security Settings
CORS_ORIGINS=http://localhost:8501,http://localhost:3000
SESSION_TIMEOUT=3600
API_RATE_LIMIT=100

# Service URLs
AGENT_SERVICE_URL=http://agent:9000
GATEWAY_URL=http://gateway:8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
```

### Deployment Instructions

1. **Clone Repository**
```bash
git clone <repository-url>
cd bhiv-hr-platform
```

2. **Environment Setup**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start Services**
```bash
docker-compose up -d
```

4. **Verify Deployment**
```bash
# Check all services are running
docker-compose ps

# Test API health
curl http://localhost:8000/health

# Test AI agent
curl http://localhost:9000/health
```

5. **Access Applications**
- **Portal**: http://localhost:8501 (Recruiter Interface)
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **AI Agent**: http://localhost:9000/docs (AI Service)

### Production Deployment

1. **Security Hardening**
```bash
# Generate secure API keys
openssl rand -hex 32

# Update .env with production values
API_KEY_SECRET=<your-secure-key>
DATABASE_URL=<production-db-url>
```

2. **SSL/TLS Setup**
```bash
# Add reverse proxy (nginx/traefik)
# Configure SSL certificates
# Update CORS origins
```

3. **Monitoring**
```bash
# Add health check endpoints
# Configure logging
# Set up alerting
```

## Values Integration

### Core Values Assessment (1-5 Scale)
- **Integrity**: Moral uprightness and ethical behavior
- **Honesty**: Truthfulness and transparency  
- **Discipline**: Self-control and consistency
- **Hard Work**: Dedication and perseverance
- **Gratitude**: Appreciation and humility

### MDVP Compliance
Daily value delivery tracking ensures continuous progress:
- Day 1: Foundation & Security
- Day 2: Values Assessment & Dashboard
- Day 3: Scheduling & Reports
- Day 4: Polish & Documentation

## API Usage Examples

### Export Job Report with Values
```bash
curl -H "Authorization: Bearer <your-api-key>" \
  "http://localhost:8000/v1/reports/job/1/export.csv" \
  --output job_report.csv
```

### Submit Values Assessment
```bash
curl -X POST http://localhost:8000/v1/feedback \
  -H "Authorization: Bearer <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "reviewer": "HR Manager",
    "feedback_text": "Excellent candidate with strong values alignment",
    "values_scores": {
      "integrity": 5,
      "honesty": 4,
      "discipline": 5,
      "hard_work": 5,
      "gratitude": 4
    }
  }'
```

## Tech Stack
- **Backend**: FastAPI, PostgreSQL
- **AI**: Custom matching algorithm with semantic analysis
- **Frontend**: Streamlit with real-time API integration
- **Deployment**: Docker Compose with health checks
- **Authentication**: Bearer tokens with secure validation
- **Reports**: CSV export with comprehensive values data