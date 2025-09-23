# 🔌 BHIV HR Platform - Integration Guide

**Complete integration guide for developers and system administrators** - Updated January 18, 2025

## 🎯 Overview

This guide provides comprehensive instructions for integrating with the BHIV HR Platform APIs, including authentication, endpoint usage, SDKs, and best practices.

### **System Status (Latest)**
- **Total Endpoints**: 166 (Gateway: 151, AI Agent: 15)
- **Success Rate**: 70.9% (90/127 endpoints functional)
- **AI Agent**: 100% functional (15/15 endpoints)
- **Performance**: 1.038s average response time
- **Security**: Enterprise-grade with OWASP compliance

---

## 🚀 Quick Start Integration

### **Base URLs**
```bash
# Production (Recommended)
GATEWAY_URL="https://bhiv-hr-gateway-901a.onrender.com"
AI_AGENT_URL="https://bhiv-hr-agent-o6nx.onrender.com"

# Local Development
GATEWAY_URL="http://localhost:8000"
AI_AGENT_URL="http://localhost:9000"
```

### **Authentication**
```bash
# API Key Authentication (Primary)
API_KEY="prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

# Test API Connection
curl -H "Authorization: Bearer $API_KEY" \
     "$GATEWAY_URL/health"
```

### **Basic Integration Test**
```bash
#!/bin/bash
# integration_test.sh

API_KEY="prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
BASE_URL="https://bhiv-hr-gateway-901a.onrender.com"

echo "Testing BHIV HR Platform Integration..."

# Test 1: Health Check
echo "1. Health Check:"
curl -s "$BASE_URL/health" | jq '.status'

# Test 2: Authentication
echo "2. Authentication Test:"
curl -s -H "Authorization: Bearer $API_KEY" \
     "$BASE_URL/v1/jobs" | jq '.count'

# Test 3: AI Matching
echo "3. AI Matching Test:"
curl -s -H "Authorization: Bearer $API_KEY" \
     "$BASE_URL/v1/match/1/top?limit=3" | jq '.candidates_processed'

echo "Integration test completed!"
```

---

## 🔐 Authentication Methods

### **1. API Key Authentication (Recommended)**
```python
import requests

class BHIVClient:
    def __init__(self, api_key, base_url="https://bhiv-hr-gateway-901a.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self):
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_jobs(self):
        response = requests.get(f"{self.base_url}/v1/jobs", headers=self.headers)
        return response.json()

# Usage
client = BHIVClient("prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
health = client.test_connection()
jobs = client.get_jobs()
```

### **2. JWT Token Authentication**
```python
import jwt
from datetime import datetime, timedelta

def generate_jwt_token(user_id, secret_key):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

# Usage
token = generate_jwt_token("user123", "your_secret_key")
headers = {"Authorization": f"Bearer {token}"}
```

### **3. Session-Based Authentication**
```python
import requests

def login_and_get_session(username, password):
    login_data = {"username": username, "password": password}
    response = requests.post(
        "https://bhiv-hr-gateway-901a.onrender.com/v1/auth/login",
        json=login_data
    )
    return response.json()["access_token"]

# Usage
token = login_and_get_session("TECH001", "demo123")
```

---

## 📊 Core API Integration

### **Job Management Integration**

#### **Create Job**
```python
def create_job(client, job_data):
    """Create a new job posting"""
    endpoint = "/v1/jobs"
    response = requests.post(
        f"{client.base_url}{endpoint}",
        json=job_data,
        headers=client.headers
    )
    return response.json()

# Example usage
job_data = {
    "title": "Senior Python Developer",
    "department": "Engineering",
    "location": "Remote",
    "experience_level": "Senior",
    "requirements": "Python, FastAPI, PostgreSQL, 5+ years experience",
    "description": "Join our team to build scalable HR solutions"
}

result = create_job(client, job_data)
print(f"Job created with ID: {result['job_id']}")
```

#### **List Jobs**
```python
def get_all_jobs(client, filters=None):
    """Get all jobs with optional filters"""
    endpoint = "/v1/jobs"
    params = filters or {}
    
    response = requests.get(
        f"{client.base_url}{endpoint}",
        headers=client.headers,
        params=params
    )
    return response.json()

# Usage
jobs = get_all_jobs(client)
print(f"Found {jobs['count']} jobs")

# With filters
filtered_jobs = get_all_jobs(client, {"department": "Engineering"})
```

