# 🔧 Render Environment Variables Guide

Complete guide for setting up environment variables for each service in Render deployment.

## 📋 Service-Specific Environment Variables

Based on code analysis of all services, here are the required environment variables for each service:

---

## 🚪 Gateway Service (bhiv-hr-gateway)

**Required Variables:**
```bash
# Database Connection
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu

# API Authentication
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# JWT Authentication Secrets
JWT_SECRET=fallback_jwt_secret_key_for_client_auth_2025
CANDIDATE_JWT_SECRET=candidate_jwt_secret_key_2025

# Service Communication
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

**Code References:**
- `services/gateway/app/main.py` lines 287-315 (get_auth function)
- Uses `JWT_SECRET` for client authentication
- Uses `CANDIDATE_JWT_SECRET` for candidate authentication
- Uses `API_KEY_SECRET` for API key validation

---

## 🤖 Agent Service (bhiv-hr-agent)

**Required Variables:**
```bash
# Database Connection
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu

# API Authentication
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# JWT Authentication (Client JWT only)
JWT_SECRET=fallback_jwt_secret_key_for_client_auth_2025
```

**Code References:**
- `services/agent/app.py` lines 50-65 (auth_dependency function)
- Uses `JWT_SECRET` for client JWT validation
- Uses `API_KEY_SECRET` for API key validation
- Does NOT use `CANDIDATE_JWT_SECRET` (only Gateway and Agent support client JWT)

---

## 🖥️ HR Portal Service (bhiv-hr-portal)

**Required Variables:**
```bash
# Gateway Connection
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com

# API Authentication
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# Agent Service Connection
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

**Code References:**
- `services/portal/app.py` lines 8-12 (API_KEY_SECRET usage)
- `services/portal/config.py` (GATEWAY_URL configuration)
- Uses API Key authentication internally to call Gateway

---

## 🏢 Client Portal Service (bhiv-hr-client-portal)

**Required Variables:**
```bash
# Gateway Connection
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com

# API Authentication
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# JWT Authentication (for client login)
JWT_SECRET=fallback_jwt_secret_key_for_client_auth_2025

# Database Connection (for auth service)
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu

# Agent Service Connection
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

**Code References:**
- `services/client_portal/app.py` lines 8-12 (API_KEY_SECRET usage)
- `services/client_portal/config.py` lines 21-22 (JWT_SECRET setup)
- Uses API Key for Gateway calls and JWT for client authentication

---

## 👤 Candidate Portal Service (bhiv-hr-candidate-portal)

**Required Variables:**
```bash
# Gateway Connection
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com

# API Authentication
API_KEY=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# JWT Authentication (for candidate login)
JWT_SECRET=candidate_jwt_secret_key_2025

# Database Connection
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
```

**Code References:**
- `services/candidate_portal/config.py` lines 15-20 (API_KEY usage)
- `services/candidate_portal/config.py` lines 22-26 (JWT_SECRET usage)
- Note: Uses `API_KEY` (not `API_KEY_SECRET`) and `JWT_SECRET` (not `CANDIDATE_JWT_SECRET`)

---

## 📊 Summary by Service

### **Gateway Service (5 variables)**
- `DATABASE_URL` ✅
- `API_KEY_SECRET` ✅
- `JWT_SECRET` ✅
- `CANDIDATE_JWT_SECRET` ✅
- `AGENT_SERVICE_URL` ✅

### **Agent Service (3 variables)**
- `DATABASE_URL` ✅
- `API_KEY_SECRET` ✅
- `JWT_SECRET` ✅

### **HR Portal Service (3 variables)**
- `GATEWAY_URL` ✅
- `API_KEY_SECRET` ✅
- `AGENT_SERVICE_URL` ✅

### **Client Portal Service (5 variables)**
- `GATEWAY_URL` ✅
- `API_KEY_SECRET` ✅
- `JWT_SECRET` ✅
- `DATABASE_URL` ✅
- `AGENT_SERVICE_URL` ✅

### **Candidate Portal Service (4 variables)**
- `GATEWAY_URL` ✅
- `API_KEY` ✅ (Note: different from others)
- `JWT_SECRET` ✅
- `DATABASE_URL` ✅

---

## 🔧 How to Add Variables in Render

### **Step 1: Access Service Settings**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your service (e.g., "bhiv-hr-gateway")
3. Click on **Environment** tab

### **Step 2: Add Variables**
For each service, add the variables listed above:

**Example for Gateway Service:**
```
Key: DATABASE_URL
Value: postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu

