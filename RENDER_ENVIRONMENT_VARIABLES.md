# 🔧 Render Environment Variables Configuration

## 🚨 **CRITICAL: New Environment Variables Required**

Based on the security fixes applied, you **MUST** add these environment variables to your Render services:

## 📋 **Required Environment Variables by Service**

### **🔗 Gateway Service**
```
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
ENVIRONMENT=production
LOG_LEVEL=INFO
OBSERVABILITY_ENABLED=true
PYTHON_VERSION=3.12.7
```

### **🤖 Agent Service**
```
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
ENVIRONMENT=production
LOG_LEVEL=INFO
OBSERVABILITY_ENABLED=true
PYTHON_VERSION=3.12.7
```

### **🏢 HR Portal Service**
```
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
ENVIRONMENT=production
LOG_LEVEL=INFO
PYTHON_VERSION=3.12.7
```

### **👥 Client Portal Service**
```
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
DEFAULT_CLIENT_PASSWORD=SecurePass2024!
ENVIRONMENT=production
LOG_LEVEL=INFO
PYTHON_VERSION=3.12.7
```

## 🆕 **NEW Environment Variables Added**

### **JWT_SECRET** (CRITICAL - NEW)
- **Required by**: All services
- **Purpose**: JWT token signing and validation
- **Value**: `prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA`
- **Impact**: Authentication will fail without this

### **DEFAULT_CLIENT_PASSWORD** (NEW)
- **Required by**: Client Portal only
- **Purpose**: Default client account password
- **Value**: `SecurePass2024!`
- **Impact**: Client registration will fail without this

### **DATABASE_URL** (UPDATED)
- **Required by**: Client Portal (newly added)
- **Purpose**: Direct database access for authentication
- **Value**: Same as Gateway/Agent services
- **Impact**: Client authentication will fail without this

## ⚠️ **DEPLOYMENT WILL FAIL WITHOUT THESE**

The security fixes removed all hardcoded fallback values. Services will now:
1. **Check for required environment variables on startup**
2. **Exit with error if variables are missing**
3. **Log clear error messages about missing variables**

## 🔧 **How to Add in Render Dashboard**

### **For Each Service:**
1. Go to Render Dashboard
2. Select your service (Gateway/Agent/HR Portal/Client Portal)
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add each variable from the list above
6. Click **Save Changes**
7. **Redeploy** the service

### **Critical Order:**
1. **Database Service** - Already configured ✅
2. **Gateway Service** - Add all Gateway variables
3. **Agent Service** - Add all Agent variables  
4. **HR Portal** - Add all HR Portal variables
5. **Client Portal** - Add all Client Portal variables

## 🚨 **Immediate Action Required**

**BEFORE** redeploying any service, you **MUST**:
1. Add **JWT_SECRET** to all services
2. Add **DATABASE_URL** to Client Portal
3. Add **DEFAULT_CLIENT_PASSWORD** to Client Portal
4. Verify all existing variables are still present

## ✅ **Verification Checklist**

After adding environment variables:
- [ ] Gateway service has 7 environment variables
- [ ] Agent service has 7 environment variables  
- [ ] HR Portal has 6 environment variables
- [ ] Client Portal has 8 environment variables
- [ ] All services redeploy successfully
- [ ] Health checks pass for all services
- [ ] Authentication works in Client Portal

## 🎯 **Expected Results**

With proper environment variables:
- ✅ **Security**: No hardcoded credentials
- ✅ **Authentication**: JWT tokens work properly
- ✅ **Database**: Client Portal can authenticate users
- ✅ **Logging**: Structured logging enabled
- ✅ **Monitoring**: Observability features active

**Status**: 🚨 **CRITICAL - MUST ADD BEFORE DEPLOYMENT**