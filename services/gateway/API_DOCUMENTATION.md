# BHIV HR Platform Gateway - Complete API Documentation
**Version: 3.2.0 | Production Ready**

## 🚀 Overview

The BHIV HR Platform Gateway provides a comprehensive REST API with 180+ endpoints organized into 6 modular components. This documentation covers all available endpoints, authentication, and usage examples.

## 🔗 Base URLs

### Production (Live)
- **Gateway API**: `https://bhiv-hr-gateway-901a.onrender.com`
- **Interactive Docs**: `https://bhiv-hr-gateway-901a.onrender.com/docs`
- **ReDoc**: `https://bhiv-hr-gateway-901a.onrender.com/redoc`

### Local Development
- **Gateway API**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`

## 🔐 Authentication

### API Key Authentication
```bash
# Include in headers
Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### JWT Token Authentication
```bash
# Login to get token
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Use token in subsequent requests
Authorization: Bearer <jwt_token>
```

## 📋 Module Overview

| Module | Endpoints | Purpose | Prefix |
|--------|-----------|---------|--------|
| **Core** | 4 | Basic API & health checks | `/` |
| **Candidates** | 12 | Candidate management | `/v1/candidates` |
| **Jobs** | 10 | Job management & AI matching | `/v1/jobs` |
| **Auth** | 17 | Authentication & security | `/v1/auth` |
| **Workflows** | 15 | Workflow orchestration | `/v1/workflows` |
| **Monitoring** | 25+ | System monitoring & analytics | `/` |

## 🔧 Core Module Endpoints

### System Information
```bash
# API Root
GET /
# Response: System information and module overview

# System Modules
GET /system/modules
# Response: Detailed module information

# System Architecture
GET /system/architecture
# Response: Architecture and technology stack details
```

### Health Checks
```bash
# Basic Health Check
GET /health
# Response: Basic system health status

# Detailed Health Check
GET /health/detailed
# Response: Comprehensive system health with components

# Simple Health Check
GET /health/simple
# Response: Minimal health status
```

## 👥 Candidates Module Endpoints

### CRUD Operations
```bash
# List Candidates (with filtering)
GET /v1/candidates?page=1&per_page=10&search=john&skills=python&location=mumbai

# Create Candidate (triggers onboarding workflow)
POST /v1/candidates
Content-Type: application/json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "skills": ["Python", "FastAPI", "React"],
  "experience_years": 5,
  "location": "Mumbai",
  "designation": "Software Engineer",
  "education": "Masters"
}

# Get Candidate Details
GET /v1/candidates/{candidate_id}

# Update Candidate
PUT /v1/candidates/{candidate_id}
Content-Type: application/json
{
  "name": "John Smith",
  "skills": ["Python", "FastAPI", "React", "Docker"]
}

# Delete Candidate
DELETE /v1/candidates/{candidate_id}
```

### Bulk Operations
```bash
# Bulk Create Candidates (triggers bulk workflow)
POST /v1/candidates/bulk
Content-Type: application/json
[
  {
    "name": "Candidate 1",
    "email": "candidate1@example.com",
    "skills": ["Python", "Django"]
  },
  {
    "name": "Candidate 2", 
    "email": "candidate2@example.com",
    "skills": ["JavaScript", "React"]
  }
]
```

### Additional Operations
```bash
# Get Candidate Applications
GET /v1/candidates/{candidate_id}/applications

# Get Candidate Interviews
GET /v1/candidates/{candidate_id}/interviews

# Upload Resume
POST /v1/candidates/{candidate_id}/resume
Content-Type: multipart/form-data
file: <resume_file>

# Search Candidates
GET /v1/candidates/search?q=python&skills=fastapi,react&location=mumbai

# Get Candidate Statistics
GET /v1/candidates/stats

# Add Candidate Note
POST /v1/candidates/{candidate_id}/notes
Content-Type: application/x-www-form-urlencoded
note=Great candidate for senior role
```

## 💼 Jobs Module Endpoints

### CRUD Operations
```bash
# List Jobs (with filtering)
GET /v1/jobs?page=1&per_page=10&department=engineering&experience_level=Senior

# Create Job (triggers job posting workflow)
POST /v1/jobs
Content-Type: application/json
{
  "title": "Senior Software Engineer",
  "description": "We are looking for an experienced software engineer...",
  "requirements": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "location": "Remote",
  "department": "Engineering",
  "experience_level": "Senior",
  "salary_min": 120000,
  "salary_max": 180000,
  "job_type": "Full-time",
  "company_id": "tech_company_001"
}

# Get Job Details
GET /v1/jobs/{job_id}

# Update Job
PUT /v1/jobs/{job_id}

# Delete Job
DELETE /v1/jobs/{job_id}
```

