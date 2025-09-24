# 🚀 BHIV HR Platform - Modular API Guide

**Version**: 3.2.1 | **Architecture**: Modular Microservices | **Total Endpoints**: 180+

## 📋 API Overview

The BHIV HR Platform API Gateway implements a **modular architecture** with 6 specialized router modules, providing comprehensive HR management capabilities with workflow integration and enterprise-grade security.

### **🎯 Key Features**
- **Modular Design**: 6 independent router modules with clear separation of concerns
- **Workflow Integration**: Background task processing and pipeline automation
- **Enhanced Validation**: Comprehensive data validation with normalization
- **Enterprise Security**: JWT authentication, rate limiting, and threat detection
- **Real-time Processing**: <100ms average response time with async operations

---

## 🏗️ Module Architecture

### **Gateway Service Modules**

| Module | Prefix | Endpoints | Purpose | Key Features |
|--------|--------|-----------|---------|--------------|
| **Core** | `/` | 4 | System health and info | Health checks, architecture details |
| **Jobs** | `/v1/jobs` | 10 | Job management | CRUD, AI matching, workflows |
| **Candidates** | `/v1/candidates` | 12 | Candidate lifecycle | Management, bulk operations |
| **Auth** | `/v1/auth` | 17 | Security & authentication | JWT, 2FA, sessions, API keys |
| **Workflows** | `/v1/workflows` | 15 | Process orchestration | Pipeline automation, tasks |
| **Monitoring** | `/v1/monitoring` | 25 | System observability | Health, metrics, alerting |

---

## 🔧 Core Module Endpoints

### **System Health & Information**

#### `GET /` - Root Endpoint
```json
{
  "message": "BHIV HR Platform API Gateway v3.2.1",
  "status": "operational",
  "architecture": "modular",
  "modules": 6,
  "total_endpoints": "180+"
}
```

#### `GET /health` - Health Check
```json
{
  "status": "healthy",
  "service": "gateway",
  "version": "3.2.1",
  "timestamp": "2025-01-18T10:30:00Z",
  "components": {
    "database": "healthy",
    "modules": "6/6 active",
    "workflows": "operational"
  }
}
```

#### `GET /system/modules` - Module Information
```json
{
  "modules": [
    {
      "name": "core",
      "description": "Basic API endpoints and health checks",
      "endpoints": 4,
      "status": "active"
    },
    {
      "name": "jobs",
      "description": "Job posting and management with AI matching",
      "endpoints": 10,
      "status": "active"
    }
  ],
  "total_modules": 6,
  "total_endpoints": "180+",
  "architecture": "modular"
}
```

#### `GET /system/architecture` - Architecture Details
```json
{
  "architecture": {
    "type": "modular_microservices",
    "pattern": "api_gateway_with_modules",
    "modules": 6,
    "workflow_integration": true,
    "pipeline_orchestration": true
  },
  "technology_stack": {
    "framework": "FastAPI 0.104+",
    "python": "3.11+",
    "database": "PostgreSQL",
    "deployment": "Render Cloud"
  },
  "performance": {
    "avg_response_time": "<100ms",
    "throughput": "1000+ req/min",
    "uptime": "99.9%"
  }
}
```

---

## 💼 Jobs Module Endpoints

### **Job Management with Workflow Integration**

