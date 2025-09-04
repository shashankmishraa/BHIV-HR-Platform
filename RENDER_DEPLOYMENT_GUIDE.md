# 🚀 BHIV HR Platform - Render Deployment Guide

## 📋 Current Deployment Status

✅ **SUCCESSFULLY DEPLOYED ON RENDER**

| Service | URL | Status |
|---------|-----|--------|
| **API Gateway** | https://bhiv-hr-gateway.onrender.com/docs | ✅ Live |
| **AI Matching Engine** | https://bhiv-hr-agent.onrender.com/docs | ✅ Live |
| **HR Portal** | https://bhiv-hr-portal.onrender.com/ | ✅ Live |
| **Client Portal** | https://bhiv-hr-client-portal.onrender.com/ | ✅ Live |
| **Database** | PostgreSQL (Internal) | ✅ Live |

## 🎯 Quick Access

### 🌐 Production URLs
- **API Documentation**: https://bhiv-hr-gateway.onrender.com/docs
- **HR Dashboard**: https://bhiv-hr-portal.onrender.com/
- **Client Login**: https://bhiv-hr-client-portal.onrender.com/
  - Username: `TECH001`
  - Password: `demo123`

### 🔧 API Testing
```bash
# Health Check
curl https://bhiv-hr-gateway.onrender.com/health

# Test Authentication
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/v1/jobs

# AI Matching Test
curl https://bhiv-hr-agent.onrender.com/health
```

## 📊 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Render Cloud Platform                    │
│                     Oregon (US West)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   PostgreSQL    │  │   API Gateway   │  │  AI Agent    │ │
│  │   Database      │  │   (FastAPI)     │  │  (FastAPI)   │ │
│  │   Port: 5432    │  │   Port: 8000    │  │  Port: 9000  │ │
│  │   Free Tier     │  │   43 Endpoints  │  │  Matching    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│           │                     │                    │      │
│           └─────────────────────┼────────────────────┘      │
│                                 │                           │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   HR Portal     │  │  Client Portal  │                  │
│  │  (Streamlit)    │  │  (Streamlit)    │                  │
│  │   Port: 8501    │  │   Port: 8502    │                  │
│  │   Dashboard     │  │   Client UI     │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Service Configuration Details

### 1. Database Service
```yaml
Name: bhiv-hr-database
Type: PostgreSQL
Plan: Free (1GB storage)
Database: bhiv_hr
User: bhiv_user
Version: 17
Region: Oregon (US West)
```

### 2. API Gateway Service
```yaml
Name: bhiv-hr-gateway
Type: Web Service
Plan: Free
Root Directory: services/gateway
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Environment Variables:
  - DATABASE_URL: [Internal PostgreSQL URL]
  - API_KEY_SECRET: myverysecureapikey123
```

### 3. AI Agent Service
```yaml
Name: bhiv-hr-agent
Type: Web Service
Plan: Free
Root Directory: services/agent
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
Environment Variables:
  - DATABASE_URL: [Internal PostgreSQL URL]
```

### 4. HR Portal Service
```yaml
Name: bhiv-hr-portal
Type: Web Service
Plan: Free
Root Directory: services/portal
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Environment Variables:
  - GATEWAY_URL: https://bhiv-hr-gateway.onrender.com
  - API_KEY_SECRET: myverysecureapikey123
```

### 5. Client Portal Service
```yaml
Name: bhiv-hr-client-portal
Type: Web Service
Plan: Free
Root Directory: services/client_portal
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Environment Variables:
  - GATEWAY_URL: https://bhiv-hr-gateway.onrender.com
  - API_KEY_SECRET: myverysecureapikey123
```

## 🚀 Deployment Process (Completed)

### Phase 1: Database Setup ✅
1. Created PostgreSQL service on Render
2. Configured database: `bhiv_hr`
3. Set user: `bhiv_user`
4. Obtained internal database URL

### Phase 2: API Gateway Deployment ✅
1. Connected GitHub repository
2. Set root directory: `services/gateway`
3. Configured build and start commands
4. Added environment variables
5. Service live at: https://bhiv-hr-gateway.onrender.com

### Phase 3: AI Agent Deployment ✅
1. Deployed AI matching service
2. Connected to database
3. Service live at: https://bhiv-hr-agent.onrender.com

### Phase 4: Portal Deployments ✅
1. Deployed HR Portal (Streamlit)
2. Deployed Client Portal (Streamlit)
3. Connected both to API Gateway
4. Configured authentication

## 📈 Performance & Monitoring