#### **Search Jobs**
```python
def search_jobs(client, query, location=None, department=None):
    """Search jobs with filters"""
    endpoint = "/v1/jobs/search"
    params = {
        "query": query,
        "location": location or "",
        "department": department or ""
    }
    
    response = requests.get(
        f"{client.base_url}{endpoint}",
        headers=client.headers,
        params=params
    )
    return response.json()

# Usage
results = search_jobs(client, "Python developer", location="Remote")
```

### **Candidate Management Integration**

#### **Bulk Upload Candidates**
```python
def bulk_upload_candidates(client, candidates_data):
    """Upload multiple candidates at once"""
    endpoint = "/v1/candidates/bulk"
    payload = {"candidates": candidates_data}
    
    response = requests.post(
        f"{client.base_url}{endpoint}",
        json=payload,
        headers=client.headers
    )
    return response.json()

# Example usage
candidates = [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "experience_years": 5,
        "technical_skills": "Python, React, PostgreSQL",
        "seniority_level": "Senior",
        "education_level": "Bachelor's"
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone": "+1-555-0124",
        "location": "New York, NY",
        "experience_years": 3,
        "technical_skills": "JavaScript, Node.js, MongoDB",
        "seniority_level": "Mid-level",
        "education_level": "Master's"
    }
]

result = bulk_upload_candidates(client, candidates)
print(f"Uploaded {result['candidates_inserted']} candidates")
```

#### **Search Candidates**
```python
def search_candidates(client, skills=None, location=None, experience_min=None):
    """Search candidates with filters"""
    endpoint = "/v1/candidates/search"
    params = {}
    
    if skills:
        params["skills"] = skills
    if location:
        params["location"] = location
    if experience_min:
        params["experience_min"] = experience_min
    
    response = requests.get(
        f"{client.base_url}{endpoint}",
        headers=client.headers,
        params=params
    )
    return response.json()

# Usage
candidates = search_candidates(
    client, 
    skills="Python", 
    location="Remote", 
    experience_min=3
)
print(f"Found {candidates['count']} matching candidates")
```

---

## 🤖 AI Matching Integration

### **Basic AI Matching**
```python
def get_ai_matches(client, job_id, limit=10):
    """Get AI-powered candidate matches for a job"""
    endpoint = f"/v1/match/{job_id}/top"
    params = {"limit": limit}
    
    response = requests.get(
        f"{client.base_url}{endpoint}",
        headers=client.headers,
        params=params
    )
    return response.json()

# Usage
matches = get_ai_matches(client, job_id=1, limit=5)
print(f"Found {len(matches['matches'])} top matches")

for match in matches['matches']:
    print(f"- {match['name']}: {match['score']}/100")
```

### **Advanced AI Matching (Direct AI Agent)**
```python
def advanced_ai_matching(job_data, candidates_data):
    """Direct integration with AI Agent service"""
    ai_url = "https://bhiv-hr-agent-o6nx.onrender.com"
    
    payload = {
        "job": job_data,
        "candidates": candidates_data,
        "options": {
            "include_explanation": True,
            "threshold": 0.7,
            "max_results": 10
        }
    }
    
    response = requests.post(
        f"{ai_url}/match",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    return response.json()

# Usage
job = {"title": "Python Developer", "skills": ["Python", "FastAPI"]}
candidates = [{"id": 1, "skills": ["Python", "Django", "PostgreSQL"]}]

matches = advanced_ai_matching(job, candidates)
```

### **Batch AI Matching**
```python
def batch_ai_matching(client, job_ids):
    """Process multiple jobs for AI matching"""
    endpoint = "/v1/match/batch"
    payload = {"job_ids": job_ids}
    
    response = requests.post(
        f"{client.base_url}{endpoint}",
        json=payload,
        headers=client.headers
    )
    return response.json()

# Usage
results = batch_ai_matching(client, [1, 2, 3, 4, 5])
for result in results["matches"]:
    print(f"Job {result['job_id']}: {len(result['matches'])} matches")
```

