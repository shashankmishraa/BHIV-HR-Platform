# ⚡ BHIV HR Platform - Quick Start Guide

**Get Started in 5 Minutes**  
**Generated**: January 2025  
**Platform**: Production Ready + Local Development  
**Status**: ✅ All Services Operational

---

## 🚀 Choose Your Path

### **🌐 Option 1: Use Live Production Platform (Recommended)**
**No setup required - Start immediately!**

### **💻 Option 2: Local Development Setup**
**Full control - Run on your machine**

---

## 🌐 Live Production Platform (0 Minutes Setup)

### **🎯 Instant Access**
All services are live and operational - no installation needed!

#### **Service URLs**
```bash
# API Gateway (55 endpoints)
https://bhiv-hr-gateway-46pz.onrender.com/docs

# AI Matching Engine (6 endpoints)  
https://bhiv-hr-agent-m1me.onrender.com/docs

# HR Portal (Complete HR workflow)
https://bhiv-hr-portal-cead.onrender.com/

# Client Portal (Enterprise interface)
https://bhiv-hr-client-portal-5g33.onrender.com/

# Candidate Portal (Job seeker interface)
https://bhiv-hr-candidate-portal.onrender.com/
```

#### **🔑 Demo Credentials**
```bash
# Client Portal Login
Username: TECH001
Password: demo123

# API Testing Key
API Key: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

#### **⚡ 30-Second Test**
```bash
# 1. Test API Health
curl https://bhiv-hr-gateway-46pz.onrender.com/health

# 2. Get Real Data (31 candidates)
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates

# 3. AI Matching Test
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top

# 4. Access HR Portal
# Visit: https://bhiv-hr-portal-cead.onrender.com/

# 5. Login to Client Portal
# Visit: https://bhiv-hr-client-portal-5g33.onrender.com/
# Use: TECH001 / demo123
```

---

## 💻 Local Development Setup (5 Minutes)

### **📋 Prerequisites**
```bash
# Required Software
✅ Docker & Docker Compose
✅ Python 3.12.7 (recommended)
✅ Git
✅ 8GB RAM minimum
✅ 10GB free disk space
```

### **🚀 Quick Setup**
```bash
# Step 1: Clone Repository (30 seconds)
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform

# Step 2: Environment Setup (30 seconds)
cp .env.example .env
# Edit .env if needed (optional for quick start)

# Step 3: Start All Services (3-4 minutes)
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Step 4: Verify Services (30 seconds)
curl http://localhost:8000/health    # Gateway
curl http://localhost:9000/health    # AI Agent
open http://localhost:8501           # HR Portal
open http://localhost:8502           # Client Portal
open http://localhost:8503           # Candidate Portal
```

### **🔧 Service Ports**
```bash
Gateway API:      http://localhost:8000
AI Agent API:     http://localhost:9000
HR Portal:        http://localhost:8501
Client Portal:    http://localhost:8502
Candidate Portal: http://localhost:8503
Database:         localhost:5432
```

---

## 🎯 First Steps Guide

### **1. Explore the HR Portal (2 minutes)**
```bash
# Visit HR Portal
http://localhost:8501  # Local
https://bhiv-hr-portal-cead.onrender.com/  # Production

# Try These Features:
✅ Dashboard Overview - See real-time metrics
✅ View 31 Real Candidates - Browse candidate database
✅ Check 19 Active Jobs - Review job postings
✅ AI Shortlisting - Test Phase 3 AI matching
✅ Export Reports - Download assessment data
```

### **2. Test Client Portal (1 minute)**
```bash
# Visit Client Portal
http://localhost:8502  # Local
https://bhiv-hr-client-portal-5g33.onrender.com/  # Production

# Login Credentials:
Username: TECH001
Password: demo123

# Explore:
✅ Client Dashboard - Job posting analytics
✅ Create New Job - Post a job opening
✅ View Candidates - See AI-matched candidates
✅ Schedule Interviews - Manage interview process
```

### **3. Try Candidate Portal (1 minute)**
```bash
# Visit Candidate Portal
http://localhost:8503  # Local
https://bhiv-hr-candidate-portal.onrender.com/  # Production

