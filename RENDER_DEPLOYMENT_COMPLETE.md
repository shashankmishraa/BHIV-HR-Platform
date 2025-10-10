# 🚀 Render Deployment Guide - Complete Setup

## 📋 All Services Dockerfile Status

### ✅ **Corrected Dockerfiles**

**Gateway Service** (`services/gateway/Dockerfile`):
```dockerfile
FROM python:3.12.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 --retries 3 -r requirements.txt
COPY app/ ./app/
EXPOSE $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --timeout-keep-alive 30"]
```

**Agent Service** (`services/agent/Dockerfile`):
```dockerfile
FROM python:3.12.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 --retries 3 -r requirements.txt
COPY . .
EXPOSE $PORT
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-9000} --timeout-keep-alive 30"]
```

**HR Portal** (`services/portal/Dockerfile`):
```dockerfile
FROM python:3.12.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 --retries 3 -r requirements.txt
COPY . .
EXPOSE $PORT
CMD ["sh", "-c", "streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false"]
```

**Client Portal** (`services/client_portal/Dockerfile`):
```dockerfile
FROM python:3.12.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 --retries 3 -r requirements.txt
COPY . .
EXPOSE $PORT
CMD ["sh", "-c", "streamlit run app.py --server.port ${PORT:-8502} --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false"]
```

## 🎯 Render Deployment Configuration

### **Service Type**: Web Service
### **Runtime**: Docker
### **Region**: Oregon (US West)

### **Per Service Settings**:

#### **1. Gateway Service**
```
Name: bhiv-hr-gateway
Repository: https://github.com/shashankmishraa/BHIV-HR-Platform
Branch: main
Root Directory: services/gateway
Build Command: (Auto-detected from Dockerfile)
Start Command: (Auto-detected from Dockerfile)
```

#### **2. Agent Service**
```
Name: bhiv-hr-agent
Repository: https://github.com/shashankmishraa/BHIV-HR-Platform
Branch: main
Root Directory: services/agent
Build Command: (Auto-detected from Dockerfile)
Start Command: (Auto-detected from Dockerfile)
```

#### **3. HR Portal**
```
Name: bhiv-hr-portal
Repository: https://github.com/shashankmishraa/BHIV-HR-Platform
Branch: main
Root Directory: services/portal
Build Command: (Auto-detected from Dockerfile)
Start Command: (Auto-detected from Dockerfile)
```

#### **4. Client Portal**
```
Name: bhiv-hr-client-portal
Repository: https://github.com/shashankmishraa/BHIV-HR-Platform
Branch: main
Root Directory: services/client_portal
Build Command: (Auto-detected from Dockerfile)
Start Command: (Auto-detected from Dockerfile)
```

#### **5. Database**
```
Service Type: PostgreSQL
Name: bhiv-hr-database
Version: PostgreSQL 17
Plan: Free ($0/month)
```

## 🔧 Environment Variables

### **All Services Need**:
```
DATABASE_URL=postgresql://username:password@host:port/database
API_KEY_SECRET=your_secret_key_here
CORS_ORIGINS=https://bhiv-hr-portal-cead.onrender.com,https://bhiv-hr-client-portal-5g33.onrender.com
```

### **Service-Specific URLs**:
```
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com
AGENT_URL=https://bhiv-hr-agent-m1me.onrender.com
PORTAL_URL=https://bhiv-hr-portal-cead.onrender.com
CLIENT_PORTAL_URL=https://bhiv-hr-client-portal-5g33.onrender.com
```

## 🚀 Deployment Steps

### **Step 1: Create Database**
1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name: `bhiv-hr-database`
4. Plan: Free
5. Copy connection string

### **Step 2: Deploy Services**
For each service:
1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Configure settings above
4. Add environment variables
5. Deploy

### **Step 3: Verify Deployment**
```bash
# Health checks
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health

# Portal access
open https://bhiv-hr-portal-cead.onrender.com/
open https://bhiv-hr-client-portal-5g33.onrender.com/
```

## 📊 Expected Results

### **Successful Deployment Logs**:
```
==> Building...
==> Successfully built
==> Detected service running on port 10000
==> Available at your primary URL https://service-name.onrender.com
```

### **Service URLs**:
- **Gateway**: https://bhiv-hr-gateway-46pz.onrender.com
- **Agent**: https://bhiv-hr-agent-m1me.onrender.com  
- **HR Portal**: https://bhiv-hr-portal-cead.onrender.com
- **Client Portal**: https://bhiv-hr-client-portal-5g33.onrender.com

## ✅ Status Check

All services should show:
- ✅ Build: Successful
- ✅ Deploy: Live
- ✅ Health: Healthy
- ✅ Port: 10000 (auto-assigned by Render)

---

**Last Updated**: January 2025  
**Status**: All Dockerfiles optimized for Render deployment