# BHIV HR Platform - Current API Reference

## Base URLs

### Production Endpoints
- **API Gateway**: `https://bhiv-hr-gateway-46pz.onrender.com`
- **AI Agent**: `https://bhiv-hr-agent-m1me.onrender.com`
- **HR Portal**: `https://bhiv-hr-portal-cead.onrender.com`
- **Client Portal**: `https://bhiv-hr-client-portal-5g33.onrender.com`

## Authentication

### API Key Authentication
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health
```

### Demo Credentials
```
Username: TECH001
Password: demo123
```

## Core Endpoints

### Health & Monitoring
```
GET /health                    # Basic health check
GET /health/detailed          # Detailed health with dependencies
GET /health/ready             # Readiness probe
GET /health/live              # Liveness probe
GET /metrics                  # Prometheus metrics
GET /metrics/json             # JSON formatted metrics
```

### System Information
```
GET /                         # Service information
GET /system/modules           # Module information
GET /system/architecture      # Architecture details
```

## Gateway API (180+ Endpoints)

### Core Module (4 endpoints)
```
GET /                         # Root endpoint
GET /health                   # Health check
GET /test-candidates          # Test endpoint
GET /architecture             # Architecture info
```

### Candidates Module (12 endpoints)
```
GET /candidates               # List candidates
POST /candidates              # Create candidate
GET /candidates/{id}          # Get candidate
PUT /candidates/{id}          # Update candidate
DELETE /candidates/{id}       # Delete candidate
GET /candidates/{id}/matches  # Get matches
POST /candidates/batch        # Batch upload
GET /candidates/search        # Search candidates
```

### Jobs Module (10 endpoints)
```
GET /jobs                     # List jobs
POST /jobs                    # Create job
GET /jobs/{id}                # Get job
PUT /jobs/{id}                # Update job
DELETE /jobs/{id}             # Delete job
GET /jobs/{id}/candidates     # Get job candidates
POST /jobs/{id}/match         # Match candidates
```

### Authentication Module (17 endpoints)
```
POST /auth/login              # User login
POST /auth/logout             # User logout
POST /auth/register           # User registration
GET /auth/profile             # User profile
PUT /auth/profile             # Update profile
POST /auth/refresh            # Refresh token
POST /auth/reset-password     # Reset password
```

### Workflows Module (15 endpoints)
```
GET /workflows                # List workflows
POST /workflows               # Create workflow
GET /workflows/{id}           # Get workflow
PUT /workflows/{id}           # Update workflow
DELETE /workflows/{id}        # Delete workflow
POST /workflows/{id}/execute  # Execute workflow
GET /workflows/{id}/status    # Workflow status
```

### Monitoring Module (25 endpoints)
```
GET /monitoring/health        # System health
GET /monitoring/metrics       # Performance metrics
GET /monitoring/logs          # System logs
GET /monitoring/alerts        # Active alerts
GET /monitoring/performance   # Performance data
```

## AI Agent API (15 endpoints)

### Core Endpoints
```
GET /                         # Service info
GET /health                   # Health check
GET /status                   # Service status
```

### AI Matching Engine
```
POST /match                   # Match candidates to job
GET /analyze/{candidate_id}   # Analyze candidate
GET /semantic-status          # Semantic engine status
POST /v1/match/candidates     # Advanced matching
POST /v1/match/semantic       # Semantic matching
POST /v1/match/advanced       # ML-powered matching
```

### Analytics
```
GET /v1/analytics/performance # Performance analytics
GET /v1/analytics/metrics     # Detailed metrics
```

### Model Management
```
GET /v1/models/status         # Model status
POST /v1/models/reload        # Reload models
GET /v1/config                # Configuration
POST /v1/config/update        # Update config
```

## Request/Response Examples

### Create Candidate
```bash
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/candidates \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "skills": "Python, FastAPI, PostgreSQL",
    "experience_years": 5
  }'
```

### AI Matching
```bash
curl -X POST https://bhiv-hr-agent-m1me.onrender.com/match \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}'
```

### Health Check
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health/detailed
```

## Response Formats

### Standard Success Response
```json
{
  "status": "success",
  "data": {...},
  "timestamp": "2025-01-01T00:00:00Z",
  "request_id": "req_12345678"
}
```

### Error Response
```json
{
  "status": "error",
  "error": "Validation Error",
  "message": "Request validation failed",
  "details": [...],
  "timestamp": "2025-01-01T00:00:00Z",
  "request_id": "req_12345678"
}
```

### Health Response
```json
{
  "status": "healthy",
  "service": "BHIV HR Gateway",
  "version": "4.0.0",
  "timestamp": "2025-01-01T00:00:00Z",
  "dependencies": {
    "database": {"status": "healthy"},
    "ai_agent": {"status": "healthy"}
  }
}
```

## Rate Limits

- **API Endpoints**: 100 requests/minute
- **Form Submissions**: 10 requests/minute
- **Health Checks**: Unlimited

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Internal Server Error
- `503` - Service Unavailable

## WebSocket Endpoints

### Real-time Updates
```
ws://bhiv-hr-gateway-46pz.onrender.com/ws/updates
```

## SDK Examples

### Python SDK
```python
import requests

class BHIVClient:
    def __init__(self, api_key):
        self.base_url = "https://bhiv-hr-gateway-46pz.onrender.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_candidates(self):
        response = requests.get(f"{self.base_url}/candidates", headers=self.headers)
        return response.json()
```

### JavaScript SDK
```javascript
class BHIVClient {
  constructor(apiKey) {
    this.baseURL = 'https://bhiv-hr-gateway-46pz.onrender.com';
    this.headers = { 'Authorization': `Bearer ${apiKey}` };
  }
  
  async getCandidates() {
    const response = await fetch(`${this.baseURL}/candidates`, { headers: this.headers });
    return response.json();
  }
}
```

## Testing

### Postman Collection
Import the collection from: `/docs/api/postman/BHIV_HR_Platform.postman_collection.json`

### cURL Examples
See individual endpoint documentation for complete cURL examples.

---

**Last Updated**: January 2025  
**API Version**: v4.0.0  
**Documentation Version**: 1.0.0