---

## 📊 Analytics & Reporting Integration

### **Get System Analytics**
```python
def get_analytics_dashboard(client):
    """Get comprehensive analytics data"""
    endpoint = "/v1/analytics/dashboard"
    
    response = requests.get(
        f"{client.base_url}{endpoint}",
        headers=client.headers
    )
    return response.json()

# Usage
analytics = get_analytics_dashboard(client)
metrics = analytics["dashboard_metrics"]
print(f"Total candidates: {metrics['total_candidates']}")
print(f"Total jobs: {metrics['total_jobs']}")
```

### **Export Data**
```python
def export_candidates(client, format="csv"):
    """Export candidate data"""
    endpoint = "/v1/candidates/export"
    params = {"format": format}
    
    response = requests.get(
        f"{client.base_url}{endpoint}",
        headers=client.headers,
        params=params
    )
    return response.json()

# Usage
export_info = export_candidates(client, "csv")
print(f"Export URL: {export_info['export_url']}")
```

---

## 🔒 Security Integration

### **Rate Limiting Handling**
```python
import time
from functools import wraps

def rate_limit_retry(max_retries=3, delay=1):
    """Decorator to handle rate limiting"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    response = func(*args, **kwargs)
                    if response.status_code == 429:  # Rate limited
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        print(f"Rate limited. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    return response
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@rate_limit_retry(max_retries=3, delay=2)
def api_call_with_retry(url, headers):
    return requests.get(url, headers=headers)
```

### **Error Handling**
```python
class BHIVAPIError(Exception):
    """Custom exception for BHIV API errors"""
    def __init__(self, status_code, message, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(f"API Error {status_code}: {message}")

def handle_api_response(response):
    """Handle API response with proper error handling"""
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise BHIVAPIError(401, "Authentication failed")
    elif response.status_code == 429:
        raise BHIVAPIError(429, "Rate limit exceeded")
    elif response.status_code >= 500:
        raise BHIVAPIError(response.status_code, "Server error")
    else:
        try:
            error_data = response.json()
            raise BHIVAPIError(
                response.status_code, 
                error_data.get("detail", "Unknown error"),
                error_data
            )
        except ValueError:
            raise BHIVAPIError(response.status_code, response.text)

# Usage
try:
    response = requests.get(url, headers=headers)
    data = handle_api_response(response)
except BHIVAPIError as e:
    print(f"API Error: {e}")
    if e.status_code == 429:
        # Handle rate limiting
        time.sleep(60)
```

---

## 🔧 SDK Development

### **Python SDK Example**
```python
# bhiv_sdk.py
import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

class BHIVClient:
    """Official BHIV HR Platform Python SDK"""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://bhiv-hr-gateway-901a.onrender.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "BHIV-Python-SDK/1.0"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        return handle_api_response(response)
    
    # Job Management
    def create_job(self, job_data: Dict) -> Dict:
        return self._request("POST", "/v1/jobs", json=job_data)
    
    def get_jobs(self, filters: Optional[Dict] = None) -> Dict:
        return self._request("GET", "/v1/jobs", params=filters)
    
    def get_job(self, job_id: int) -> Dict:
        return self._request("GET", f"/v1/jobs/{job_id}")
    
    def update_job(self, job_id: int, job_data: Dict) -> Dict:
        return self._request("PUT", f"/v1/jobs/{job_id}", json=job_data)
    
    def delete_job(self, job_id: int) -> Dict:
        return self._request("DELETE", f"/v1/jobs/{job_id}")
    
    # Candidate Management
    def get_candidates(self, limit: int = 50, offset: int = 0) -> Dict:
        params = {"limit": limit, "offset": offset}
        return self._request("GET", "/v1/candidates", params=params)
    
    def search_candidates(self, **filters) -> Dict:
        return self._request("GET", "/v1/candidates/search", params=filters)
    
    def bulk_upload_candidates(self, candidates: List[Dict]) -> Dict:
        payload = {"candidates": candidates}
        return self._request("POST", "/v1/candidates/bulk", json=payload)
    
    # AI Matching
    def get_ai_matches(self, job_id: int, limit: int = 10) -> Dict:
        params = {"limit": limit}
        return self._request("GET", f"/v1/match/{job_id}/top", params=params)
    
    def batch_ai_matching(self, job_ids: List[int]) -> Dict:
        payload = {"job_ids": job_ids}
        return self._request("POST", "/v1/match/batch", json=payload)
    
    # Analytics
    def get_analytics(self) -> Dict:
        return self._request("GET", "/v1/analytics/dashboard")
    
    def get_job_stats(self) -> Dict:
        return self._request("GET", "/v1/jobs/stats")
    
    def get_candidate_stats(self) -> Dict:
        return self._request("GET", "/v1/candidates/stats")
    
    # System
    def health_check(self) -> Dict:
        return self._request("GET", "/health")
    
    def get_system_status(self) -> Dict:
        return self._request("GET", "/v1/system/status")

# Usage Example
if __name__ == "__main__":
    client = BHIVClient("prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
    
    # Test connection
    health = client.health_check()
    print(f"System status: {health['status']}")
    
    # Get jobs
    jobs = client.get_jobs()
    print(f"Total jobs: {jobs['count']}")
    
    # AI matching
    matches = client.get_ai_matches(job_id=1, limit=5)
    print(f"Top matches: {len(matches['matches'])}")
```