### AI Matching & Analytics
```bash
# Match Candidates to Job (triggers AI matching workflow)
POST /v1/jobs/{job_id}/match-candidates

# Get Match Score between Job and Candidate
GET /v1/jobs/{job_id}/match-score/{candidate_id}

# Search Jobs
GET /v1/jobs/search?q=engineer&department=engineering&salary_min=100000

# Get Job Applications
GET /v1/jobs/{job_id}/applications

# Get Job Analytics
GET /v1/jobs/analytics
```

## 🔐 Authentication Module Endpoints

### User Management
```bash
# User Login
POST /v1/auth/login
Content-Type: application/x-www-form-urlencoded
username=admin&password=admin123

# User Logout
POST /v1/auth/logout

# User Registration (triggers onboarding workflow)
POST /v1/auth/register
Content-Type: application/json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword123",
  "role": "hr_manager"
}

# Get User Profile
GET /v1/auth/profile

# Update User Profile
PUT /v1/auth/profile
Content-Type: application/x-www-form-urlencoded
email=updated@example.com&name=Updated Name
```

### Token Management
```bash
# Refresh Access Token
POST /v1/auth/refresh
Content-Type: application/x-www-form-urlencoded
refresh_token=<refresh_token>

# Generate API Key
POST /v1/auth/api-key

# Validate Token
POST /v1/auth/security/validate-token
Content-Type: application/x-www-form-urlencoded
token=<jwt_token>
```

### Password Management
```bash
# Forgot Password (triggers reset workflow)
POST /v1/auth/forgot-password
Content-Type: application/x-www-form-urlencoded
email=user@example.com

# Reset Password
POST /v1/auth/reset-password
Content-Type: application/x-www-form-urlencoded
token=<reset_token>&new_password=newpassword123

# Change Password
POST /v1/auth/change-password
Content-Type: application/x-www-form-urlencoded
current_password=oldpass&new_password=newpass
```

### Email Verification
```bash
# Verify Email
POST /v1/auth/verify-email
Content-Type: application/x-www-form-urlencoded
token=<verification_token>

# Resend Verification (triggers verification workflow)
POST /v1/auth/resend-verification
Content-Type: application/x-www-form-urlencoded
email=user@example.com
```

### Session Management
```bash
# Get User Sessions
GET /v1/auth/sessions

# Terminate Session
DELETE /v1/auth/sessions/{session_id}

# Get User Permissions
GET /v1/auth/permissions
```

### Security Endpoints
```bash
# Get Rate Limit Status
GET /v1/auth/security/rate-limit-status
```

## 🔄 Workflows Module Endpoints

### Workflow Management
```bash
# Create Workflow
POST /v1/workflows
Content-Type: application/json
{
  "workflow_type": "candidate_onboarding",
  "metadata": {
    "candidate_data": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}

# List Workflows (with filtering)
GET /v1/workflows?status=completed&workflow_type=job_posting&limit=20

# Get Workflow Details
GET /v1/workflows/{workflow_id}

# Start Workflow Execution
POST /v1/workflows/{workflow_id}/start

# Cancel Workflow
POST /v1/workflows/{workflow_id}/cancel

# Get Workflow Steps
GET /v1/workflows/{workflow_id}/steps
```

### Pipeline Management
```bash
# List Pipeline Templates
GET /v1/workflows/pipelines/templates

# Execute Pipeline Template
POST /v1/workflows/pipelines/execute/{template_id}
Content-Type: application/json
{
  "parameters": {
    "candidate_name": "Jane Smith",
    "candidate_email": "jane@example.com"
  }
}
```

### Analytics & Health
```bash
# Get Workflow Analytics
GET /v1/workflows/analytics

# Get Workflow System Health
GET /v1/workflows/health
```

## 📊 Monitoring Module Endpoints

### System Metrics
```bash
# Prometheus Metrics
GET /metrics

# Performance Metrics
GET /monitoring/performance

# System Capacity
GET /monitoring/capacity

# Service Dependencies
GET /monitoring/dependencies
```

### Error & Log Management
```bash
# Error Analytics
GET /monitoring/errors

# Search Logs
GET /monitoring/logs/search?query=error&level=ERROR&limit=100

# Active Alerts
GET /monitoring/alerts

# Monitoring Dashboard
GET /monitoring/dashboard
```

