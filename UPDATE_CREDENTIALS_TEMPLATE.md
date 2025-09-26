# 🔄 Render Deployment Credentials Update Template

## Current Configuration (OLD - To be replaced)
```yaml
Services:
- Gateway: https://bhiv-hr-gateway-901a.onrender.com
- AI Agent: https://bhiv-hr-agent-o6nx.onrender.com  
- HR Portal: https://bhiv-hr-portal-xk2k.onrender.com
- Client Portal: https://bhiv-hr-client-portal-zdbt.onrender.com

Database: postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb

API Key: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT Secret: prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
```

## NEW CREDENTIALS NEEDED (Please provide):

### 1. New Service URLs
```
Gateway URL: https://your-new-gateway.onrender.com
AI Agent URL: https://your-new-agent.onrender.com
HR Portal URL: https://your-new-portal.onrender.com
Client Portal URL: https://your-new-client-portal.onrender.com
```

### 2. New Database Connection
```
Database URL: postgresql://user:password@host/database
```

### 3. New Security Credentials
```
API Key: your_new_api_key_here
JWT Secret: your_new_jwt_secret_here
```

### 4. New Deploy Hooks (from Render dashboard)
```
Gateway Deploy Hook: https://api.render.com/deploy/srv-XXXXX?key=XXXXX
Agent Deploy Hook: https://api.render.com/deploy/srv-XXXXX?key=XXXXX
Portal Deploy Hook: https://api.render.com/deploy/srv-XXXXX?key=XXXXX
Client Portal Deploy Hook: https://api.render.com/deploy/srv-XXXXX?key=XXXXX
```

## Files That Will Be Updated:
1. ✅ README.md - Service URLs and demo credentials
2. ✅ config/environments.yml - Production environment URLs
3. ✅ config/render-deployment-config.yml - Deploy hooks and credentials
4. ✅ config/settings.json - Service URLs
5. ✅ .env.example - Template with new URLs
6. ✅ GitHub Secrets (manual update needed)

## Next Steps:
1. Provide the new credentials above
2. I'll update all configuration files
3. Commit and push changes
4. Update GitHub repository secrets
5. Trigger new deployment

---
**Status**: ⏳ Waiting for new credentials