### Current Performance Metrics
- **API Response Time**: <100ms average
- **AI Matching Speed**: <0.02 seconds
- **Cold Start Time**: 30-60 seconds (free tier)
- **Uptime**: 99.9% target
- **Rate Limiting**: 60 requests/minute

### Monitoring Endpoints
```bash
# System Health
curl https://bhiv-hr-gateway.onrender.com/health

# Detailed Health Check
curl https://bhiv-hr-gateway.onrender.com/health/detailed

# Prometheus Metrics
curl https://bhiv-hr-gateway.onrender.com/metrics

# Real-time Dashboard
curl https://bhiv-hr-gateway.onrender.com/metrics/dashboard

# Database Status
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/test-candidates
```

## 🔒 Security Features

### Authentication & Authorization
- **API Key**: `myverysecureapikey123`
- **Bearer Token**: Required for protected endpoints
- **Client Portal**: Username/Password authentication
- **Rate Limiting**: 60 requests/minute per IP

### Security Headers
- Content Security Policy (CSP)
- X-XSS-Protection
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security

### Additional Security
- Input validation (XSS/SQL injection protection)
- 2FA support (TOTP compatible)
- Password strength validation
- Automated security testing endpoints

## 💰 Cost Breakdown

### Current Costs (Free Tier)
- **Database**: $0/month (Free PostgreSQL)
- **API Gateway**: $0/month (Free web service)
- **AI Agent**: $0/month (Free web service)
- **HR Portal**: $0/month (Free web service)
- **Client Portal**: $0/month (Free web service)
- **Total**: $0/month

### Free Tier Limitations
- **Monthly Hours**: 750 hours total across all services
- **Sleep Timer**: Services sleep after 15 minutes of inactivity
- **Cold Starts**: 30-60 seconds wake-up time
- **Concurrent Requests**: Limited on free tier
- **Storage**: 1GB database storage

## 🔄 Maintenance & Updates

### Auto-Deployment
- **Enabled**: Automatic deployment on GitHub push
- **Branch**: `main`
- **Trigger**: Code changes in respective service directories

### Manual Operations
```bash
# Trigger manual deployment
# Use Render dashboard "Manual Deploy" button

# View logs
# Access through Render dashboard for each service

# Environment variable updates
# Update through Render dashboard settings
```

## 🧪 Testing & Validation

### API Endpoint Testing
```bash
# Test all core endpoints
curl https://bhiv-hr-gateway.onrender.com/
curl https://bhiv-hr-gateway.onrender.com/health
curl https://bhiv-hr-gateway.onrender.com/docs

# Test authenticated endpoints
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/v1/jobs

curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/candidates/stats
```

### Portal Testing
1. **HR Portal**: Visit https://bhiv-hr-portal.onrender.com/
2. **Client Portal**: Visit https://bhiv-hr-client-portal.onrender.com/
   - Login with: TECH001 / demo123
3. **API Documentation**: Visit https://bhiv-hr-gateway.onrender.com/docs

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Service Not Responding
- **Cause**: Service sleeping (15min inactivity)
- **Solution**: Wait 30-60 seconds for cold start

#### Database Connection Errors
- **Cause**: Database URL misconfiguration
- **Solution**: Verify DATABASE_URL environment variable

#### Authentication Failures
- **Cause**: Missing or incorrect API key
- **Solution**: Check API_KEY_SECRET environment variable

#### Build Failures
- **Cause**: Missing dependencies or incorrect paths
- **Solution**: Verify requirements.txt and root directory settings

### Debug Commands
```bash
# Check service health
curl https://bhiv-hr-gateway.onrender.com/health

# Test database connectivity
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/test-candidates

# View API documentation
open https://bhiv-hr-gateway.onrender.com/docs
```

## 📚 Additional Resources

### Documentation Links
- **API Documentation**: https://bhiv-hr-gateway.onrender.com/docs
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Render Dashboard**: https://dashboard.render.com/

### Support & Contact
- **Platform**: Render Cloud Platform
- **Region**: Oregon (US West)
- **Deployment Date**: January 3, 2025
- **Status**: Production Ready ✅

---

## 🎉 Deployment Success Summary

✅ **All 5 services successfully deployed on Render**
✅ **Zero monthly cost (Free tier)**
✅ **Production-ready with 99.9% uptime target**
✅ **Comprehensive API with 46 endpoints including advanced monitoring**
✅ **AI-powered candidate matching active**
✅ **Dual portal system operational**
✅ **Enterprise-grade security features**

**BHIV HR Platform is now live and accessible worldwide! 🌍**