Key: API_KEY_SECRET
Value: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

Key: JWT_SECRET
Value: fallback_jwt_secret_key_for_client_auth_2025

Key: CANDIDATE_JWT_SECRET
Value: candidate_jwt_secret_key_2025

Key: AGENT_SERVICE_URL
Value: https://bhiv-hr-agent-m1me.onrender.com
```

### **Step 3: Deploy Changes**
1. Click **Save Changes**
2. Service will automatically redeploy
3. Verify deployment in **Logs** tab

---

## ⚠️ Important Notes

### **Variable Name Differences**
- **Candidate Portal** uses `API_KEY` (not `API_KEY_SECRET`)
- **Candidate Portal** uses `JWT_SECRET` for candidate auth (not `CANDIDATE_JWT_SECRET`)
- **Other services** use `API_KEY_SECRET` consistently

### **JWT Secret Usage**
- **Gateway**: Uses both `JWT_SECRET` (client) and `CANDIDATE_JWT_SECRET` (candidate)
- **Agent**: Uses only `JWT_SECRET` (client JWT)
- **Client Portal**: Uses `JWT_SECRET` for client authentication
- **Candidate Portal**: Uses `JWT_SECRET` for candidate authentication

### **Service URLs**
- All services need to know Gateway URL: `https://bhiv-hr-gateway-46pz.onrender.com`
- Services that do AI matching need Agent URL: `https://bhiv-hr-agent-m1me.onrender.com`

---

## 🧪 Testing After Setup

### **Test Gateway Service**
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health
```

### **Test Agent Service**
```bash
curl https://bhiv-hr-agent-m1me.onrender.com/health
```

### **Test Portal Services**
- **HR Portal**: https://bhiv-hr-portal-cead.onrender.com/
- **Client Portal**: https://bhiv-hr-client-portal-5g33.onrender.com/
- **Candidate Portal**: https://bhiv-hr-candidate-portal.onrender.com/

### **Test Authentication**
```bash
# Test API Key
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Test Client JWT
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login \
     -H "Content-Type: application/json" \
     -d '{"client_id": "TECH001", "password": "demo123"}'
```

---

## 🔄 Current Status

Based on existing deployment, these variables are likely **already set**:
- ✅ `DATABASE_URL` - All services
- ✅ `API_KEY_SECRET` - Gateway, Agent, HR Portal, Client Portal
- ✅ `GATEWAY_URL` - Portal services
- ✅ `AGENT_SERVICE_URL` - Services that need AI matching

**Need to ADD these variables:**
- ❌ `JWT_SECRET` - Gateway, Agent, Client Portal, Candidate Portal
- ❌ `CANDIDATE_JWT_SECRET` - Gateway only
- ❌ `API_KEY` - Candidate Portal only (different from API_KEY_SECRET)

---

## 🎯 Priority Actions

### **High Priority (Required for Authentication)**
1. **Gateway Service**: Add `JWT_SECRET` and `CANDIDATE_JWT_SECRET`
2. **Agent Service**: Add `JWT_SECRET`
3. **Client Portal**: Add `JWT_SECRET`
4. **Candidate Portal**: Add `JWT_SECRET` and `API_KEY`

### **Medium Priority (Service Communication)**
1. Verify `AGENT_SERVICE_URL` is set on all services that need it
2. Verify `GATEWAY_URL` is set on all portal services

### **Low Priority (Already Working)**
1. `DATABASE_URL` - Already set and working
2. `API_KEY_SECRET` - Already set and working

---

*Last Updated: October 23, 2025 | Based on Code Analysis of All Services*