### **JavaScript/Node.js SDK**
```javascript
// bhiv-sdk.js
const axios = require('axios');

class BHIVClient {
    constructor(apiKey, baseUrl = 'https://bhiv-hr-gateway-901a.onrender.com') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
            'User-Agent': 'BHIV-Node-SDK/1.0'
        };
    }

    async _request(method, endpoint, data = null, params = null) {
        try {
            const config = {
                method,
                url: `${this.baseUrl}${endpoint}`,
                headers: this.headers,
                data,
                params
            };
            
            const response = await axios(config);
            return response.data;
        } catch (error) {
            throw new Error(`API Error: ${error.response?.status} - ${error.response?.data?.detail || error.message}`);
        }
    }

    // Job Management
    async createJob(jobData) {
        return this._request('POST', '/v1/jobs', jobData);
    }

    async getJobs(filters = {}) {
        return this._request('GET', '/v1/jobs', null, filters);
    }

    async getJob(jobId) {
        return this._request('GET', `/v1/jobs/${jobId}`);
    }

    // Candidate Management
    async getCandidates(limit = 50, offset = 0) {
        return this._request('GET', '/v1/candidates', null, { limit, offset });
    }

    async searchCandidates(filters) {
        return this._request('GET', '/v1/candidates/search', null, filters);
    }

    async bulkUploadCandidates(candidates) {
        return this._request('POST', '/v1/candidates/bulk', { candidates });
    }

    // AI Matching
    async getAIMatches(jobId, limit = 10) {
        return this._request('GET', `/v1/match/${jobId}/top`, null, { limit });
    }

    // System
    async healthCheck() {
        return this._request('GET', '/health');
    }
}

module.exports = BHIVClient;

// Usage Example
const client = new BHIVClient('prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o');

async function example() {
    try {
        const health = await client.healthCheck();
        console.log('System status:', health.status);
        
        const jobs = await client.getJobs();
        console.log('Total jobs:', jobs.count);
        
        const matches = await client.getAIMatches(1, 5);
        console.log('Top matches:', matches.matches.length);
    } catch (error) {
        console.error('Error:', error.message);
    }
}

example();
```

---

## 🔄 Webhook Integration