# Features:
✅ Register Account - Create candidate profile
✅ Browse Jobs - View available positions
✅ Apply for Jobs - Submit applications
✅ Track Applications - Monitor application status
```

### **4. API Testing (1 minute)**
```bash
# Test Gateway API (55 endpoints)
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/v1/jobs  # Local
     # OR
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs  # Production

# Test AI Agent (6 endpoints)
curl -X POST -H "Content-Type: application/json" \
     -d '{"job_id": 1}' \
     http://localhost:9000/match  # Local
     # OR
     https://bhiv-hr-agent-m1me.onrender.com/match  # Production
```

---

## 🔥 Key Features to Try

### **🤖 AI-Powered Matching**
```bash
# 1. Get AI Matches for Job
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top

# 2. Batch Processing
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"job_ids": [1, 2, 3]}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/batch

# 3. Candidate Analysis
curl https://bhiv-hr-agent-m1me.onrender.com/analyze/1
```

### **📊 Values Assessment**
```bash
# Submit 5-Point BHIV Values Assessment
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "integrity": 5,
       "honesty": 4,
       "discipline": 4,
       "hard_work": 5,
       "gratitude": 4,
       "comments": "Excellent candidate"
     }' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```

### **🔒 Security Features**
```bash
# Test 2FA Setup
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/2fa/setup

# Test Input Validation
curl -X POST -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     -H "Content-Type: application/json" \
     -d '{"input_data": "<script>alert(\"test\")</script>"}' \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/security/test-input-validation
```

---

## 📊 Real Data Available

### **Production Database**
```bash
# Current Real Data:
✅ 31 Candidates - Complete profiles with skills and experience
✅ 19 Jobs - Active job postings from 3 client companies
✅ 27 Resume Files - Processed resume files
✅ 3 Client Companies - TECH001, STARTUP01, ENTERPRISE01
✅ 3 HR Users - Different role levels
✅ Assessment Data - Values assessment framework
✅ Interview Data - Interview scheduling system
```

### **Data Verification**
```bash
# Check Database Status
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/database/schema

# Get Candidate Statistics
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/candidates/stats
```

---

## 🛠️ Development Workflow

### **Local Development Commands**
```bash
# Start Services
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# View Logs
docker-compose -f deployment/docker/docker-compose.production.yml logs -f

# Stop Services
docker-compose -f deployment/docker/docker-compose.production.yml down

# Restart Single Service
docker-compose -f deployment/docker/docker-compose.production.yml restart gateway

# Database Access
psql postgresql://bhiv_user:password@localhost:5432/bhiv_hr
```

### **Testing Commands**
```bash
# Run API Tests
python tests/api/test_endpoints.py

# Run Security Tests
python tests/security/test_security.py

# Run All Tests
python tests/run_all_tests.py

# Test Specific Portal
python tests/integration/test_client_portal.py
```

---

## 🔧 Configuration

### **Environment Variables**
```bash
# Database Configuration
DATABASE_URL=postgresql://bhiv_user:password@localhost:5432/bhiv_hr

# API Configuration
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=fallback_jwt_secret_key_for_client_auth_2025
CANDIDATE_JWT_SECRET=candidate_jwt_secret_key_2025

# Service URLs
GATEWAY_URL=http://gateway:8000
AGENT_SERVICE_URL=http://agent:9000
```

### **Service Configuration**
```bash
# Gateway Service (Port 8000)
- FastAPI 0.115.6
- 55 endpoints
- Triple authentication
- Rate limiting

# Agent Service (Port 9000)
- FastAPI 0.115.6
- 6 endpoints
- Phase 3 AI engine
- Semantic matching

# Portal Services (Ports 8501-8503)
- Streamlit 1.41.1
- Real-time data integration
- Interactive interfaces
```

---

## 🚨 Troubleshooting

### **Common Issues & Solutions**

#### **Services Not Starting**
```bash
# Check Docker
docker --version
docker-compose --version

# Check Ports
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501

# Restart Docker
sudo systemctl restart docker  # Linux
# Restart Docker Desktop      # Windows/Mac
```

#### **Database Connection Issues**
```bash
# Check Database Container
docker-compose -f deployment/docker/docker-compose.production.yml ps

# Check Database Logs
docker-compose -f deployment/docker/docker-compose.production.yml logs db

# Reset Database
docker-compose -f deployment/docker/docker-compose.production.yml down -v
docker-compose -f deployment/docker/docker-compose.production.yml up -d
```

