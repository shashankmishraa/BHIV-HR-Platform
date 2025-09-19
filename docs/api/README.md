# 🔌 BHIV HR Platform API Documentation

Complete API reference for the BHIV HR Platform with 118 tested endpoints (30.51% success rate - requires fixes).

## 🚀 Quick Start

### **Base URLs**
- **Gateway API**: https://bhiv-hr-gateway.onrender.com
- **AI Agent API**: https://bhiv-hr-agent.onrender.com
- **Interactive Docs**: `/docs` endpoint on each service

### **Authentication**
```bash
# API Key Authentication
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway.onrender.com/v1/jobs
```

---

## 🏗️ API Architecture

### **Service Overview**
| Service | Endpoints | Purpose | Base URL |
|---------|-----------|---------|----------|
| **Gateway** | 49 | Core business logic | `/v1/` |
| **AI Agent** | 15 | AI matching & analytics | `/` |
| **Total** | **118** | Tested endpoints | - |
| **Status** | **30.51%** | Success rate | **82 failing** |

---

## 🔐 Gateway API (106 Endpoints)

### **Core Endpoints (4)**
```bash
GET  /                    # API information
GET  /health             # Health check
GET  /test-candidates    # Test data
GET  /http-methods-test  # HTTP method testing
```

### **Job Management (8)**
```bash
POST   /v1/jobs           # Create job
GET    /v1/jobs           # List jobs
GET    /v1/jobs/{id}      # Get job details
PUT    /v1/jobs/{id}      # Update job
DELETE /v1/jobs/{id}      # Delete job
GET    /v1/jobs/search    # Search jobs
GET    /v1/jobs/stats     # Job statistics
POST   /v1/jobs/bulk      # Bulk job operations
```

### **Candidate Management (12)**
```bash
GET    /v1/candidates              # List candidates
POST   /v1/candidates              # Create candidate
GET    /v1/candidates/{id}         # Get candidate
PUT    /v1/candidates/{id}         # Update candidate
DELETE /v1/candidates/{id}         # Delete candidate
GET    /v1/candidates/search       # Search candidates
GET    /v1/candidates/stats        # Candidate statistics
POST   /v1/candidates/bulk         # Bulk operations
POST   /v1/candidates/import       # Import candidates
GET    /v1/candidates/export       # Export candidates
POST   /v1/candidates/merge        # Merge duplicates
GET    /v1/candidates/duplicates   # Find duplicates
POST   /v1/candidates/validate     # Validate data
GET    /v1/candidates/analytics    # Analytics
```

### **AI Matching (8)**
```bash
GET  /v1/match/{job_id}/top        # Top matches for job
GET  /v1/match/performance-test    # Performance testing
GET  /v1/match/cache-status        # Cache status
POST /v1/match/batch               # Batch matching
GET  /v1/match/history             # Match history
POST /v1/match/feedback            # Match feedback
GET  /v1/match/analytics           # Match analytics
POST /v1/match/retrain             # Retrain model
```

### **Security & Authentication (27)**
```bash
# Security Testing (12)
GET  /v1/security/headers          # Security headers
POST /v1/security/test-xss         # XSS testing
POST /v1/security/test-sql-injection # SQL injection test
GET  /v1/security/audit-log        # Audit logs
GET  /v1/security/status           # Security status
POST /v1/security/rotate-keys      # Rotate API keys
GET  /v1/security/policy           # Security policy
GET  /v1/security/threat-detection # Threat detection
POST /v1/security/incident-report  # Report incidents
GET  /v1/security/alert-monitor    # Alert monitoring
POST /v1/security/alert-config     # Configure alerts
GET  /v1/security/backup-status    # Backup status

# Authentication (15)
POST /v1/auth/2fa/setup            # Setup 2FA
POST /v1/auth/2fa/verify           # Verify 2FA
POST /v1/auth/2fa/login            # 2FA login
POST /v1/auth/password/validate    # Validate password
POST /v1/auth/password/generate    # Generate password
POST /v1/auth/password/reset       # Reset password
GET  /v1/auth/password/history     # Password history
POST /v1/auth/api-key/generate     # Generate API key
GET  /v1/auth/api-key/list         # List API keys
DELETE /v1/auth/api-key/{id}       # Delete API key
POST /v1/auth/bulk-password-reset  # Bulk password reset
GET  /v1/auth/active-sessions      # Active sessions
POST /v1/auth/logout-all          # Logout all sessions
GET  /v1/auth/session-stats       # Session statistics
POST /v1/auth/validate-token      # Validate token
```

