# Render Environment Variables Fix

## Root Cause
Missing `API_KEY_SECRET` and `JWT_SECRET` in Render dashboard causing 401 errors.

## Fix (2 minutes)
Add these to **each service** in Render dashboard → Environment:

```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
ENVIRONMENT=production
```

## Services to Update
1. bhiv-hr-gateway
2. bhiv-hr-agent  
3. bhiv-hr-portal
4. bhiv-hr-client-portal

## Result
- `/v1/jobs` will work with new API key
- JWT authentication will work properly
- 401 errors will stop