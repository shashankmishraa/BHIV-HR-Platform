# 🔐 Triple Authentication Testing Guide

Complete testing guide for the triple authentication system across all BHIV HR Platform services.

## 🎯 Authentication Overview

The platform supports **3 authentication methods**:

1. **API Key Authentication** - For system/developer access
2. **Client JWT Authentication** - For enterprise clients  
3. **Candidate JWT Authentication** - For job seekers

## 🚀 Testing Production Services

### **Gateway Service (55 Endpoints)**
**Base URL**: `https://bhiv-hr-gateway-46pz.onrender.com`

### **Agent Service (6 Endpoints)**  
**Base URL**: `https://bhiv-hr-agent-m1me.onrender.com`

---

## 🔑 Method 1: API Key Authentication

### **Test Credentials**
```bash
API_KEY="prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
```

### **Gateway Service Testing**

#### **1. Health Check (No Auth Required)**
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health
```

#### **2. API Key Protected Endpoints**
```bash
# Test API Key Authentication
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Test Database Connectivity
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates

# Test Candidate Search
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/search?skills=python&limit=5"

# Test AI Matching
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top

# Test Database Schema
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/database/schema
```

#### **3. Invalid API Key Test**
```bash
# Should return 401 Unauthorized
curl -H "Authorization: Bearer invalid_api_key" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

### **Agent Service Testing**

#### **1. Health Check (No Auth Required)**
```bash
curl https://bhiv-hr-agent-m1me.onrender.com/health
```

#### **2. API Key Protected Endpoints**
```bash
# Test Database Connectivity
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-agent-m1me.onrender.com/test-db

# Test AI Matching
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"job_id": 1}' \
     https://bhiv-hr-agent-m1me.onrender.com/match

# Test Candidate Analysis
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-agent-m1me.onrender.com/analyze/1

# Test Batch Matching
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"job_ids": [1, 2]}' \
     https://bhiv-hr-agent-m1me.onrender.com/batch-match
```

---

## 🏢 Method 2: Client JWT Authentication

### **Step 1: Get Client JWT Token**
```bash
# Login to get JWT token
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login \
     -H "Content-Type: application/json" \
     -d '{
       "client_id": "TECH001",
       "password": "demo123"
     }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Authentication successful",
  "client_id": "TECH001",
  "company_name": "TechCorp Solutions",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### **Step 2: Use Client JWT Token**
```bash
# Replace YOUR_CLIENT_JWT_TOKEN with the access_token from step 1
CLIENT_JWT="YOUR_CLIENT_JWT_TOKEN"

# Test Gateway endpoints with Client JWT
curl -H "Authorization: Bearer $CLIENT_JWT" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

curl -H "Authorization: Bearer $CLIENT_JWT" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates

curl -H "Authorization: Bearer $CLIENT_JWT" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top

# Test Agent endpoints with Client JWT
curl -H "Authorization: Bearer $CLIENT_JWT" \
     https://bhiv-hr-agent-m1me.onrender.com/test-db

curl -H "Authorization: Bearer $CLIENT_JWT" \
     -H "Content-Type: application/json" \
     -d '{"job_id": 1}' \
     https://bhiv-hr-agent-m1me.onrender.com/match
```

### **Step 3: Test Invalid Client JWT**
```bash
# Should return 401 Unauthorized
curl -H "Authorization: Bearer invalid_jwt_token" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

---

## 👤 Method 3: Candidate JWT Authentication

### **Step 1: Register New Candidate**
```bash
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/register \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test Candidate",
       "email": "test.candidate@example.com",
       "password": "SecurePass123!",
       "phone": "+1-555-0123",
       "location": "San Francisco, CA",
       "experience_years": 3,
       "technical_skills": "Python, JavaScript, React",
       "education_level": "Bachelor",
       "seniority_level": "Mid-level"
     }'
```

### **Step 2: Login to Get Candidate JWT**
```bash
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test.candidate@example.com",
       "password": "SecurePass123!"
     }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "candidate": {
    "id": 32,
    "name": "Test Candidate",
    "email": "test.candidate@example.com"
  }
}
```

### **Step 3: Use Candidate JWT Token**
```bash
# Replace YOUR_CANDIDATE_JWT_TOKEN with the token from step 2
CANDIDATE_JWT="YOUR_CANDIDATE_JWT_TOKEN"

# Test Gateway endpoints with Candidate JWT
curl -H "Authorization: Bearer $CANDIDATE_JWT" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Update candidate profile
curl -X PUT https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/profile/32 \
     -H "Authorization: Bearer $CANDIDATE_JWT" \
     -H "Content-Type: application/json" \
     -d '{
       "technical_skills": "Python, JavaScript, React, Node.js",
       "experience_years": 4
     }'

# Apply for a job
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/apply \
     -H "Authorization: Bearer $CANDIDATE_JWT" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 32,
       "job_id": 1,
       "cover_letter": "I am interested in this position..."
     }'

# Get candidate applications
curl -H "Authorization: Bearer $CANDIDATE_JWT" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/applications/32
```

---

## 🖥️ Portal Services Testing

### **HR Portal**
**URL**: `https://bhiv-hr-portal-cead.onrender.com/`

**Testing Steps:**
1. Open HR Portal in browser
2. Portal uses API Key authentication internally
3. Test dashboard functionality
4. Test candidate search and AI matching features

### **Client Portal**
**URL**: `https://bhiv-hr-client-portal-5g33.onrender.com/`

**Testing Steps:**
1. Open Client Portal in browser
2. Login with credentials:
   - **Username**: `TECH001`
   - **Password**: `demo123`
3. Portal generates Client JWT internally
4. Test job posting and candidate review features

