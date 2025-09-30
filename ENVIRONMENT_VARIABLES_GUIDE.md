# 🔧 Environment Variables Configuration Guide

## 📋 Complete Environment Variables Setup for Render Deployment

### **🔑 Required Environment Variables by Service**

## 1. **Agent Service** (https://bhiv-hr-agent-m1me.onrender.com)

```bash
# Authentication & Security
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA

# Database Configuration
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu

# Environment Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
PYTHON_VERSION=3.12.7

# Monitoring & Observability
OBSERVABILITY_ENABLED=true
```

## 2. **Gateway Service** (https://bhiv-hr-gateway-46pz.onrender.com)

```bash
# Service URLs
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com

# Authentication & Security
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
SECRET_KEY=prod_secret_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ
PROD_API_KEY=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# Database Configuration
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu

# Environment Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
PYTHON_VERSION=3.12.7

# Monitoring & Observability
OBSERVABILITY_ENABLED=true
```

## 3. **HR Portal Service** (https://bhiv-hr-portal-cead.onrender.com)

```bash
# Service URLs
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com

# Authentication & Security
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA

# Environment Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
PYTHON_VERSION=3.12.7
```

## 4. **Client Portal Service** (https://bhiv-hr-client-portal-5g33.onrender.com)

```bash
# Service URLs
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com

# Authentication & Security
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA

# Environment Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
PYTHON_VERSION=3.12.7
```

## 5. **Database Service** (PostgreSQL)

```bash
# Database URLs
Internal_Database_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a/bhiv_hr_jcuu
External_Database_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
```

---

## 🔍 **Environment Variables Analysis**

### **✅ Correctly Configured Variables**
- `API_KEY_SECRET`: ✅ Consistent across all services
- `JWT_SECRET`: ✅ Properly set for authentication
- `DATABASE_URL`: ✅ Correct external URL format
- `ENVIRONMENT`: ✅ Set to production
- `LOG_LEVEL`: ✅ Appropriate for production
- `PYTHON_VERSION`: ✅ Consistent (3.12.7)
- `GATEWAY_URL`: ✅ Correctly pointing to Gateway service
- `OBSERVABILITY_ENABLED`: ✅ Set for monitoring services

### **⚠️ Variables to Add/Modify**

#### **Agent Service - Missing Variables:**
```bash
# Add these to Agent service environment
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com  # Self-reference for health checks
```

#### **Gateway Service - Redundant Variables:**
```bash
# These can be removed (redundant with API_KEY_SECRET):
SECRET_KEY=prod_secret_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ  # ⚠️ Redundant
PROD_API_KEY=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o  # ⚠️ Redundant
```

#### **Portal Services - Optional Additions:**
```bash
# Optional for enhanced monitoring
OBSERVABILITY_ENABLED=true
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com  # For direct AI calls
```

---

## 🚀 **Updated Service URLs**

### **Production URLs (Current)**
```bash
Agent_URL=https://bhiv-hr-agent-m1me.onrender.com
Gateway_URL=https://bhiv-hr-gateway-46pz.onrender.com
Client_Portal_URL=https://bhiv-hr-client-portal-5g33.onrender.com
HR_Portal_URL=https://bhiv-hr-portal-cead.onrender.com
Database_External_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
Database_Internal_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a/bhiv_hr_jcuu
```

### **Previous URLs (Updated)**
```bash
# Old URLs (replaced)
Agent_URL_OLD=https://bhiv-hr-agent.onrender.com
Gateway_URL_OLD=https://bhiv-hr-gateway.onrender.com
Client_Portal_URL_OLD=https://bhiv-hr-client-portal.onrender.com
HR_Portal_URL_OLD=https://bhiv-hr-portal.onrender.com
```

---

## 🔧 **Implementation Checklist**

### **✅ Completed Updates**
- [x] Updated all service files with new URLs
- [x] Updated README.md with new production URLs
- [x] Updated DEPLOYMENT_STATUS.md with new URLs
- [x] Updated config/.env.render with new URLs
- [x] Updated API key references to production key
- [x] Updated database URL to external format

### **📋 Recommended Actions**

#### **1. Environment Variables Cleanup**
```bash
# Remove redundant variables from Gateway service:
- SECRET_KEY (use API_KEY_SECRET instead)
- PROD_API_KEY (use API_KEY_SECRET instead)
```

#### **2. Add Missing Variables**
```bash
# Add to Agent service:
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com

# Add to Portal services (optional):
OBSERVABILITY_ENABLED=true
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

#### **3. Verify Database Connectivity**
```bash
# Test database connection with external URL:
psql "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
```

---

## 🧪 **Testing & Validation**

### **Health Check Commands**
```bash
# Test all services with new URLs
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health

# Test authenticated endpoints
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Test portal access
curl https://bhiv-hr-portal-cead.onrender.com/
curl https://bhiv-hr-client-portal-5g33.onrender.com/
```

### **Database Connection Test**
```bash
# Test database connectivity
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates
```

---

## 📊 **Security Considerations**

### **✅ Security Best Practices**
- All API keys are production-grade with sufficient entropy
- JWT secrets are unique and secure
- Database credentials use strong passwords
- All communications use HTTPS
- Environment variables are properly scoped per service

### **🔒 Additional Security Recommendations**
1. **Rotate API keys** every 90 days
2. **Monitor access logs** for unusual activity
3. **Enable rate limiting** on all public endpoints
4. **Use secrets management** for sensitive variables
5. **Implement IP whitelisting** for admin endpoints

---

**Last Updated**: January 2025 | **Status**: 🟢 All Environment Variables Configured