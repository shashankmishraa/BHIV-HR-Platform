# BHIV HR Platform - Deployment Credentials Summary

## 🔐 Production Environment Variables

### Database Configuration
```bash
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
POSTGRES_USER=bhiv_user
POSTGRES_PASSWORD=3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2
POSTGRES_DB=bhiv_hr_jcuu
```

### API Security
```bash
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
```

### Environment Settings
```bash
ENVIRONMENT=production
PYTHON_VERSION=3.12.7
LOG_LEVEL=INFO
```

## 🌐 Production Service URLs

### Live Services
- **Gateway**: https://bhiv-hr-gateway-46pz.onrender.com
- **AI Agent**: https://bhiv-hr-agent-m1me.onrender.com
- **HR Portal**: https://bhiv-hr-portal-cead.onrender.com
- **Client Portal**: https://bhiv-hr-client-portal-5g33.onrender.com

### API Documentation
- **Gateway API**: https://bhiv-hr-gateway-46pz.onrender.com/docs
- **AI Agent API**: https://bhiv-hr-agent-m1me.onrender.com/docs

## 🚀 Deploy Trigger Keys

### Render Deployment Webhooks
```bash
# Gateway Service
curl -X POST https://api.render.com/deploy/srv-d3bfsejuibrs73feao6g?key=W4WZMj1i9g0

# AI Agent Service  
curl -X POST https://api.render.com/deploy/srv-d3bfvbggjchc73fgdop0?key=0IGyxdvF0LA

# HR Portal Service
curl -X POST https://api.render.com/deploy/srv-d3bg3igdl3ps739btv5g?key=LXdmYEdUCTU

# Client Portal Service
curl -X POST https://api.render.com/deploy/srv-d3bg4s56ubrc739n5ps0?key=NZPMJzMGWU0
```

## 🗄️ Database Access

### PSQL Connection
```bash
PGPASSWORD=3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2 psql -h dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com -U bhiv_user bhiv_hr_jcuu
```

### Connection URLs
- **Internal**: `postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a/bhiv_hr_jcuu`
- **External**: `postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu`

## 🔑 Demo Access

### Client Portal Login
```bash
Username: TECH001
Password: demo123
```

### API Testing
```bash
# Health Check
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health

# Authentication Test
curl -X POST https://bhiv-hr-gateway-46pz.onrender.com/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"TECH001","password":"demo123"}'
```

## ✅ Updated Files

### Environment Files
- ✅ `.env.production`
- ✅ `config/production.env`
- ✅ `services/gateway/.env.production`
- ✅ `services/agent/.env.production`
- ✅ `services/portal/.env.production`
- ✅ `services/client_portal/.env.production`

### Configuration Files
- ✅ `docker-compose.production.yml`
- ✅ `services/gateway/app/main.py`
- ✅ `README.md`

### CI/CD Workflows
- ✅ `.github/workflows/unified-pipeline.yml`
- ✅ `.github/workflows/fast-check.yml`

### Documentation
- ✅ `services/gateway/TESTING_GUIDE.md`
- ✅ `DEPLOYMENT_CREDENTIALS.md` (this file)

## 🔒 Security Notes

- All credentials are production-ready
- API keys are properly formatted for Bearer token authentication
- Database credentials use secure password generation
- Service URLs use HTTPS with SSL certificates
- Environment variables are properly scoped for production use

---

**Last Updated**: January 2025  
**Status**: ✅ All credentials updated and verified  
**Environment**: Production on Render Cloud