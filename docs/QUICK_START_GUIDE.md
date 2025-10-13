# 🚀 BHIV HR Platform - Quick Start Guide

**Get started with the BHIV HR Platform in 5 minutes**

## 📋 Prerequisites

### **System Requirements**
- **Python**: 3.12.7+ (Required for Phase 3)
- **Docker**: Latest version with Docker Compose
- **Git**: For repository cloning
- **Internet**: For dependency installation

### **Recommended Setup**
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **OS**: Windows 10/11, macOS, or Linux

## 🎯 Choose Your Path

### **Option 1: Use Live Platform (Recommended)**
Access the production platform immediately without any setup.

### **Option 2: Local Development**
Run the complete platform on your local machine.

---

## 🌐 Option 1: Live Platform Access

### **Step 1: Access Production Services**

| Service | URL | Purpose |
|---------|-----|---------|
| **API Gateway** | https://bhiv-hr-gateway-46pz.onrender.com/docs | REST API (50 endpoints) ✅ |
| **AI Agent** | https://bhiv-hr-agent-m1me.onrender.com/docs | AI Matching (6 endpoints) ❌ |
| **HR Portal** | https://bhiv-hr-portal-cead.onrender.com/ | HR Dashboard ✅ |
| **Client Portal** | https://bhiv-hr-client-portal-5g33.onrender.com/ | Client Interface ✅ |

### **Step 2: Test API Access**

```bash
# Test API health
curl https://bhiv-hr-gateway-46pz.onrender.com/health

# Test with authentication
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

### **Step 3: Login to Portals**

**Client Portal Credentials:**
- **Username**: `TECH001`
- **Password**: `demo123`

**HR Portal:**
- Direct access (no login required for demo)

### **Step 4: Explore Features**

1. **Post a Job** (Client Portal)
2. **Upload Candidates** (HR Portal)
3. **Run AI Matching** (Both Portals)
4. **Submit Assessments** (HR Portal)

---

## 💻 Option 2: Local Development Setup

### **Step 1: Clone Repository**

```bash
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform
```

### **Step 2: Environment Configuration**

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional for local development)
# Default values work for local setup
```

### **Step 3: Start All Services**

```bash
# Start complete platform with Docker Compose
docker-compose -f docker-compose.production.yml up -d

# Wait for services to initialize (30-60 seconds)
```

### **Step 4: Verify Services**

```bash
# Check service health
curl http://localhost:8000/health    # Gateway
curl http://localhost:9000/health    # AI Agent

# Access web interfaces
open http://localhost:8501           # HR Portal
open http://localhost:8502           # Client Portal
```

### **Step 5: Test Complete Workflow**

```bash
# Test API endpoints
curl http://localhost:8000/v1/jobs

# Test AI matching
curl -X POST http://localhost:9000/match \
     -H "Content-Type: application/json" \
     -d '{"job_id": 1}'
```

---

## 🧪 Verification Tests

### **API Health Checks**

```bash
# Gateway Service (50 endpoints)
curl https://bhiv-hr-gateway-46pz.onrender.com/health
# Expected: {"status": "healthy", "version": "3.1.0"}

# AI Agent Service (6 endpoints) - OFFLINE
curl https://bhiv-hr-agent-m1me.onrender.com/health
# Expected: Connection timeout (service offline)
```

### **Portal Access Tests**

```bash
# HR Portal
curl -I https://bhiv-hr-portal-cead.onrender.com/
# Expected: HTTP 200 OK

# Client Portal
curl -I https://bhiv-hr-client-portal-5g33.onrender.com/
# Expected: HTTP 200 OK
```

### **Database Connectivity**

```bash
# Test database connection
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates
# Expected: {"database_status": "connected", "total_candidates": 11}
```

---

## 🎯 First Workflow: Complete Hiring Process

### **Step 1: Create Job Posting**

**Via Client Portal:**
1. Go to https://bhiv-hr-client-portal-5g33.onrender.com/
2. Login with `TECH001` / `demo123`
3. Navigate to "Job Posting"
4. Fill job details and submit

