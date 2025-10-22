# BHIV HR Platform - Quick Start Guide

**Get started in 5 minutes** | **Updated**: October 22, 2025 | **Status**: All 5 Services Live ✅

## 🚀 Choose Your Path

### **🌐 Option 1: Use Live Platform (Recommended)**
**No setup required - Start immediately**

| Portal | URL | Credentials | Purpose |
|--------|-----|-------------|---------|
| **HR Portal** | https://bhiv-hr-portal-cead.onrender.com | No login required | Manage candidates and jobs |
| **Client Portal** | https://bhiv-hr-client-portal-5g33.onrender.com | TECH001 / demo123 | Post jobs, review candidates |
| **Candidate Portal** | https://bhiv-hr-candidate-portal.onrender.com | Register new account | Job search and applications |
| **API Gateway** | https://bhiv-hr-gateway-46pz.onrender.com/docs | API Key required | Developer integration |

### **💻 Option 2: Local Development**
**Full control - Run on your machine**

```bash
# Prerequisites: Docker & Docker Compose
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Access locally:
# HR Portal: http://localhost:8501
# Client Portal: http://localhost:8502  
# Candidate Portal: http://localhost:8503
# API Gateway: http://localhost:8000/docs
```

## 🎯 5-Minute Demo Walkthrough

### **Step 1: HR Portal (30 seconds)**
1. Visit: https://bhiv-hr-portal-cead.onrender.com
2. View dashboard with 31 candidates and 19 jobs
3. Try AI matching for any job posting
4. Browse candidate profiles with BHIV values scores

### **Step 2: Client Portal (1 minute)**
1. Visit: https://bhiv-hr-client-portal-5g33.onrender.com
2. Login: `TECH001` / `demo123`
3. Create a new job posting
4. Review matched candidates with AI scores
5. Schedule interviews for top candidates

### **Step 3: Candidate Portal (2 minutes)** ✨ **NEW**
1. Visit: https://bhiv-hr-candidate-portal.onrender.com
2. Register new account with your details
3. Browse available job postings (19 active jobs)
4. Apply for positions that match your skills
5. Track application status in dashboard

### **Step 4: API Integration (1.5 minutes)**
```bash
# Test API with production key
API_KEY="prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

# Get all jobs
curl -H "Authorization: Bearer $API_KEY" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs

# Get AI matches for job ID 1
curl -H "Authorization: Bearer $API_KEY" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top

# Get candidate statistics
curl -H "Authorization: Bearer $API_KEY" \
     https://bhiv-hr-gateway-46pz.onrender.com/candidates/stats
```

## 🔧 Platform Features Overview

### **🤖 AI-Powered Matching**
- **Phase 3 Engine**: Advanced semantic matching with learning capabilities
- **Real-time Processing**: <0.02 second response time
- **Adaptive Scoring**: Company-specific weight optimization
- **Cultural Fit**: BHIV values alignment analysis

### **👥 Multi-User Support**
- **HR Teams**: Internal candidate and job management
- **Client Companies**: External job posting and candidate review
- **Job Seekers**: Registration, search, and application tracking
- **Developers**: 61 REST API endpoints for integration

### **🔒 Enterprise Security**
- **Authentication**: JWT tokens, API keys, 2FA support
- **Rate Limiting**: Dynamic adjustment (60-500 requests/minute)
- **Data Protection**: Encrypted passwords, secure sessions
- **Input Validation**: XSS/SQL injection protection

### **📊 Real-Time Analytics**
- **Live Dashboards**: Performance metrics and insights
- **Candidate Statistics**: Comprehensive reporting
- **Job Market Data**: Trend analysis and success rates
- **System Monitoring**: Health checks and performance tracking

## 🛠️ Development Setup

### **Local Environment Requirements**
```bash
# Required Software
- Docker Desktop
- Git
- Python 3.12.7 (optional, for direct development)

# Optional Tools
- DBeaver (database management)
- Postman (API testing)
- VS Code (code editing)
```

### **Environment Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings (optional - defaults work)
DATABASE_URL=postgresql://...
API_KEY_SECRET=your_api_key
JWT_SECRET=your_jwt_secret
```

### **Service Health Checks**
```bash
# Verify all services are running
curl http://localhost:8000/health    # Gateway
curl http://localhost:9000/health    # AI Agent  
curl http://localhost:8501          # HR Portal
curl http://localhost:8502          # Client Portal
curl http://localhost:8503          # Candidate Portal
```

## 📚 Next Steps

### **For HR Teams**
1. **Explore Dashboard**: Review candidate pipeline and job metrics
2. **Test AI Matching**: Try semantic matching for different job types
3. **Values Assessment**: Use BHIV values scoring system
4. **Batch Operations**: Upload candidate data in bulk

### **For Client Companies**
1. **Job Management**: Create and manage job postings
2. **Candidate Review**: Access AI-matched candidates
3. **Interview Scheduling**: Coordinate with HR teams
4. **Real-time Sync**: See updates across portals instantly

### **For Job Seekers**
1. **Complete Profile**: Add skills, experience, and preferences
2. **Job Search**: Use filters to find relevant positions
3. **Application Tracking**: Monitor status and feedback
4. **Profile Updates**: Keep information current for better matches

### **For Developers**
1. **API Documentation**: Explore https://bhiv-hr-gateway-46pz.onrender.com/docs
2. **Authentication**: Get API key for integration
3. **Webhook Setup**: Configure auto-deploy for updates
4. **Custom Integration**: Build on top of 61 available endpoints

## 🔍 Troubleshooting

### **Common Issues**
```bash
# Service not responding
docker-compose restart <service_name>

# Database connection issues  
docker-compose down && docker-compose up -d

# Port conflicts
# Change ports in docker-compose.yml if needed

# API authentication errors
# Verify API key: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

### **Getting Help**
- **Health Checks**: Monitor service status via `/health` endpoints
- **Logs**: Check Docker logs for detailed error information
- **API Docs**: Interactive documentation at `/docs` endpoints
- **Database**: Connect via DBeaver for data inspection

## 📊 Platform Statistics

### **Current Status**
- **Services**: 5/5 Live ✅
- **API Endpoints**: 61 total (55 Gateway + 6 Agent)
- **Database**: PostgreSQL 17 with 17 tables
- **Candidates**: 31 with complete profiles
- **Jobs**: 19 active postings
- **Uptime**: 99.9% target
- **Cost**: $0/month (Free tier)

### **Performance Metrics**
- **API Response**: <100ms average
- **AI Matching**: <0.02s with caching
- **Success Rate**: 85.7% endpoint availability
- **Concurrent Users**: Multi-user support enabled

---

**🎉 You're ready to explore the complete BHIV HR Platform!**

Choose your path above and start experiencing enterprise-grade recruiting with AI-powered matching, comprehensive security, and real-time analytics.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*