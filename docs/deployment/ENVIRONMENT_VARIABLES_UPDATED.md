# BHIV HR Platform - Environment Variables Configuration
**Updated: January 2025**

## Production Environment Variables

### 1. Gateway Service
**Service URL**: https://bhiv-hr-gateway-901a.onrender.com
**Deploy Hook**: https://api.render.com/deploy/srv-d3744qje5dus7390foq0?key=V6wlJ-fv6EY

```bash
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
DATABASE_URL=postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a/bhiv_hr_nqzb
ENVIRONMENT=production
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
PYTHON_VERSION=3.11.11
```

### 2. Agent Service
**Service URL**: https://bhiv-hr-agent-o6nx.onrender.com
**Deploy Hook**: https://api.render.com/deploy/srv-d3747q3uibrs738n539g?key=cto8n-Ctivw

```bash
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
DATABASE_URL=postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a/bhiv_hr_nqzb
ENVIRONMENT=production
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
PYTHON_VERSION=3.11.11
```

### 3. Portal Service
**Service URL**: https://bhiv-hr-portal-xk2k.onrender.com
**Deploy Hook**: https://api.render.com/deploy/srv-d374emmmcj7s73fdbbb0?key=dTyTmqjQwu4

```bash
AGENT_SERVICE_URL=https://bhiv-hr-agent-o6nx.onrender.com
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
ENVIRONMENT=production
GATEWAY_URL=https://bhiv-hr-gateway-901a.onrender.com
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
PYTHON_VERSION=3.11.11
```

### 4. Client Portal Service
**Service URL**: https://bhiv-hr-client-portal-zdbt.onrender.com
**Deploy Hook**: https://api.render.com/deploy/srv-d374kkre5dus7390tlgg?key=aV7OERRhxS4

```bash
AGENT_SERVICE_URL=https://bhiv-hr-agent-o6nx.onrender.com
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
ENVIRONMENT=production
GATEWAY_URL=https://bhiv-hr-gateway-901a.onrender.com
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
PYTHON_VERSION=3.11.11
DATABASE_URL=postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a/bhiv_hr_nqzb
```

## Database Configuration

### Internal Database URL
```
postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a/bhiv_hr_nqzb
```

### External Database URL
```
postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb
```

### PSQL Command
```bash
render psql dpg-d373qrogjchc73bu9gug-a
```

## Deployment Commands

### Trigger All Services
```bash
# Gateway
curl -X POST https://api.render.com/deploy/srv-d3744qje5dus7390foq0?key=V6wlJ-fv6EY

# Agent
curl -X POST https://api.render.com/deploy/srv-d3747q3uibrs738n539g?key=cto8n-Ctivw

# Portal
curl -X POST https://api.render.com/deploy/srv-d374emmmcj7s73fdbbb0?key=dTyTmqjQwu4

# Client Portal
curl -X POST https://api.render.com/deploy/srv-d374kkre5dus7390tlgg?key=aV7OERRhxS4
```

### Using Deploy Script
```bash
chmod +x scripts/deploy-all-services.sh
./scripts/deploy-all-services.sh
```

## Health Check URLs

```bash
# Gateway Health
curl https://bhiv-hr-gateway-901a.onrender.com/health

# Agent Health
curl https://bhiv-hr-agent-o6nx.onrender.com/health

# Portal (Web Interface)
curl https://bhiv-hr-portal-xk2k.onrender.com/

# Client Portal (Web Interface)
curl https://bhiv-hr-client-portal-zdbt.onrender.com/
```

## API Testing

```bash
# Test with API Key
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/v1/jobs

# Test Health Endpoint
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-901a.onrender.com/health
```

## Security Notes

1. **Never commit these credentials to version control**
2. **Set environment variables directly in Render Dashboard**
3. **Use .env files only for local development**
4. **Rotate credentials regularly for security**

## Local Development

For local development, use the docker-compose.production.yml file which references these credentials through environment variables:

```bash
# Set local environment variables
export DB_PASSWORD=B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J
export API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
export JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA

# Start services
docker-compose -f docker-compose.production.yml up -d
```