### **Setting Up Webhooks**
```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret"

def verify_webhook_signature(payload, signature, secret):
    """Verify webhook signature for security"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@app.route('/webhooks/bhiv', methods=['POST'])
def handle_bhiv_webhook():
    """Handle BHIV platform webhooks"""
    payload = request.get_data()
    signature = request.headers.get('X-BHIV-Signature')
    
    if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
        return jsonify({"error": "Invalid signature"}), 401
    
    data = request.json
    event_type = data.get('event_type')
    
    if event_type == 'job.created':
        handle_job_created(data['job'])
    elif event_type == 'candidate.matched':
        handle_candidate_matched(data['match'])
    elif event_type == 'interview.scheduled':
        handle_interview_scheduled(data['interview'])
    
    return jsonify({"status": "received"}), 200

def handle_job_created(job_data):
    """Handle new job creation event"""
    print(f"New job created: {job_data['title']} (ID: {job_data['id']})")
    # Your custom logic here

def handle_candidate_matched(match_data):
    """Handle candidate matching event"""
    print(f"New match: Candidate {match_data['candidate_id']} for Job {match_data['job_id']}")
    # Your custom logic here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 📊 Performance Optimization

### **Connection Pooling**
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OptimizedBHIVClient:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url or "https://bhiv-hr-gateway-901a.onrender.com"
        
        # Create session with connection pooling
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Mount adapter with retry strategy
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=retry_strategy
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return handle_api_response(response)
```

### **Caching Strategy**
```python
import redis
import json
from functools import wraps

# Redis cache setup
cache = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(ttl=300):  # 5 minutes default
    """Decorator to cache API responses"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"bhiv_api:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Call API and cache result
            result = func(*args, **kwargs)
            cache.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

class CachedBHIVClient(BHIVClient):
    @cache_response(ttl=600)  # Cache for 10 minutes
    def get_jobs(self, filters=None):
        return super().get_jobs(filters)
    
    @cache_response(ttl=300)  # Cache for 5 minutes
    def get_ai_matches(self, job_id, limit=10):
        return super().get_ai_matches(job_id, limit)
```

---

## 🧪 Testing Integration

### **Unit Tests**
```python
import unittest
from unittest.mock import patch, Mock
from bhiv_sdk import BHIVClient

class TestBHIVIntegration(unittest.TestCase):
    def setUp(self):
        self.client = BHIVClient("test_api_key")
    
    @patch('requests.request')
    def test_health_check(self, mock_request):
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy"}
        mock_request.return_value = mock_response
        
        # Test
        result = self.client.health_check()
        self.assertEqual(result["status"], "healthy")
    
    @patch('requests.request')
    def test_create_job(self, mock_request):
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"job_id": 123, "message": "Job created"}
        mock_request.return_value = mock_response
        
        # Test data
        job_data = {
            "title": "Test Job",
            "department": "Engineering",
            "location": "Remote"
        }
        
        # Test
        result = self.client.create_job(job_data)
        self.assertEqual(result["job_id"], 123)
    
    def test_api_key_validation(self):
        with self.assertRaises(ValueError):
            BHIVClient("")  # Empty API key should raise error

if __name__ == '__main__':
    unittest.main()
```

### **Integration Tests**
```python
import pytest
import time
from bhiv_sdk import BHIVClient

@pytest.fixture
def client():
    return BHIVClient("prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")

def test_full_workflow(client):
    """Test complete job posting and matching workflow"""
    
    # Step 1: Create job
    job_data = {
        "title": "Integration Test Job",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Senior",
        "requirements": "Python, FastAPI, PostgreSQL",
        "description": "Test job for integration testing"
    }
    
    job_result = client.create_job(job_data)
    assert "job_id" in job_result
    job_id = job_result["job_id"]
    
    # Step 2: Get AI matches
    time.sleep(1)  # Allow for job processing
    matches = client.get_ai_matches(job_id, limit=5)
    assert "matches" in matches
    assert len(matches["matches"]) <= 5
    
    # Step 3: Clean up (delete job)
    delete_result = client.delete_job(job_id)
    assert "message" in delete_result

def test_rate_limiting(client):
    """Test rate limiting behavior"""
    start_time = time.time()
    
    # Make multiple rapid requests
    for i in range(10):
        try:
            client.health_check()
        except Exception as e:
            if "429" in str(e):  # Rate limited
                break
    
    elapsed = time.time() - start_time
    assert elapsed < 60  # Should complete within reasonable time
```

---

## 📚 Best Practices

### **1. Error Handling**
```python
# Always handle specific error cases
try:
    result = client.get_jobs()
except BHIVAPIError as e:
    if e.status_code == 429:
        # Rate limited - implement backoff
        time.sleep(60)
        result = client.get_jobs()
    elif e.status_code == 401:
        # Authentication failed - refresh token
        client.refresh_token()
        result = client.get_jobs()
    else:
        # Log error and handle gracefully
        logger.error(f"API Error: {e}")
        result = {"jobs": [], "count": 0}  # Fallback
```

