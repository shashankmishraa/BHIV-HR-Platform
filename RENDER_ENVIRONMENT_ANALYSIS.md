# BHIV HR Platform - Render Environment Variables Analysis

## Current Issues Identified

### 1. **CRITICAL: Database URL Malformed**
**Issue**: DATABASE_URL contains "mailto:" prefix which is invalid
**Current**: `postgresql://bhiv_user:mailto:mailto:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu`
**Should be**: `postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu`

### 2. **Variable Naming Inconsistency**
**Issue**: JWT_SECRET vs JWT_SECRET_KEY inconsistency
**Current**: Using `JWT_SECRET`
**Should be**: `JWT_SECRET_KEY` (matches codebase)

### 3. **Missing Required Variables**
- Agent service missing `GATEWAY_SERVICE_URL`
- Portal service missing `AGENT_SERVICE_URL` 
- Client Portal service missing `AGENT_SERVICE_URL`

### 4. **Unnecessary Variables**
- `OBSERVABILITY_ENABLED` (not used in codebase)
- `PYTHON_VERSION` (managed by Render)
- `SECRET_KEY` in Gateway (duplicate of API_KEY_SECRET)

## Recommended Render Environment Configuration

### **Agent Service** (bhiv-hr-agent)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
ENVIRONMENT=production
JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
LOG_LEVEL=INFO
GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-46pz.onrender.com
```

### **Gateway Service** (bhiv-hr-gateway)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
ENVIRONMENT=production
JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
LOG_LEVEL=INFO
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

### **Portal Service** (bhiv-hr-portal)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
ENVIRONMENT=production
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com
JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
LOG_LEVEL=INFO
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

### **Client Portal Service** (bhiv-hr-client-portal)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
ENVIRONMENT=production
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com
JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
LOG_LEVEL=INFO
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

## Changes Required by Service

### **Agent Service**
- **MODIFY**: `JWT_SECRET` → `JWT_SECRET_KEY`
- **ADD**: `GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-46pz.onrender.com`
- **REMOVE**: `OBSERVABILITY_ENABLED`, `PYTHON_VERSION`
- **FIX**: Remove "mailto:" from `DATABASE_URL`

### **Gateway Service**
- **MODIFY**: `JWT_SECRET` → `JWT_SECRET_KEY`
- **REMOVE**: `OBSERVABILITY_ENABLED`, `PYTHON_VERSION`, `SECRET_KEY`
- **FIX**: Remove "mailto:" from `DATABASE_URL`

### **Portal Service**
- **MODIFY**: `JWT_SECRET` → `JWT_SECRET_KEY`
- **REMOVE**: `PYTHON_VERSION`

### **Client Portal Service**
- **MODIFY**: `JWT_SECRET` → `JWT_SECRET_KEY`
- **REMOVE**: `PYTHON_VERSION`
- **FIX**: Remove "mailto:" from `DATABASE_URL`

## Files That Need URL Updates

Based on codebase scan, these files contain hardcoded URLs that need updating:

### **Production URLs to Update**
```
Gateway: https://bhiv-hr-gateway-46pz.onrender.com
Agent: https://bhiv-hr-agent-m1me.onrender.com
Portal: https://bhiv-hr-portal-cead.onrender.com
Client Portal: https://bhiv-hr-client-portal-5g33.onrender.com
```

### **Files Requiring Updates**
1. `services/portal/app.py` - Line 12: API_BASE URL
2. `services/client_portal/app.py` - Line 15: API_BASE_URL
3. `config/render-deployment.yml` - All service URLs
4. `README.md` - Live demo URLs
5. `DEPLOYMENT_STATUS.md` - Service URLs
6. `environments/production/.env.template` - Service URLs
7. `docker-compose.production.yml` - Comments with production URLs

## Priority Actions Required

### **IMMEDIATE (Critical)**
1. Fix DATABASE_URL in all services (remove "mailto:")
2. Change JWT_SECRET to JWT_SECRET_KEY in all services

### **HIGH PRIORITY**
1. Add missing GATEWAY_SERVICE_URL to Agent
2. Add missing AGENT_SERVICE_URL to Portal and Client Portal
3. Remove unnecessary variables

### **MEDIUM PRIORITY**
1. Update hardcoded URLs in codebase files
2. Verify all services restart successfully after changes

## Implementation Steps

### **Step 1: Fix Database URL**
In Render Dashboard for each service, update DATABASE_URL:
```
OLD: postgresql://bhiv_user:mailto:mailto:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
NEW: postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
```

### **Step 2: Standardize JWT Variable**
In all services, change:
```
OLD: JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
NEW: JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
```

### **Step 3: Add Missing Variables**
- Agent: Add `GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-46pz.onrender.com`
- Portal: Add `AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com`
- Client Portal: Add `AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com`

### **Step 4: Remove Unnecessary Variables**
Remove from all services:
- `OBSERVABILITY_ENABLED`
- `PYTHON_VERSION`
- `SECRET_KEY` (Gateway only)

## Validation Commands

After making changes, validate with:
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health
curl https://bhiv-hr-portal-cead.onrender.com/
curl https://bhiv-hr-client-portal-5g33.onrender.com/
```

## Expected Results

After implementing these changes:
- All services should restart successfully
- Database connections should work properly
- JWT authentication should function correctly
- Service-to-service communication should be restored
- All health endpoints should return 200 OK