# 🚀 BHIV HR Platform - Deployment Guide

## 📋 Current Status
**Platform**: Render Cloud | **Region**: Oregon (US West) | **Cost**: $0/month | **Status**: 🟢 ALL SERVICES LIVE

## 🌐 Live Production Services
| Service | URL | Status |
|---------|-----|--------|
| **API Gateway** | https://bhiv-hr-gateway.onrender.com/docs | 🟢 Live |
| **AI Agent** | https://bhiv-hr-agent.onrender.com/docs | 🟢 Live |
| **HR Portal** | https://bhiv-hr-portal.onrender.com/ | 🟢 Live |
| **Client Portal** | https://bhiv-hr-client-portal.onrender.com/ | 🟢 Live |

**Demo Access**: Username: `TECH001` | Password: `demo123`

## 🚀 Render Cloud Deployment

### Prerequisites
- GitHub repository: https://github.com/shashankmishraa/BHIV-HR-Platform
- Render account (free tier)

### Step-by-Step Deployment

#### 1. Deploy Database (FIRST)
```yaml
Service Type: PostgreSQL
Name: bhiv-hr-database
Database: bhiv_hr
User: bhiv_user
Plan: Free (1GB)
```

#### 2. Deploy Services
For each service, use these settings:

**API Gateway:**
```yaml
Name: bhiv-hr-gateway
Root Directory: services/gateway
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Environment Variables:
  - DATABASE_URL: [Internal Database URL]
  - API_KEY_SECRET: myverysecureapikey123
```

**AI Agent:**
```yaml
Name: bhiv-hr-agent
Root Directory: services/agent
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
Environment Variables:
  - DATABASE_URL: [Internal Database URL]
```

**HR Portal:**
```yaml
Name: bhiv-hr-portal
Root Directory: services/portal
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Environment Variables:
  - GATEWAY_URL: https://bhiv-hr-gateway.onrender.com
  - API_KEY_SECRET: myverysecureapikey123
```

**Client Portal:**
```yaml
Name: bhiv-hr-client-portal
Root Directory: services/client_portal
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Environment Variables:
  - GATEWAY_URL: https://bhiv-hr-gateway.onrender.com
  - API_KEY_SECRET: myverysecureapikey123
```

### Verification
```bash
# Test services
curl https://bhiv-hr-gateway.onrender.com/health
curl https://bhiv-hr-agent.onrender.com/health

# Test authentication
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/v1/jobs
```

## 🐳 Local Docker Deployment

### Quick Start
```bash
# Clone and start
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform
docker-compose -f docker-compose.production.yml up -d

# Access services
open http://localhost:8501  # HR Portal
open http://localhost:8502  # Client Portal
open http://localhost:8000/docs  # API Docs
```

### Local Ports
- **API Gateway**: http://localhost:8000
- **AI Agent**: http://localhost:9000
- **HR Portal**: http://localhost:8501
- **Client Portal**: http://localhost:8502

## 🔧 Environment Configuration

### Production (.env for Render)
```bash
DATABASE_URL=postgresql://bhiv_user:password@host:5432/bhiv_hr
API_KEY_SECRET=myverysecureapikey123
GATEWAY_URL=https://bhiv-hr-gateway.onrender.com
```

### Local (.env for Docker)
```bash
DATABASE_URL=postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr
API_KEY_SECRET=myverysecureapikey123
GATEWAY_URL=http://gateway:8000
```

## 🏥 Health Monitoring

### Production Health Checks
```bash
curl https://bhiv-hr-gateway.onrender.com/health/detailed
curl https://bhiv-hr-gateway.onrender.com/metrics
```

### Local Health Checks
```bash
docker-compose -f docker-compose.production.yml ps
./scripts/health-check.sh
```

## 🔒 Security & Authentication
- **API Key**: `myverysecureapikey123`
- **Client Login**: TECH001 / demo123
- **Rate Limiting**: 60 requests/minute
- **2FA Support**: TOTP compatible

## 🛠️ Troubleshooting

### Render Issues
- **Service Sleeping**: Wait 30-60s for cold start (free tier)
- **Build Failures**: Check logs in Render dashboard
- **Database Errors**: Verify DATABASE_URL environment variable

### Local Issues
```bash
# Restart services
docker-compose -f docker-compose.production.yml restart

# Check logs
docker-compose -f docker-compose.production.yml logs gateway

# Reset database
docker-compose -f docker-compose.production.yml down -v
docker-compose -f docker-compose.production.yml up -d
```

## 💰 Cost Analysis
**Render Free Tier**: $0/month
- 750 hours/month across all services
- 15min sleep timer after inactivity
- 1GB database storage

## 📈 Performance Metrics
- **API Response**: <100ms
- **AI Matching**: <0.02s
- **Uptime Target**: 99.9%
- **Cold Start**: 30-60s (free tier)

---

**BHIV HR Platform** - Production-ready AI recruiting platform deployed on Render Cloud with zero monthly cost.

*Last Updated: January 2025*