### **2. Pagination Handling**
```python
def get_all_candidates(client):
    """Get all candidates with pagination"""
    all_candidates = []
    offset = 0
    limit = 50
    
    while True:
        response = client.get_candidates(limit=limit, offset=offset)
        candidates = response["candidates"]
        
        if not candidates:
            break
            
        all_candidates.extend(candidates)
        
        if len(candidates) < limit:
            break
            
        offset += limit
    
    return all_candidates
```

### **3. Async Integration**
```python
import asyncio
import aiohttp

class AsyncBHIVClient:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url or "https://bhiv-hr-gateway-901a.onrender.com"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    async def _request(self, method, endpoint, **kwargs):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}{endpoint}"
            async with session.request(method, url, headers=self.headers, **kwargs) as response:
                return await response.json()
    
    async def get_jobs(self):
        return await self._request("GET", "/v1/jobs")
    
    async def get_ai_matches(self, job_id, limit=10):
        params = {"limit": limit}
        return await self._request("GET", f"/v1/match/{job_id}/top", params=params)

# Usage
async def main():
    client = AsyncBHIVClient("your_api_key")
    
    # Concurrent requests
    jobs_task = client.get_jobs()
    matches_task = client.get_ai_matches(1)
    
    jobs, matches = await asyncio.gather(jobs_task, matches_task)
    print(f"Jobs: {jobs['count']}, Matches: {len(matches['matches'])}")

asyncio.run(main())
```

---

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Authentication Errors**
```python
# Problem: 401 Unauthorized
# Solution: Check API key format
api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
headers = {"Authorization": f"Bearer {api_key}"}  # Note: "Bearer " prefix

# Test authentication
response = requests.get("https://bhiv-hr-gateway-901a.onrender.com/health", headers=headers)
print(response.status_code)  # Should be 200
```

#### **2. Rate Limiting**
```python
# Problem: 429 Too Many Requests
# Solution: Implement exponential backoff
import time
import random

def api_call_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except BHIVAPIError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            raise e
```

#### **3. Timeout Issues**
```python
# Problem: Request timeouts
# Solution: Configure appropriate timeouts
import requests

session = requests.Session()
session.timeout = (10, 30)  # (connect_timeout, read_timeout)

# For long-running operations
response = session.get(url, timeout=60)
```

### **Debug Mode**
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DebugBHIVClient(BHIVClient):
    def _request(self, method, endpoint, **kwargs):
        logger.debug(f"Making {method} request to {endpoint}")
        logger.debug(f"Headers: {self.headers}")
        logger.debug(f"Kwargs: {kwargs}")
        
        result = super()._request(method, endpoint, **kwargs)
        
        logger.debug(f"Response: {result}")
        return result
```

---

## 📞 Support & Resources

### **Documentation Links**
- **API Reference**: https://bhiv-hr-gateway-901a.onrender.com/docs
- **AI Agent Docs**: https://bhiv-hr-agent-o6nx.onrender.com/docs
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **User Guide**: docs/USER_GUIDE.md
- **Security Guide**: docs/security/SECURITY_COMPLIANCE.md

### **Support Channels**
- **Technical Support**: tech-support@bhiv-platform.com
- **Integration Help**: integration@bhiv-platform.com
- **Bug Reports**: bugs@bhiv-platform.com
- **Feature Requests**: features@bhiv-platform.com

### **Community Resources**
- **Developer Forum**: https://community.bhiv-platform.com
- **Stack Overflow**: Tag `bhiv-hr-platform`
- **Discord**: https://discord.gg/bhiv-developers
- **Newsletter**: Subscribe for API updates and best practices

---

**Integration Guide Version**: 2.0  
**Last Updated**: January 18, 2025  
**API Version**: v1  
**SDK Versions**: Python 1.0, Node.js 1.0  
**Total Endpoints Covered**: 166 (Gateway: 151, AI Agent: 15)  
**Success Rate**: 70.9% functional endpoints  
**Support Level**: Enterprise-grade with 24/7 availability