### **Candidate Portal**
**URL**: `https://bhiv-hr-candidate-portal.onrender.com/`

**Testing Steps:**
1. Open Candidate Portal in browser
2. Register new account or login with existing credentials
3. Portal generates Candidate JWT internally
4. Test profile management and job application features

---

## 🧪 Local Development Testing

### **Start Local Services**
```bash
# Start all services with Docker Compose
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Verify services are running
curl http://localhost:8000/health    # Gateway
curl http://localhost:9000/health    # Agent
curl http://localhost:8501           # HR Portal
curl http://localhost:8502           # Client Portal
curl http://localhost:8503           # Candidate Portal
```

### **Test Local Authentication**
```bash
# Test API Key on local Gateway
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/v1/jobs

# Test API Key on local Agent
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:9000/test-db

# Test Client Login on local Gateway
curl -X POST http://localhost:8000/v1/client/login \
     -H "Content-Type: application/json" \
     -d '{"client_id": "TECH001", "password": "demo123"}'

# Test Candidate Registration on local Gateway
curl -X POST http://localhost:8000/v1/candidate/register \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Local Test User",
       "email": "local.test@example.com",
       "password": "TestPass123!"
     }'
```

---

## 🔍 Authentication Flow Testing

### **Test Authentication Priority**
The authentication system tries methods in this order:
1. **API Key** (highest priority)
2. **Client JWT** (medium priority)  
3. **Candidate JWT** (lowest priority)

```bash
# Test with API Key (should work)
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Test with Client JWT (should work)
curl -H "Authorization: Bearer YOUR_CLIENT_JWT_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Test with Candidate JWT (should work)
curl -H "Authorization: Bearer YOUR_CANDIDATE_JWT_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Test with no authentication (should fail with 401)
curl https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

### **Test Cross-Service Authentication**
```bash
# Gateway to Agent communication (internal)
# This happens automatically when you call Gateway matching endpoints
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top
```

---

## 📊 Expected Test Results

### **✅ Successful Authentication**
- **Status Code**: `200 OK`
- **Response**: Valid JSON data
- **Headers**: May include rate limit headers

### **❌ Failed Authentication**
- **Status Code**: `401 Unauthorized`
- **Response**: `{"detail": "Invalid authentication"}`

### **🚫 Missing Authentication**
- **Status Code**: `401 Unauthorized`
- **Response**: `{"detail": "Authentication required"}`

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **1. Invalid API Key**
```bash
# Error: {"detail": "Invalid authentication"}
# Solution: Check API key is correct
echo "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
```

#### **2. Expired JWT Token**
```bash
# Error: {"detail": "Invalid authentication"}
# Solution: Get new JWT token by logging in again
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login \
     -H "Content-Type: application/json" \
     -d '{"client_id": "TECH001", "password": "demo123"}'
```

#### **3. Missing Authorization Header**
```bash
# Error: {"detail": "Authentication required"}
# Solution: Add Authorization header
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

#### **4. Service Unavailable**
```bash
# Check service health first
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health
```

---

## 📝 Test Automation Script

Create a test script to automate authentication testing:

```bash
#!/bin/bash
# save as test_auth.sh

API_KEY="prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
GATEWAY_URL="https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL="https://bhiv-hr-agent-m1me.onrender.com"

echo "🔐 Testing Triple Authentication System"
echo "======================================"

# Test 1: API Key Authentication
echo "1. Testing API Key Authentication..."
response=$(curl -s -H "Authorization: Bearer $API_KEY" "$GATEWAY_URL/v1/jobs")
if [[ $response == *"jobs"* ]]; then
    echo "✅ API Key authentication: PASSED"
else
    echo "❌ API Key authentication: FAILED"
fi

# Test 2: Client JWT Authentication
echo "2. Testing Client JWT Authentication..."
jwt_response=$(curl -s -X POST "$GATEWAY_URL/v1/client/login" \
    -H "Content-Type: application/json" \
    -d '{"client_id": "TECH001", "password": "demo123"}')

if [[ $jwt_response == *"access_token"* ]]; then
    echo "✅ Client JWT login: PASSED"
    # Extract token and test endpoint
    token=$(echo $jwt_response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    test_response=$(curl -s -H "Authorization: Bearer $token" "$GATEWAY_URL/v1/jobs")
    if [[ $test_response == *"jobs"* ]]; then
        echo "✅ Client JWT endpoint access: PASSED"
    else
        echo "❌ Client JWT endpoint access: FAILED"
    fi
else
    echo "❌ Client JWT login: FAILED"
fi

# Test 3: Agent Service Authentication
echo "3. Testing Agent Service Authentication..."
agent_response=$(curl -s -H "Authorization: Bearer $API_KEY" "$AGENT_URL/test-db")
if [[ $agent_response == *"success"* ]]; then
    echo "✅ Agent service authentication: PASSED"
else
    echo "❌ Agent service authentication: FAILED"
fi

echo "======================================"
echo "🎯 Authentication testing completed!"
```

**Run the script:**
```bash
chmod +x test_auth.sh
./test_auth.sh
```

---

## 🎯 Summary

The triple authentication system provides:

1. **API Key**: System-level access for developers and internal services
2. **Client JWT**: Enterprise client access with company-specific permissions
3. **Candidate JWT**: Job seeker access with profile and application management

All authentication methods work across both Gateway (55 endpoints) and Agent (6 endpoints) services, with automatic fallback and priority handling.

**Total Testable Endpoints**: 61 (55 Gateway + 6 Agent)
**Authentication Methods**: 3 (API Key, Client JWT, Candidate JWT)
**Portal Services**: 3 (HR, Client, Candidate)

---

*Last Updated: October 23, 2025 | Production Services: ✅ All Operational*