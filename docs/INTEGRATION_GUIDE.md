# 🔌 BHIV HR Platform - Integration Guide

Comprehensive guide for integrating with the BHIV HR Platform APIs and services.

**⚠️ IMPORTANT**: Current API status shows 30.51% endpoint success rate. Many endpoints require schema fixes before integration.

## 🎯 Integration Overview

### **Available Integration Methods**
- **REST API**: 118 tested endpoints (36 working, 82 failing - schema issues)
- **Webhooks**: Event-driven notifications (planned)
- **SDK Libraries**: Python client library (available)
- **Bulk Import/Export**: CSV and JSON data exchange
- **Third-party Connectors**: ATS and HRIS integrations (planned)

---

## 🚀 Quick Start Integration

### **1. API Authentication Setup**
```python
import requests

# API Configuration
BASE_URL = "https://bhiv-hr-gateway.onrender.com"
API_KEY = "your-api-key-here"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Test connection
response = requests.get(f"{BASE_URL}/health", headers=headers)
print(f"API Status: {response.status_code}")
```

### **2. Basic Operations**
```python
# Create a candidate
candidate_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "skills": ["Python", "React", "PostgreSQL"],
    "experience_years": 5,
    "location": "Remote"
}

response = requests.post(
    f"{BASE_URL}/v1/candidates",
    json=candidate_data,
    headers=headers
)
candidate = response.json()
print(f"Created candidate: {candidate['id']}")

# Create a job
job_data = {
    "title": "Senior Software Engineer",
    "description": "Full-stack development role",
    "required_skills": ["Python", "React", "PostgreSQL"],
    "experience_level": "Senior",
    "location": "Remote",
    "salary_range": "$120,000 - $150,000"
}

response = requests.post(
    f"{BASE_URL}/v1/jobs",
    json=job_data,
    headers=headers
)
job = response.json()
print(f"Created job: {job['id']}")

# Get AI matching results
response = requests.get(
    f"{BASE_URL}/v1/match/{job['id']}/top",
    headers=headers
)
matches = response.json()
print(f"Found {len(matches)} candidate matches")
```

---

## 📚 Python SDK

### **Installation**
```bash
# Install from source (SDK in development)
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform/sdk/python
pip install -e .
```

### **SDK Usage**
```python
from bhiv_hr_sdk import BHIVClient

# Initialize client
client = BHIVClient(
    api_key="your-api-key",
    base_url="https://bhiv-hr-gateway.onrender.com"
)

# Candidate operations
candidates = client.candidates.list()
candidate = client.candidates.create({
    "name": "Jane Smith",
    "email": "jane@example.com",
    "skills": ["Java", "Spring", "MySQL"]
})
client.candidates.update(candidate.id, {"phone": "+1-555-0124"})

# Job operations
jobs = client.jobs.list()
job = client.jobs.create({
    "title": "Backend Developer",
    "required_skills": ["Java", "Spring"]
})

# AI matching
matches = client.matching.get_top_matches(job.id)
batch_matches = client.matching.batch_match(job.id, [c.id for c in candidates])

# Analytics
stats = client.analytics.get_dashboard_data()
trends = client.analytics.get_trends(period="30d")
```

---

## 🔗 REST API Integration

### **Core Endpoints**

#### **Candidate Management**
```python
# List candidates with filtering
params = {
    "skills": "Python,React",
    "experience_min": 3,
    "location": "Remote",
    "page": 1,
    "limit": 20
}
response = requests.get(f"{BASE_URL}/v1/candidates", params=params, headers=headers)

# Search candidates
search_data = {
    "query": "senior python developer",
    "filters": {
        "skills": ["Python", "Django"],
        "experience_range": [3, 8],
        "location_preference": "Remote"
    }
}
response = requests.post(f"{BASE_URL}/v1/candidates/search", json=search_data, headers=headers)

# Bulk candidate operations
bulk_data = {
    "operation": "update",
    "candidates": [
        {"id": "cand_1", "status": "active"},
        {"id": "cand_2", "status": "inactive"}
    ]
}
response = requests.post(f"{BASE_URL}/v1/candidates/bulk", json=bulk_data, headers=headers)
```

#### **Job Management**
```python
# List jobs with filtering
params = {
    "status": "active",
    "location": "Remote",
    "experience_level": "Senior"
}
response = requests.get(f"{BASE_URL}/v1/jobs", params=params, headers=headers)

# Update job
job_updates = {
    "status": "closed",
    "closing_reason": "Position filled"
}
response = requests.put(f"{BASE_URL}/v1/jobs/{job_id}", json=job_updates, headers=headers)

# Job analytics
response = requests.get(f"{BASE_URL}/v1/jobs/stats", headers=headers)
```

