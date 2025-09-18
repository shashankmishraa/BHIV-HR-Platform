# 🚨 URGENT: Update Render Environment Variables

## Issue Identified
All services still have the demo API key in Render dashboard:
```
API_KEY_SECRET=myverysecureapikey123  ❌ DEMO KEY
```

## Required Fix
Update API_KEY_SECRET to production value for ALL services:

### 1. Agent Service (srv-d2s0dp3e5dus73cl3a20)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### 2. Gateway Service (srv-d2s0a6mmcj7s73fn3iqg)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### 3. Client Portal Service (srv-d2s67pffte5s739kp99g)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### 4. HR Portal Service (srv-d2s5vtje5dus73cr0s90)
```
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

## Steps to Fix
1. Go to Render Dashboard
2. For each service, click Settings → Environment
3. Edit API_KEY_SECRET variable
4. Change from `myverysecureapikey123` to `prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o`
5. Save changes
6. Services will auto-redeploy

## This Will Resolve
- CWE-798 hardcoded credentials detection
- Service authentication consistency
- Production security validation
- Demo key rejection errors