### **Session Management (6)**
```bash
POST /v1/sessions/create    # Create session
GET  /v1/sessions/validate  # Validate session
POST /v1/sessions/logout    # Logout session
GET  /v1/sessions/active    # Active sessions
POST /v1/sessions/cleanup   # Cleanup sessions
GET  /v1/sessions/stats     # Session statistics
```

### **Interview Management (8)**
```bash
GET    /v1/interviews           # List interviews
POST   /v1/interviews           # Create interview
GET    /v1/interviews/{id}      # Get interview
PUT    /v1/interviews/{id}      # Update interview
DELETE /v1/interviews/{id}      # Delete interview
POST   /v1/interviews/schedule  # Schedule interview
GET    /v1/interviews/calendar  # Interview calendar
POST   /v1/interviews/feedback  # Interview feedback
```

### **Monitoring & Analytics (24)**
```bash
# Monitoring (12)
GET /metrics                      # Prometheus metrics
GET /health/detailed             # Detailed health
GET /monitoring/errors           # Error monitoring
GET /monitoring/dependencies     # Dependencies
GET /monitoring/performance      # Performance metrics
GET /monitoring/alerts           # Alert status
GET /monitoring/logs             # Log access
GET /monitoring/dashboard        # Monitoring dashboard
GET /monitoring/export           # Export metrics
GET /monitoring/config           # Configuration
GET /monitoring/test             # Test monitoring
GET /monitoring/reset            # Reset metrics

# Analytics (6)
GET /candidates/stats            # Candidate statistics
GET /v1/reports/summary          # Summary reports
GET /v1/analytics/dashboard      # Analytics dashboard
GET /v1/analytics/export         # Export analytics
GET /v1/analytics/trends         # Trend analysis
GET /v1/analytics/predictions    # Predictive analytics

# Database (4)
GET  /v1/database/health         # Database health
POST /v1/database/add-interviewer-column # Add column
GET  /v1/database/stats          # Database stats
POST /v1/database/migrate        # Run migrations

# Client Portal (3)
POST /v1/client/login            # Client login
GET  /v1/client/profile          # Client profile
PUT  /v1/client/profile          # Update profile
```

---

## 🤖 AI Agent API (15 Endpoints)

### **Core Operations (3)**
```bash
GET /           # Service information
GET /health     # Health check
GET /status     # Service status
```

### **AI Matching (8)**
```bash
POST /match              # Basic matching
POST /match/batch        # Batch matching
POST /match/semantic     # Semantic matching
POST /match/advanced     # Advanced matching
POST /match/explain      # Match explanation
POST /match/feedback     # Provide feedback
POST /match/retrain      # Retrain model
POST /match/benchmark    # Performance benchmark
```

### **Analytics & System (4)**
```bash
GET /analytics     # AI analytics
GET /performance   # Performance metrics
GET /metrics       # System metrics
GET /version       # Version information
GET /diagnostics   # System diagnostics
```

---

## 📝 Request/Response Examples

### **Create Job**
```bash
POST /v1/jobs
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "title": "Senior Software Engineer",
  "description": "Full-stack development role",
  "required_skills": ["Python", "React", "PostgreSQL"],
  "experience_level": "Senior",
  "location": "Remote",
  "salary_range": "$120,000 - $150,000"
}

# Response
{
  "id": "job_123",
  "title": "Senior Software Engineer",
  "status": "active",
  "created_at": "2025-01-17T10:00:00Z"
}
```