#### **AI Matching**
```python
# Get top matches for a job
response = requests.get(f"{BASE_URL}/v1/match/{job_id}/top", headers=headers)

# Batch matching
batch_data = {
    "job_id": job_id,
    "candidate_ids": ["cand_1", "cand_2", "cand_3"],
    "options": {
        "include_explanation": True,
        "threshold": 0.7
    }
}
response = requests.post(f"{BASE_URL}/v1/match/batch", json=batch_data, headers=headers)

# Provide matching feedback
feedback_data = {
    "job_id": job_id,
    "candidate_id": candidate_id,
    "feedback": "good_match",
    "notes": "Strong technical skills, good culture fit"
}
response = requests.post(f"{BASE_URL}/v1/match/feedback", json=feedback_data, headers=headers)
```

---

## 📊 Bulk Data Operations

### **CSV Import/Export**

#### **Candidate Import**
```python
import pandas as pd

# Prepare CSV data
candidates_df = pd.DataFrame([
    {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "skills": "Python,React,Node.js",
        "experience_years": 4,
        "location": "New York"
    },
    {
        "name": "Bob Wilson",
        "email": "bob@example.com", 
        "skills": "Java,Spring,MySQL",
        "experience_years": 6,
        "location": "San Francisco"
    }
])

# Convert to API format
candidates_data = []
for _, row in candidates_df.iterrows():
    candidates_data.append({
        "name": row["name"],
        "email": row["email"],
        "skills": row["skills"].split(","),
        "experience_years": row["experience_years"],
        "location": row["location"]
    })

# Bulk import
import_data = {
    "candidates": candidates_data,
    "options": {
        "skip_duplicates": True,
        "validate_emails": True
    }
}
response = requests.post(f"{BASE_URL}/v1/candidates/import", json=import_data, headers=headers)
```

#### **Data Export**
```python
# Export candidates
export_params = {
    "format": "csv",
    "filters": {
        "status": "active",
        "created_after": "2025-01-01"
    }
}
response = requests.get(f"{BASE_URL}/v1/candidates/export", params=export_params, headers=headers)

# Save to file
with open("candidates_export.csv", "wb") as f:
    f.write(response.content)
```

---

## 🔔 Webhook Integration (Planned)

### **Webhook Configuration**
```python
# Register webhook endpoint
webhook_data = {
    "url": "https://your-app.com/webhooks/bhiv",
    "events": [
        "candidate.created",
        "candidate.updated", 
        "job.created",
        "match.completed",
        "interview.scheduled"
    ],
    "secret": "your-webhook-secret"
}
response = requests.post(f"{BASE_URL}/v1/webhooks", json=webhook_data, headers=headers)
```

### **Webhook Handler Example**
```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhooks/bhiv', methods=['POST'])
def handle_webhook():
    # Verify webhook signature
    signature = request.headers.get('X-BHIV-Signature')
    payload = request.get_data()
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, f"sha256={expected_signature}"):
        return "Invalid signature", 401
    
    # Process webhook event
    event_data = request.json
    event_type = event_data['type']
    
    if event_type == 'candidate.created':
        handle_candidate_created(event_data['data'])
    elif event_type == 'match.completed':
        handle_match_completed(event_data['data'])
    
    return "OK", 200

def handle_candidate_created(candidate_data):
    print(f"New candidate created: {candidate_data['name']}")
    # Add your business logic here

def handle_match_completed(match_data):
    print(f"Matching completed for job: {match_data['job_id']}")
    # Add your business logic here
```

---

## 🏢 ATS/HRIS Integration

### **Common Integration Patterns**

#### **Workday Integration**
```python
class WorkdayIntegration:
    def __init__(self, workday_client, bhiv_client):
        self.workday = workday_client
        self.bhiv = bhiv_client
    
    def sync_candidates(self):
        # Get candidates from Workday
        workday_candidates = self.workday.get_candidates()
        
        for wd_candidate in workday_candidates:
            # Transform to BHIV format
            bhiv_candidate = {
                "name": wd_candidate["name"],
                "email": wd_candidate["email"],
                "external_id": wd_candidate["id"],
                "skills": self.extract_skills(wd_candidate),
                "experience_years": wd_candidate["experience"]
            }
            
            # Create or update in BHIV
            existing = self.bhiv.candidates.find_by_external_id(wd_candidate["id"])
            if existing:
                self.bhiv.candidates.update(existing.id, bhiv_candidate)
            else:
                self.bhiv.candidates.create(bhiv_candidate)
    
    def sync_jobs(self):
        # Similar pattern for job synchronization
        pass
```

#### **BambooHR Integration**
```python
class BambooHRIntegration:
    def __init__(self, bamboo_client, bhiv_client):
        self.bamboo = bamboo_client
        self.bhiv = bhiv_client
    
    def sync_employee_data(self):
        employees = self.bamboo.get_employees()
        
        for employee in employees:
            # Create candidate profile from employee data
            candidate_data = {
                "name": f"{employee['firstName']} {employee['lastName']}",
                "email": employee["workEmail"],
                "department": employee["department"],
                "job_title": employee["jobTitle"],
                "hire_date": employee["hireDate"]
            }
            
            self.bhiv.candidates.create(candidate_data)
```

---

## 📱 Mobile App Integration

