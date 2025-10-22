# Candidate Portal Deployment Guide

## ✅ Current Status
- **Live Services**: 5/5 deployed
- **Candidate Portal**: ✅ **LIVE** at https://bhiv-hr-candidate-portal.onrender.com
- **Service ID**: srv-d3se2s63jp1c738mnp7g

## 🚀 Deploy Candidate Portal to Render

### Step 1: Create New Web Service on Render
1. **Login to Render**: https://dashboard.render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect Repository**: Select your GitHub repo
4. **Service Configuration**:
   ```
   Name: bhiv-hr-candidate-portal
   Environment: Python 3
   Region: Oregon (US West)
   Branch: main
   Root Directory: services/candidate_portal
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

### Step 2: Environment Variables (✅ Configured)
```env
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com
API_KEY=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=candidate_jwt_secret_key_2025
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
```

### Step 3: Deploy Service
1. **Click "Create Web Service"**
2. **Wait for Build** (~5-10 minutes)
3. **Get Service URL** (will be something like `bhiv-hr-candidate-portal-xxxx.onrender.com`)

## 🌐 Access Candidate Portal

### ✅ Live Access:
```bash
# Candidate Portal URL:
https://bhiv-hr-candidate-portal.onrender.com

# Test health:
curl https://bhiv-hr-candidate-portal.onrender.com

# Auto-deploy webhook:
https://api.render.com/deploy/srv-d3se2s63jp1c738mnp7g?key=RgSd9ayhCsE
```

### Features Available:
- **Registration**: New candidate signup
- **Login**: Existing candidate authentication  
- **Dashboard**: Personal candidate dashboard
- **Job Search**: Browse and search jobs
- **Applications**: Apply for jobs and track status
- **Profile Management**: Update candidate information

## 🔧 Alternative: Local Development Access

### If you want to test locally while waiting for deployment:
```bash
# Run candidate portal locally
cd services/candidate_portal
pip install -r requirements.txt
streamlit run app.py --server.port 8503

# Access at: http://localhost:8503
```

## 📋 Complete Service List After Deployment

| Service | URL | Status |
|---------|-----|--------|
| **API Gateway** | bhiv-hr-gateway-46pz.onrender.com | ✅ Live |
| **AI Agent** | bhiv-hr-agent-m1me.onrender.com | ✅ Live |
| **HR Portal** | bhiv-hr-portal-cead.onrender.com | ✅ Live |
| **Client Portal** | bhiv-hr-client-portal-5g33.onrender.com | ✅ Live |
| **Candidate Portal** | bhiv-hr-candidate-portal.onrender.com | ✅ Live |

## 🎯 Quick Deploy Steps

1. **Render Dashboard** → **New Web Service**
2. **Root Directory**: `services/candidate_portal`
3. **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. **Add Environment Variables**
5. **Deploy**

**Estimated Time**: 10-15 minutes for complete deployment

---
**Result**: You'll have all 5 services live with candidate portal accessible via web URL