### **AI Matching**
```bash
POST /match
Content-Type: application/json

{
  "job_id": "job_123",
  "candidate_ids": ["cand_456", "cand_789"],
  "options": {
    "include_explanation": true,
    "threshold": 0.7
  }
}

# Response
{
  "matches": [
    {
      "candidate_id": "cand_456",
      "score": 0.92,
      "explanation": {
        "strengths": ["Strong Python skills", "React experience"],
        "gaps": ["Limited PostgreSQL experience"],
        "recommendation": "Excellent match, consider for interview"
      }
    }
  ]
}
```

### **Search Candidates**
```bash
GET /v1/candidates/search?skills=Python,React&experience=Senior&location=Remote
Authorization: Bearer your-api-key

# Response
{
  "candidates": [
    {
      "id": "cand_456",
      "name": "John Doe",
      "skills": ["Python", "React", "Node.js"],
      "experience": "5 years",
      "location": "Remote"
    }
  ],
  "total": 1,
  "page": 1
}
```

---

## 🔒 Authentication & Security

### **API Key Authentication**
```bash
# Header-based authentication
Authorization: Bearer your-api-key

# Query parameter (not recommended for production)
?api_key=your-api-key
```

### **Rate Limiting**
```bash
# Limits per minute
API Endpoints: 60 requests/minute
Form Submissions: 10 requests/minute
Bulk Operations: 5 requests/minute

# Headers in response
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1642428000
```

### **Security Headers**
```bash
# Required headers for secure requests
Content-Type: application/json
Authorization: Bearer your-api-key
X-Requested-With: XMLHttpRequest (for CSRF protection)
```

---

## 📊 Response Codes & Error Handling

### **HTTP Status Codes**
```bash
200 OK           # Success
201 Created      # Resource created
400 Bad Request  # Invalid request
401 Unauthorized # Authentication required
403 Forbidden    # Access denied
404 Not Found    # Resource not found
429 Too Many Requests # Rate limit exceeded
500 Internal Server Error # Server error
```

### **Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    },
    "timestamp": "2025-01-17T10:00:00Z"
  }
}
```

---

## 🚀 Performance & Optimization

### **Response Times**
- **Simple Queries**: <50ms
- **Complex Searches**: <200ms
- **AI Matching**: <500ms
- **Bulk Operations**: <2s

### **Pagination**
```bash
# Query parameters
?page=1&limit=20&sort=created_at&order=desc

# Response metadata
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

### **Caching**
```bash
# Cache headers
Cache-Control: public, max-age=300
ETag: "abc123"
Last-Modified: Wed, 17 Jan 2025 10:00:00 GMT
```

---

## 🔧 SDK & Integration

### **cURL Examples**
```bash
# Health check
curl https://bhiv-hr-gateway.onrender.com/health

# List jobs with authentication
curl -H "Authorization: Bearer your-api-key" \
     https://bhiv-hr-gateway.onrender.com/v1/jobs

# Create candidate
curl -X POST \
     -H "Authorization: Bearer your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"name":"John Doe","email":"john@example.com"}' \
     https://bhiv-hr-gateway.onrender.com/v1/candidates
```

### **Python SDK Example**
```python
import requests

class BHIVClient:
    def __init__(self, api_key, base_url="https://bhiv-hr-gateway.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_jobs(self):
        response = requests.get(f"{self.base_url}/v1/jobs", headers=self.headers)
        return response.json()
    
    def create_candidate(self, candidate_data):
        response = requests.post(
            f"{self.base_url}/v1/candidates", 
            json=candidate_data, 
            headers=self.headers
        )
        return response.json()

# Usage
client = BHIVClient("your-api-key")
jobs = client.get_jobs()
```

---

## 📚 Additional Resources

### **Interactive Documentation**
- **Gateway API**: https://bhiv-hr-gateway.onrender.com/docs
- **AI Agent API**: https://bhiv-hr-agent.onrender.com/docs

### **Testing Tools**
- **Postman Collection**: Available in `/docs/api/postman/`
- **OpenAPI Spec**: Available at `/openapi.json` on each service
- **Test Scripts**: Available in `/tests/` directory

### **Support**
- **GitHub Issues**: Repository issues page
- **Documentation**: Complete guides in `/docs/`
- **Live Demo**: Test endpoints with demo credentials

---

**Last Updated**: January 17, 2025 | **API Version**: v1 | **Total Endpoints**: 121