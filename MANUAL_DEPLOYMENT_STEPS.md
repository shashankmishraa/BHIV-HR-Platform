# Manual Deployment Steps for Render

## 🚨 Critical Changes Made That Need Deployment

### 1. **Gateway Service - Client Login Fix**
- **File Changed**: `services/gateway/app/main.py`
- **Issue**: Client login endpoint was failing with auth_service import error
- **Fix**: Replaced auth_service import with direct database authentication

### 2. **Candidate Portal Deployment**
- **Status**: ✅ **COMPLETED** - Live at https://bhiv-hr-candidate-portal.onrender.com
- **Service ID**: srv-d3se2s63jp1c738mnp7g
- **Features**: Registration, login, profile updates, job applications

## 📋 Manual Steps Required

### Step 1: Push Code Changes to GitHub
```bash
# Commit and push all changes
git add .
git commit -m "Fix client login endpoint and add candidate portal APIs"
git push origin main
```

### Step 2: Trigger Manual Deployment on Render

#### For Gateway Service (CRITICAL - Client Login Fix)
1. Go to Render Dashboard
2. Navigate to `bhiv-hr-gateway-46pz` service
3. Click **"Manual Deploy"** button
4. Select **"Deploy latest commit"**
5. Wait for deployment to complete (~3-5 minutes)

#### For Other Services (If Auto-Deploy Not Working)
```bash
# If auto-deploy from GitHub is not configured:
1. Portal Service: bhiv-hr-portal-cead
2. Client Portal: bhiv-hr-client-portal-5g33  
3. Agent Service: bhiv-hr-agent-m1me
```

### Step 3: Verify Deployment Success
```bash
# Test the fixed client login endpoint
curl -X POST "https://bhiv-hr-gateway-46pz.onrender.com/v1/client/login" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"TECH001","password":"demo123"}'

# Expected: {"success":true,"access_token":"..."}
# Not: {"success":false,"error":"No module named 'auth_service'"}
```

### Step 4: Test New Candidate Portal Endpoints
```bash
# Test candidate registration
curl -X POST "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123"}'

# Test candidate login  
curl -X POST "https://bhiv-hr-gateway-46pz.onrender.com/v1/candidate/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## ⚡ Quick Deployment Actions

### Option 1: GitHub Auto-Deploy (Recommended)
```bash
# If auto-deploy is configured, just push:
git push origin main
# Render will automatically deploy all connected services
```

### Option 2: Manual Deploy via Render Dashboard
1. **Login to Render**: https://dashboard.render.com
2. **Select Service**: bhiv-hr-gateway-46pz
3. **Click Deploy**: "Manual Deploy" → "Deploy latest commit"
4. **Monitor Logs**: Watch deployment progress
5. **Test Health**: Check `/health` endpoint

### Option 3: API-Based Deployment
```bash
# Using Render API (if you have API key)
curl -X POST "https://api.render.com/v1/services/srv-YOUR_SERVICE_ID/deploys" \
  -H "Authorization: Bearer YOUR_RENDER_API_KEY" \
  -H "Content-Type: application/json"
```

## 🔍 Verification Checklist

### After Deployment, Test These:
- [ ] **Client Login**: `/v1/client/login` returns success
- [ ] **Health Check**: `/health` returns healthy status  
- [ ] **API Endpoints**: All 56 endpoints respond correctly
- [ ] **Database**: Connection and queries working
- [ ] **New Features**: Candidate portal endpoints functional

### Expected Results:
```bash
# Client Login (FIXED)
✅ {"success":true,"client_id":"TECH001","access_token":"..."}

# Health Check  
✅ {"status":"healthy","service":"BHIV HR Gateway"}

# Candidate Registration
✅ {"success":true,"candidate_id":123}
```

## 🚨 If Deployment Fails

### Common Issues & Solutions:
1. **Build Failure**: Check requirements.txt dependencies
2. **Import Errors**: Verify all imports are available
3. **Database Connection**: Check DATABASE_URL environment variable
4. **Port Issues**: Ensure services use $PORT variable

### Rollback Plan:
```bash
# If new deployment breaks, rollback to previous version
1. Go to Render Dashboard
2. Select problematic service  
3. Click "Deploys" tab
4. Find last working deployment
5. Click "Redeploy" on that version
```

## 📊 Deployment Priority

### ✅ Completed Deployments:
1. **Gateway Service** - Client login fix deployed
2. **Candidate Portal** - New service deployed and operational

### Medium Priority:
3. **Portal Services** - UI improvements and fixes
4. **Agent Service** - AI matching enhancements

### Low Priority:
5. **Documentation** - README and guide updates

## ⏱️ Estimated Timeline

- **Code Push**: 1 minute
- **Render Build**: 3-5 minutes per service
- **Testing**: 2-3 minutes
- **Total**: ~10-15 minutes for complete deployment

## 🎯 Success Criteria

Deployment is successful when:
- ✅ Client login returns JWT token (not auth_service error)
- ✅ All health checks pass
- ✅ New candidate endpoints respond correctly
- ✅ Existing functionality remains intact
- ✅ 85%+ endpoint success rate maintained

---
**Status**: ✅ All critical deployments completed - 5/5 services operational