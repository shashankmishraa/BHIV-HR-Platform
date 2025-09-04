# 🚨 RENDER DEPLOYMENT FIX - "Merge Main Branch" Error

## Problem
Gateway service failing to deploy on Render with "merge main branch" error.

## Immediate Solutions

### Solution 1: Force Redeploy (Fastest)
1. Go to Render Dashboard → bhiv-hr-gateway service
2. Click "Manual Deploy" → "Deploy latest commit"
3. Wait 2-3 minutes for deployment

### Solution 2: Clear Deploy Cache
1. Render Dashboard → bhiv-hr-gateway → Settings
2. Scroll to "Build & Deploy" section
3. Click "Clear build cache"
4. Trigger new deployment

### Solution 3: Branch Sync Fix
```bash
# If you have local access to the repo
git checkout main
git pull origin main
git push origin main --force-with-lease
```

### Solution 4: Environment Variables Check
Ensure these are set in Render service settings:
```
DATABASE_URL=postgresql://bhiv_user:password@dpg-xxxxx-a:5432/bhiv_hr
API_KEY_SECRET=myverysecureapikey123
PORT=10000
```

### Solution 5: Dockerfile Fix (If needed)
If build fails, check services/gateway/Dockerfile exists and is correct.

## Current Service Status
- **Gateway**: ❌ Deployment Error (merge main branch)
- **Agent**: ✅ Live (https://bhiv-hr-agent.onrender.com)
- **Portal**: ✅ Live (https://bhiv-hr-portal.onrender.com)
- **Client Portal**: ✅ Live (https://bhiv-hr-client-portal.onrender.com)
- **Database**: ✅ Live

## Expected Resolution Time
- Manual redeploy: 2-3 minutes
- Cache clear: 3-5 minutes
- Branch sync: 5-10 minutes

## Verification
After fix, test:
```bash
curl https://bhiv-hr-gateway.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "BHIV HR Gateway",
  "version": "3.1.0"
}
```