### Analytics Endpoints
```bash
# Analytics Dashboard
GET /v1/analytics/dashboard

# Candidate Analytics
GET /v1/analytics/candidates

# Job Analytics
GET /v1/analytics/jobs

# Workflow Analytics
GET /v1/analytics/workflows

# Pipeline Analytics
GET /v1/analytics/pipelines
```

### Database Monitoring
```bash
# Database Health
GET /v1/database/health

# Database Statistics
GET /v1/database/statistics
```

### Integration Status
```bash
# Integration System Status
GET /v1/integration/status
```

## 📝 Workflow Types

### Available Workflow Types
1. **`candidate_onboarding`** - Complete candidate onboarding process
2. **`job_posting`** - Job creation and setup workflow
3. **`interview_process`** - Interview scheduling and management
4. **`hiring_pipeline`** - Complete hiring process workflow
5. **`bulk_operations`** - Bulk data processing workflow
6. **`security_audit`** - Security validation and compliance

### Pipeline Templates
1. **`complete_candidate_flow`** - End-to-end candidate processing
2. **`job_posting_workflow`** - Complete job creation pipeline
3. **`interview_management_flow`** - Interview coordination pipeline
4. **`security_audit_pipeline`** - Security validation pipeline
5. **`monitoring_health_check`** - System health monitoring pipeline

## 🔧 Response Formats

### Standard Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "id": "resource_id",
    "created_at": "2025-01-18T10:00:00Z"
  },
  "timestamp": "2025-01-18T10:00:00Z",
  "request_id": "req_abc123"
}
```

### Standard Error Response
```json
{
  "success": false,
  "error": "ValidationError",
  "message": "Request validation failed",
  "details": {
    "field": "email",
    "issue": "Invalid email format"
  },
  "timestamp": "2025-01-18T10:00:00Z",
  "request_id": "req_abc123"
}
```

### Health Check Response
```json
{
  "status": "healthy",
  "service": "BHIV HR Gateway",
  "version": "3.2.0",
  "timestamp": "2025-01-18T10:00:00Z",
  "components": {
    "database": "healthy",
    "workflows": "healthy",
    "cache": "healthy"
  },
  "uptime": "72h 15m 30s"
}
```

## 📈 Rate Limiting

### Default Limits
- **Standard Endpoints**: 60 requests/minute
- **Authentication Endpoints**: 30 requests/minute
- **Workflow Operations**: 20 requests/minute
- **Bulk Operations**: 10 requests/minute

### Rate Limit Headers
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642518000
```

## 🚀 Usage Examples

### Complete Candidate Onboarding Flow
```bash
# 1. Create candidate (triggers workflow)
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/candidates" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "skills": ["Python", "FastAPI"],
    "experience_years": 5
  }'

# 2. Check workflow status
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/workflows?workflow_type=candidate_onboarding" \
  -H "Authorization: Bearer <token>"

# 3. Upload resume
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/candidates/cand_123/resume" \
  -H "Authorization: Bearer <token>" \
  -F "file=@resume.pdf"
```

### Job Posting with AI Matching
```bash
# 1. Create job (triggers workflow)
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Software Engineer",
    "description": "Looking for experienced developer",
    "requirements": ["Python", "FastAPI", "PostgreSQL"],
    "location": "Remote",
    "department": "Engineering",
    "experience_level": "Senior",
    "salary_min": 120000,
    "salary_max": 180000
  }'

# 2. Trigger AI matching
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs/job_123/match-candidates" \
  -H "Authorization: Bearer <token>"

# 3. Get match results
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs/job_123/match-score/cand_123" \
  -H "Authorization: Bearer <token>"
```

## 🔍 Testing & Validation

### Health Check
```bash
curl "https://bhiv-hr-gateway-901a.onrender.com/health"
```

### Authentication Test
```bash
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### API Key Test
```bash
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/candidates" \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
```

## 📞 Support & Resources

### Documentation
- **Interactive API Docs**: `/docs`
- **ReDoc Documentation**: `/redoc`
- **OpenAPI Schema**: `/openapi.json`

### Live System
- **Production API**: https://bhiv-hr-gateway-901a.onrender.com
- **System Status**: https://bhiv-hr-gateway-901a.onrender.com/health
- **System Modules**: https://bhiv-hr-gateway-901a.onrender.com/system/modules

---

**BHIV HR Platform Gateway v3.2.0** - Complete API Documentation

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Status**: 🟢 Production Ready | **Endpoints**: 180+ | **Modules**: 6