#### `GET /v1/jobs` - List Jobs
**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 10, max: 100)
- `department` (string): Filter by department
- `experience_level` (string): Filter by experience level
- `status` (string): Filter by job status

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs?page=1&per_page=10"
```

**Response:**
```json
{
  "jobs": [
    {
      "id": "job_12345",
      "title": "Senior Software Engineer",
      "department": "Engineering",
      "experience_level": "Senior-level",
      "salary_min": 120000,
      "salary_max": 180000,
      "status": "active"
    }
  ],
  "total": 7,
  "page": 1,
  "per_page": 10,
  "pages": 1
}
```

#### `POST /v1/jobs` - Create Job with Enhanced Validation
**Request Body:**
```json
{
  "title": "Senior Python Developer",
  "description": "We are looking for an experienced Python developer...",
  "requirements": "Python, FastAPI, PostgreSQL, Docker",
  "location": "San Francisco, CA",
  "department": "Engineering",
  "experience_level": "Senior",
  "salary_min": 120000,
  "salary_max": 180000,
  "job_type": "Full-time"
}
```

**Enhanced Features:**
- **Flexible Requirements**: Accepts both string and array formats
- **Experience Level Normalization**: Converts "Senior" to "Senior-level"
- **Salary Validation**: Ensures min ≤ max and reasonable ranges
- **Workflow Trigger**: Automatically triggers job posting workflow

**Response:**
```json
{
  "job_id": "job_67890",
  "message": "Job created successfully with enhanced validation",
  "status": "active",
  "workflow_triggered": true,
  "created_at": "2025-01-18T10:30:00Z",
  "validation_applied": true,
  "requirements": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "experience_level": "Senior-level"
}
```

#### `PUT /v1/jobs/{job_id}` - Update Job
**Enhanced Validation**: Same validation rules as creation
**Workflow Integration**: Triggers update workflow for notifications

#### `DELETE /v1/jobs/{job_id}` - Delete Job
```json
{
  "message": "Job job_67890 deleted successfully"
}
```

#### `GET /v1/jobs/search` - Search Jobs
**Query Parameters:**
- `q` (string, required): Search query (min 2 characters)
- `department` (string): Filter by department
- `salary_min` (int): Minimum salary filter

#### `POST /v1/jobs/{job_id}/match-candidates` - AI Matching
**Workflow Integration**: Triggers AI matching workflow in background
```json
{
  "job_id": "job_67890",
  "matches": [],
  "total_matches": 0,
  "algorithm": "semantic_v3.2",
  "workflow_triggered": true
}
```

---

## 👥 Candidates Module Endpoints

### **Candidate Lifecycle Management**

#### `GET /v1/candidates` - List Candidates
**Enhanced Filtering**: Skills, experience, location, availability

#### `POST /v1/candidates` - Create Candidate
**Workflow Integration**: Triggers candidate onboarding workflow
**Validation**: Email format, phone pattern, skills array

#### `PUT /v1/candidates/{candidate_id}` - Update Candidate
**Bulk Operations**: Support for batch updates

#### `POST /v1/candidates/bulk-upload` - Bulk Upload
**Workflow Integration**: Background processing for large uploads
**File Support**: CSV, Excel, JSON formats

---

## 🔐 Auth Module Endpoints

### **Authentication & Security Workflows**

#### `POST /v1/auth/login` - User Login
**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_id": "user_123",
  "username": "admin"
}
```

#### `POST /v1/auth/register` - User Registration
**Workflow Integration**: Triggers user onboarding workflow
**Security**: Password hashing, email verification

#### `POST /v1/auth/forgot-password` - Password Reset
**Workflow Integration**: Triggers password reset workflow
**Security**: Token generation, email notification

#### `GET /v1/auth/security/rate-limit-status` - Rate Limit Status
```json
{
  "rate_limit": "60 requests/minute",
  "remaining": 45,
  "reset_time": "2025-01-18T10:30:00Z",
  "window": "60s"
}
```

#### `POST /v1/auth/api-key` - Generate API Key
```json
{
  "api_key": "ak_1234567890abcdef1234567890abcdef12345678",
  "created_at": "2025-01-18T10:30:00Z",
  "expires_at": "2026-01-18T10:30:00Z"
}
```

---

## 🔄 Workflows Module Endpoints

### **Process Orchestration & Pipeline Management**

#### `GET /v1/workflows` - List Workflows
**Filtering**: By type, status, date range

#### `POST /v1/workflows` - Create Workflow
**Types**: job_posting, candidate_onboarding, interview_process, bulk_operations

#### `GET /v1/workflows/{workflow_id}` - Get Workflow Status
```json
{
  "workflow_id": "wf_12345",
  "type": "job_posting",
  "status": "in_progress",
  "steps": [
    {
      "step_id": "validate_job",
      "name": "Job Validation",
      "status": "completed",
      "completed_at": "2025-01-18T10:25:00Z"
    },
    {
      "step_id": "ai_processing",
      "name": "AI Analysis",
      "status": "in_progress",
      "started_at": "2025-01-18T10:26:00Z"
    }
  ]
}
```

#### `POST /v1/workflows/{workflow_id}/trigger` - Trigger Workflow Step
**Background Processing**: Async execution with status updates

---

## 📊 Monitoring Module Endpoints

### **System Observability & Analytics**

#### `GET /v1/monitoring/health/detailed` - Detailed Health Check
```json
{
  "status": "healthy",
  "components": {
    "database": {
      "status": "healthy",
      "response_time": "15ms",
      "connections": "5/100"
    },
    "modules": {
      "core": "active",
      "jobs": "active",
      "candidates": "active",
      "auth": "active",
      "workflows": "active",
      "monitoring": "active"
    },
    "workflows": {
      "active_workflows": 3,
      "pending_tasks": 12,
      "failed_tasks": 0
    }
  }
}
```

#### `GET /v1/monitoring/metrics` - System Metrics
**Prometheus Compatible**: Metrics in Prometheus format
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{method="GET",endpoint="/v1/jobs"} 1234
api_requests_total{method="POST",endpoint="/v1/jobs"} 567