**Via API:**
```bash
curl -X POST \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "department": "Engineering", 
    "location": "Remote",
    "experience_level": "Senior",
    "requirements": "Python, FastAPI, PostgreSQL",
    "description": "Join our engineering team..."
  }' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs
```

### **Step 2: Upload Candidates**

**Via HR Portal:**
1. Go to https://bhiv-hr-portal-cead.onrender.com/
2. Navigate to "Upload Candidates"
3. Upload CSV file or use batch upload

**Via API:**
```bash
curl -X POST \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": [
      {
        "name": "John Doe",
        "email": "john@example.com",
        "technical_skills": "Python, FastAPI, PostgreSQL",
        "experience_years": 5
      }
    ]
  }' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/candidates/bulk
```

### **Step 3: Run AI Matching**

**Via Portal:**
1. Navigate to "AI Shortlist & Matching"
2. Select job ID
3. Click "Generate AI Shortlist"

**Via API:**
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/match/1/top?limit=10
```

### **Step 4: Submit Values Assessment**

**Via HR Portal:**
1. Navigate to "Submit Values Assessment"
2. Fill 5-point assessment form
3. Submit feedback

**Via API:**
```bash
curl -X POST \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "integrity": 5,
    "honesty": 4,
    "discipline": 4,
    "hard_work": 5,
    "gratitude": 4
  }' \
  https://bhiv-hr-gateway-46pz.onrender.com/v1/feedback
```

---

## 🔧 Troubleshooting

### **Common Issues**

**1. Services Not Starting (Local)**
```bash
# Check Docker status
docker ps

# View service logs
docker-compose -f docker-compose.production.yml logs gateway
docker-compose -f docker-compose.production.yml logs agent
```

**2. API Authentication Errors**
```bash
# Verify API key format
echo "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

# Test authentication
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/health
```

**3. Portal Access Issues**
```bash
# Check portal status
curl -I https://bhiv-hr-portal-cead.onrender.com/
curl -I https://bhiv-hr-client-portal-5g33.onrender.com/

# Clear browser cache and try again
```

**4. Database Connection Issues**
```bash
# Test database connectivity
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates
```

### **Getting Help**

**1. Check Service Status**
- All services: https://bhiv-hr-gateway-46pz.onrender.com/health
- Detailed metrics: https://bhiv-hr-gateway-46pz.onrender.com/metrics

**2. Review Documentation**
- API Docs: https://bhiv-hr-gateway-46pz.onrender.com/docs
- User Guide: [docs/USER_GUIDE.md](USER_GUIDE.md)

**3. Common Solutions**
- **Rate Limiting**: Wait 1 minute and retry
- **Authentication**: Verify Bearer token format
- **CORS Issues**: Use proper headers in requests

---

## 📊 Next Steps

### **Explore Advanced Features**

1. **Phase 3 AI Matching**
   - Adaptive scoring with company preferences
   - Cultural fit analysis
   - Enhanced batch processing

2. **Security Features**
   - 2FA authentication
   - Rate limiting
   - Input validation

3. **Analytics & Reporting**
   - Export assessment reports
   - Performance metrics
   - Business analytics

### **Integration Options**

1. **API Integration**
   - REST API with 50 endpoints
   - Webhook support
   - Real-time notifications

2. **Portal Customization**
   - White-label options
   - Custom branding
   - Workflow customization

### **Production Deployment**

1. **Environment Setup**
   - Production database
   - SSL certificates
   - Load balancing

2. **Monitoring & Maintenance**
   - Health checks
   - Performance monitoring
   - Backup strategies

---

## 📞 Support & Resources

### **Live Platform**
- **Status**: ⚠️ 4/5 services operational (Agent offline)
- **Uptime**: 99.9% target (operational services)
- **Response Time**: <100ms average

### **Documentation**
- **API Reference**: [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Deployment Guide**: [deployment/RENDER_DEPLOYMENT_GUIDE.md](deployment/RENDER_DEPLOYMENT_GUIDE.md)

### **Development**
- **GitHub**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Issues**: GitHub Issues for bug reports
- **Contributions**: Pull requests welcome

---

**🎉 You're ready to start using the BHIV HR Platform!**

Choose your path above and begin exploring the comprehensive recruiting solution with AI-powered matching and values-based assessment.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*