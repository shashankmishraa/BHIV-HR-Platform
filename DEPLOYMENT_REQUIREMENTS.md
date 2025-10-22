# BHIV HR Platform - Complete Deployment Requirements

## 🚀 Render Deployment Setup

### 1. Render Account & Services
```bash
# Required Render Services (5 total)
1. Web Service: API Gateway (bhiv-hr-gateway)
2. Web Service: AI Agent (bhiv-hr-agent) 
3. Web Service: HR Portal (bhiv-hr-portal)
4. Web Service: Client Portal (bhiv-hr-client-portal)
5. PostgreSQL Database (bhiv-hr-database)
```

### 2. Render Environment Variables
```env
# Database Connection
DATABASE_URL=postgresql://username:password@host:port/database

# API Security
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=fallback_jwt_secret_key_for_client_auth_2025
CANDIDATE_JWT_SECRET=candidate_jwt_secret_key_2025

# Service URLs
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-46pz.onrender.com

# Python Configuration
PYTHON_VERSION=3.12.7
```

### 3. Render Service Configuration
```yaml
# render.yaml (for each service)
services:
  - type: web
    name: bhiv-hr-gateway
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    
  - type: web  
    name: bhiv-hr-portal
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    healthCheckPath: /
```

## 🔄 GitHub Actions Setup

### 1. Repository Secrets (GitHub Settings > Secrets)
```bash
# Render Deployment
RENDER_API_KEY=rnd_xxxxxxxxxxxxxxxxxx
RENDER_SERVICE_ID_GATEWAY=srv-xxxxxxxxxxxxxxxxxx
RENDER_SERVICE_ID_AGENT=srv-xxxxxxxxxxxxxxxxxx
RENDER_SERVICE_ID_PORTAL=srv-xxxxxxxxxxxxxxxxxx
RENDER_SERVICE_ID_CLIENT=srv-xxxxxxxxxxxxxxxxxx

# Database Credentials
DATABASE_URL=postgresql://username:password@host:port/database
DB_HOST=dpg-xxxxxxxxxxxxxxxxxx-a.oregon-postgres.render.com
DB_USER=bhiv_user
DB_PASSWORD=3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2
DB_NAME=bhiv_hr_jcuu

# API Keys
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=fallback_jwt_secret_key_for_client_auth_2025
```

### 2. GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST "https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID_GATEWAY }}/deploys" \
            -H "Authorization: Bearer $RENDER_API_KEY"
```

## 🗄️ Database Setup (PostgreSQL on Render)

### 1. Database Creation
```sql
-- Database: bhiv_hr_jcuu
-- User: bhiv_user
-- Host: dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com
-- Port: 5432
-- SSL: Required
```

### 2. Connection Details
```bash
# External Connection (DBeaver/pgAdmin)
Host: dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com
Port: 5432
Database: bhiv_hr_jcuu
Username: bhiv_user
Password: 3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2
SSL Mode: Require

# Internal Connection String
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
```

### 3. DBeaver Configuration
```properties
# Connection Settings
jdbc.url=jdbc:postgresql://dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com:5432/bhiv_hr_jcuu
user.name=bhiv_user
user.password=3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2
ssl.mode=require
ssl.factory=org.postgresql.ssl.DefaultJavaSSLFactory
```

## 📁 Required Files & Structure

### 1. Service Requirements Files
```bash
# services/gateway/requirements.txt
fastapi>=0.104.0,<0.120.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
python-jose[cryptography]>=3.3.0
bcrypt>=4.0.0
pyotp>=2.8.0
qrcode>=7.4.0
httpx>=0.25.0
psutil>=5.9.0

# services/portal/requirements.txt  
streamlit>=1.28.0,<2.0.0
requests>=2.31.0
pandas>=2.0.0
plotly>=5.15.0
```

### 2. Docker Configuration
```dockerfile
# Dockerfile (for each service)
FROM python:3.12.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE $PORT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
```

### 3. Environment Files
```bash
# .env.production
DATABASE_URL=postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=fallback_jwt_secret_key_for_client_auth_2025
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
```

## 🔐 Security Credentials

### 1. API Keys
```bash
# Production API Key
API_KEY=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

# JWT Secrets
CLIENT_JWT=fallback_jwt_secret_key_for_client_auth_2025
CANDIDATE_JWT=candidate_jwt_secret_key_2025

# Demo Credentials
CLIENT_ID=TECH001
CLIENT_PASSWORD=demo123
```

### 2. Database Credentials
```bash
# Production Database
DB_HOST=dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com
DB_PORT=5432
DB_NAME=bhiv_hr_jcuu
DB_USER=bhiv_user
DB_PASS=3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2
```

## 🌐 Service URLs

### 1. Production URLs
```bash
# Live Services
API_GATEWAY=https://bhiv-hr-gateway-46pz.onrender.com
AI_AGENT=https://bhiv-hr-agent-m1me.onrender.com
HR_PORTAL=https://bhiv-hr-portal-cead.onrender.com
CLIENT_PORTAL=https://bhiv-hr-client-portal-5g33.onrender.com

# Health Checks
https://bhiv-hr-gateway-46pz.onrender.com/health
https://bhiv-hr-agent-m1me.onrender.com/health
```

### 2. API Documentation
```bash
# Interactive API Docs
https://bhiv-hr-gateway-46pz.onrender.com/docs
https://bhiv-hr-agent-m1me.onrender.com/docs
```

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] GitHub repository with all code
- [ ] Render account created
- [ ] Database service provisioned
- [ ] Environment variables configured
- [ ] Requirements.txt files updated
- [ ] Health check endpoints implemented

### Render Setup
- [ ] Create 4 web services (Gateway, Agent, HR Portal, Client Portal)
- [ ] Create 1 PostgreSQL database
- [ ] Configure environment variables for each service
- [ ] Set up auto-deploy from GitHub
- [ ] Configure custom domains (optional)

### Database Setup
- [ ] Run schema migration (consolidated_schema.sql)
- [ ] Insert sample data
- [ ] Configure connection pooling
- [ ] Set up backup schedule
- [ ] Test external connections (DBeaver)

### GitHub Actions
- [ ] Add repository secrets
- [ ] Create deployment workflow
- [ ] Test automated deployments
- [ ] Set up branch protection rules

### Testing
- [ ] Health check all services
- [ ] Test API endpoints
- [ ] Verify database connectivity
- [ ] Test authentication flows
- [ ] Performance testing

## 🛠️ Quick Setup Commands

### 1. Clone & Setup
```bash
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform
cp .env.example .env.production
```

### 2. Database Migration
```bash
psql $DATABASE_URL -f services/db/consolidated_schema.sql
```

### 3. Test Deployment
```bash
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health
```

## 📞 Support Information

### Current Status
- **Services**: 5/5 Operational
- **Database**: PostgreSQL 17 on Render
- **Cost**: $0/month (Free tier)
- **Uptime**: 99.9% target

### Monitoring
```bash
# Health Checks
curl https://bhiv-hr-gateway-46pz.onrender.com/metrics
curl https://bhiv-hr-gateway-46pz.onrender.com/health/detailed
```

---
**Last Updated**: October 22, 2025  
**Platform**: Render Cloud (Oregon, US West)  
**Status**: Production Ready ✅