#### **API Authentication Issues**
```bash
# Verify API Key
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/health

# Check Environment Variables
echo $API_KEY_SECRET

# Test Without Authentication (health endpoints)
curl http://localhost:8000/health
```

#### **Portal Access Issues**
```bash
# Check Service Status
curl http://localhost:8501/  # Should return HTML
curl http://localhost:8502/  # Should return HTML
curl http://localhost:8503/  # Should return HTML

# Check Streamlit Logs
docker-compose -f deployment/docker/docker-compose.production.yml logs portal
docker-compose -f deployment/docker/docker-compose.production.yml logs client_portal
docker-compose -f deployment/docker/docker-compose.production.yml logs candidate_portal
```

### **Performance Issues**
```bash
# Check System Resources
docker stats

# Check Service Health
curl http://localhost:8000/health/detailed
curl http://localhost:9000/health

# Monitor Performance
curl http://localhost:8000/metrics
```

---

## 📚 Next Steps

### **After Quick Start**
1. **Explore Documentation**: Read [CURRENT_FEATURES.md](CURRENT_FEATURES.md) for complete feature list
2. **API Integration**: Check [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md) for all 61 endpoints
3. **Security Setup**: Review [SECURITY_AUDIT.md](security/SECURITY_AUDIT.md) for security features
4. **Production Deploy**: Follow [RENDER_DEPLOYMENT_GUIDE.md](deployment/RENDER_DEPLOYMENT_GUIDE.md)

### **Advanced Usage**
```bash
# Data Processing Tools
python tools/dynamic_job_creator.py --count 10
python tools/comprehensive_resume_extractor.py
python tools/database_sync_manager.py

# Custom Configuration
# Edit config/production.env
# Modify deployment/docker/docker-compose.production.yml

# Monitoring Setup
# Access Prometheus metrics at /metrics
# Set up custom dashboards
```

### **Integration Examples**
```python
# Python Integration
import requests

BASE_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Get candidates
candidates = requests.get(f"{BASE_URL}/v1/candidates", headers=headers).json()

# AI matching
matches = requests.get(f"{BASE_URL}/v1/match/1/top", headers=headers).json()
```

---

## 🎯 Success Checklist

### **✅ Quick Start Complete When:**
- [ ] Can access all 5 portal URLs
- [ ] API health checks return "healthy"
- [ ] Can login to client portal (TECH001/demo123)
- [ ] Can view 31 candidates in HR portal
- [ ] AI matching returns candidate scores
- [ ] Can create new job posting
- [ ] Can register new candidate
- [ ] Database shows 17 tables
- [ ] All 61 endpoints respond correctly
- [ ] Export functionality works

### **🚀 Ready for Production When:**
- [ ] All services running smoothly
- [ ] Performance metrics acceptable (<100ms API)
- [ ] Security features tested (2FA, validation)
- [ ] Data integrity verified
- [ ] Monitoring setup complete
- [ ] Backup strategy in place

---

## 📞 Support & Resources

### **Documentation Links**
- **Complete Features**: [CURRENT_FEATURES.md](CURRENT_FEATURES.md)
- **API Reference**: [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)
- **Architecture**: [SERVICES_ARCHITECTURE_SUMMARY.md](architecture/SERVICES_ARCHITECTURE_SUMMARY.md)
- **Deployment**: [DEPLOYMENT_STATUS.md](architecture/DEPLOYMENT_STATUS.md)

### **Live Platform URLs**
- **Gateway API**: https://bhiv-hr-gateway-46pz.onrender.com/docs
- **Agent API**: https://bhiv-hr-agent-m1me.onrender.com/docs
- **HR Portal**: https://bhiv-hr-portal-cead.onrender.com/
- **Client Portal**: https://bhiv-hr-client-portal-5g33.onrender.com/
- **Candidate Portal**: https://bhiv-hr-candidate-portal.onrender.com/

### **Demo Credentials**
```bash
# Client Portal
Username: TECH001
Password: demo123

# API Testing
API Key: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
```

---

**BHIV HR Platform Quick Start Guide** - Get started in 5 minutes with live production platform or local development setup.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: January 2025 | **Setup Time**: 0-5 minutes | **Services**: 5/5 Live | **Status**: ✅ Ready to Use