### **React Native Example**
```javascript
// BHIV API Client for React Native
class BHIVClient {
    constructor(apiKey, baseUrl = 'https://bhiv-hr-gateway.onrender.com') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        const response = await fetch(url, config);
        return response.json();
    }
    
    // Candidate operations
    async getCandidates(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/v1/candidates?${params}`);
    }
    
    async createCandidate(candidateData) {
        return this.request('/v1/candidates', {
            method: 'POST',
            body: JSON.stringify(candidateData)
        });
    }
    
    // Job operations
    async getJobs(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/v1/jobs?${params}`);
    }
    
    // AI matching
    async getMatches(jobId) {
        return this.request(`/v1/match/${jobId}/top`);
    }
}

// Usage in React Native component
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';

const CandidateList = () => {
    const [candidates, setCandidates] = useState([]);
    const client = new BHIVClient('your-api-key');
    
    useEffect(() => {
        loadCandidates();
    }, []);
    
    const loadCandidates = async () => {
        try {
            const data = await client.getCandidates({ status: 'active' });
            setCandidates(data.candidates);
        } catch (error) {
            console.error('Failed to load candidates:', error);
        }
    };
    
    return (
        <View>
            <FlatList
                data={candidates}
                keyExtractor={item => item.id}
                renderItem={({ item }) => (
                    <View>
                        <Text>{item.name}</Text>
                        <Text>{item.email}</Text>
                    </View>
                )}
            />
        </View>
    );
};
```

---

## 🔧 Advanced Integration Patterns

### **Real-time Data Synchronization**
```python
import asyncio
import websockets

class RealTimeSync:
    def __init__(self, bhiv_client):
        self.bhiv = bhiv_client
        self.sync_queue = asyncio.Queue()
    
    async def start_sync(self):
        # Start background sync process
        await asyncio.gather(
            self.process_sync_queue(),
            self.monitor_changes()
        )
    
    async def process_sync_queue(self):
        while True:
            try:
                sync_item = await self.sync_queue.get()
                await self.process_sync_item(sync_item)
            except Exception as e:
                print(f"Sync error: {e}")
    
    async def monitor_changes(self):
        # Monitor for changes and add to sync queue
        while True:
            changes = await self.detect_changes()
            for change in changes:
                await self.sync_queue.put(change)
            await asyncio.sleep(30)  # Check every 30 seconds
```

### **Error Handling and Retry Logic**
```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

class RobustBHIVClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
    
    @retry_on_failure(max_retries=3)
    def create_candidate(self, candidate_data):
        response = requests.post(
            f"{self.base_url}/v1/candidates",
            json=candidate_data,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json()
```

---

## 📊 Integration Monitoring

### **Health Checks**
```python
class IntegrationMonitor:
    def __init__(self, bhiv_client):
        self.bhiv = bhiv_client
    
    async def check_api_health(self):
        try:
            response = await self.bhiv.get_health()
            return {
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    async def check_integration_status(self):
        checks = {
            "api_health": await self.check_api_health(),
            "authentication": await self.check_authentication(),
            "data_sync": await self.check_data_sync()
        }
        return checks
```

### **Performance Monitoring**
```python
import time
from contextlib import contextmanager

@contextmanager
def monitor_performance(operation_name):
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        print(f"{operation_name} took {duration:.2f} seconds")
        
        # Log to monitoring system
        metrics.record_operation_time(operation_name, duration)

# Usage
with monitor_performance("candidate_creation"):
    candidate = bhiv_client.candidates.create(candidate_data)
```

---

## 🚀 Best Practices

### **API Usage Guidelines**
1. **Rate Limiting**: Respect rate limits (60 requests/minute)
2. **Error Handling**: Implement proper error handling and retries
3. **Authentication**: Secure API key storage and rotation
4. **Data Validation**: Validate data before sending to API
5. **Monitoring**: Monitor integration health and performance

### **Security Considerations**
1. **API Key Security**: Store API keys securely, never in code
2. **HTTPS Only**: Always use HTTPS for API communications
3. **Input Validation**: Validate all input data
4. **Error Messages**: Don't expose sensitive information in errors
5. **Audit Logging**: Log all integration activities

### **Performance Optimization**
1. **Batch Operations**: Use bulk endpoints for multiple operations
2. **Caching**: Cache frequently accessed data
3. **Pagination**: Use pagination for large datasets
4. **Async Operations**: Use async/await for better performance
5. **Connection Pooling**: Reuse HTTP connections

---

## 📚 Integration Examples Repository

### **Available Examples**
- **Python SDK**: Complete Python integration examples
- **REST API**: cURL and HTTP examples
- **Webhook Handlers**: Event processing examples
- **ATS Connectors**: Workday, BambooHR integration samples
- **Mobile Apps**: React Native and Flutter examples

### **Sample Applications**
- **HR Dashboard**: Complete HR management application
- **Candidate Portal**: Self-service candidate application
- **Analytics Dashboard**: Reporting and analytics integration
- **Mobile Recruiter**: Mobile recruiting application

---

**Integration Guide Version**: 1.0  
**Last Updated**: January 17, 2025  
**API Version**: v1  
**SDK Status**: Python SDK available, JavaScript SDK in development  
**Support**: Integration support available via GitHub issues