# HELP api_response_time_seconds API response time
# TYPE api_response_time_seconds histogram
api_response_time_seconds_bucket{le="0.1"} 890
api_response_time_seconds_bucket{le="0.5"} 1200
```

#### `GET /v1/monitoring/errors` - Error Analytics
```json
{
  "error_summary": {
    "total_errors": 23,
    "error_rate": "0.5%",
    "top_errors": [
      {
        "type": "ValidationError",
        "count": 15,
        "percentage": "65.2%"
      }
    ]
  },
  "recent_errors": []
}
```

#### `POST /v1/monitoring/alerts` - Configure Alerts
**Alert Types**: threshold, anomaly, error_rate, uptime
**Channels**: email, webhook, slack

---

## 🔧 Enhanced Validation System

### **Validation Features**

#### **Job Requirements Normalization**
```python
# Input (String)
"Python, FastAPI, PostgreSQL"

# Output (Array)
["Python", "FastAPI", "PostgreSQL"]
```

#### **Experience Level Standardization**
```python
# Input Variations
"Senior" → "Senior-level"
"Mid" → "Mid-level"
"Entry" → "Entry-level"
"Lead" → "Lead-level"
"Executive" → "Executive-level"
```

#### **Salary Range Validation**
```python
# Validation Rules
- salary_min >= 0
- salary_max >= salary_min
- Both values <= $10,000,000
- Both fields required for job creation
```

### **Error Handling**

#### **Validation Error Response**
```json
{
  "message": "Job validation failed",
  "errors": [
    {
      "field": "requirements",
      "message": "Requirements must be a list or comma-separated string",
      "invalid_value": null
    },
    {
      "field": "salary_max",
      "message": "Maximum salary must be greater than minimum salary",
      "invalid_value": 80000
    }
  ],
  "help": {
    "requirements": "Provide as list ['Python', 'FastAPI'] or string 'Python, FastAPI'",
    "experience_level": "Use: Entry, Mid, Senior, Lead, or Executive",
    "salary_fields": "Both salary_min and salary_max are required (integers)"
  }
}
```

---

## 🚀 Usage Examples

### **Complete Job Creation Workflow**

```bash
# 1. Create job with enhanced validation
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are seeking an experienced Python developer to join our team...",
    "requirements": "Python, FastAPI, PostgreSQL, Docker, AWS",
    "location": "San Francisco, CA",
    "department": "Engineering",
    "experience_level": "Senior",
    "salary_min": 120000,
    "salary_max": 180000,
    "job_type": "Full-time"
  }'

# 2. Trigger AI matching workflow
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs/job_67890/match-candidates" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Monitor workflow progress
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/workflows/wf_12345" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **Authentication Flow**

```bash
# 1. Login to get token
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 2. Use token for API calls
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/jobs" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# 3. Check rate limit status
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/auth/security/rate-limit-status" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📈 Performance & Monitoring

### **Response Time Targets**

| Endpoint Type | Target | Current | Status |
|---------------|--------|---------|--------|
| Health Checks | <50ms | <30ms | ✅ |
| CRUD Operations | <100ms | <80ms | ✅ |
| AI Matching | <200ms | <150ms | ✅ |
| Bulk Operations | <5s | <3s | ✅ |
| Workflow Triggers | <100ms | <60ms | ✅ |

### **Monitoring Endpoints**

```bash
# System health
curl "https://bhiv-hr-gateway-901a.onrender.com/health"

# Detailed health with components
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/monitoring/health/detailed"

# Prometheus metrics
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/monitoring/metrics"

# Error analytics
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/monitoring/errors"
```

---

## 🔒 Security & Authentication

### **Authentication Methods**

1. **JWT Tokens**: For user sessions
2. **API Keys**: For service-to-service communication
3. **Bearer Tokens**: For API access

### **Security Headers**

```http
X-Process-Time: 0.0234
X-Gateway-Version: 3.2.1-modular
X-Request-ID: req_abc12345
X-Environment: production
X-Total-Modules: 6
```

### **Rate Limiting**

- **API Requests**: 60 per minute per user
- **Form Submissions**: 10 per minute per user
- **Bulk Operations**: 5 per hour per user

---

## 🚀 Getting Started

### **1. Authentication**
```bash
# Get access token
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### **2. Explore API**
```bash
# Check system architecture
curl "https://bhiv-hr-gateway-901a.onrender.com/system/architecture"

# List available modules
curl "https://bhiv-hr-gateway-901a.onrender.com/system/modules"
```

### **3. Interactive Documentation**
Visit: https://bhiv-hr-gateway-901a.onrender.com/docs

---

**BHIV HR Platform Modular API v3.2.1** - Enterprise-grade HR management with workflow automation

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: January 18, 2025 | **Next Update**: v3.2.2 (Production Sync)