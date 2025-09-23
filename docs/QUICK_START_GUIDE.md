# 🚀 BHIV HR Platform - Quick Start Guide

## 🎯 Choose Your Path

### **🌐 Option 1: Use Live Platform (Recommended)**
Access the production platform immediately without any setup.

### **💻 Option 2: Local Development**
Run the complete platform on your local machine.

---

## 🌐 Live Platform Access

### **🔗 Service URLs**
- **HR Portal**: https://bhiv-hr-portal.onrender.com/ ✅
- **Client Portal**: https://bhiv-hr-client-portal.onrender.com/ ✅
- **API Gateway**: https://bhiv-hr-gateway.onrender.com/docs ✅
- **AI Agent**: https://bhiv-hr-agent.onrender.com/docs ✅

### **🔑 Demo Credentials**
```bash
# Client Portal Login
Username: TECH001
Password: demo123

# API Testing
API Key: myverysecureapikey123
```

### **⚡ Quick Test**
```bash
# Test API health
curl https://bhiv-hr-gateway.onrender.com/health

# Test authenticated endpoint
curl -H "Authorization: Bearer myverysecureapikey123" \
     https://bhiv-hr-gateway.onrender.com/v1/jobs
```

---

## 💻 Local Development Setup

### **📋 Prerequisites**
- Docker & Docker Compose
- Git
- PostgreSQL 17 (for database)
- 4GB+ RAM available

### **🔥 CRITICAL: Database Setup First**
```bash
# PRIORITY 1: Fix database schema issues (34 endpoints failing)
# Run database initialization before starting services
python init-database.py
python scripts/create_database_schema.sql

# Verify database tables exist
psql -h localhost -U bhiv_user -d bhiv_hr_nqzb -c "\dt"
```

### **🚀 Quick Start**
```bash
# 1. Clone repository
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform

# 2. CRITICAL: Setup database schema first
python init-database.py
# Verify: Should create candidates, jobs, interviews, feedback tables

# 3. Start all services
docker-compose -f docker-compose.production.yml up -d

# 4. Wait for services to start (30-60 seconds)
# Check status
docker-compose -f docker-compose.production.yml ps

# 5. Verify database connectivity
curl http://localhost:8000/test-candidates
```

### **🔗 Local URLs**
- **HR Portal**: http://localhost:8501 ✅
- **Client Portal**: http://localhost:8502 ✅
- **API Gateway**: http://localhost:8000/docs ✅
- **AI Agent**: http://localhost:9000/docs ✅

### **✅ Verify Setup**
```bash
# Test all services
curl http://localhost:8000/health
curl http://localhost:8501
curl http://localhost:9000/health
```

---

## 🎯 Platform Walkthrough

### **👥 For HR Teams**

#### **Step 1: Access HR Portal**
- Go to HR Portal (live or local)
- Navigate through the workflow menu

#### **Step 2: Create Job Positions**
- Select "🏢 Step 1: Create Job Positions"
- Fill job details and requirements
- Job automatically syncs with Client Portal

#### **Step 3: Upload Candidates**
- Select "📤 Step 2: Upload Candidates" or "📁 Batch Operations"
- Choose upload method:
  - **Individual Files**: ✅ Select multiple resumes (31 files processed)
  - **ZIP Archive**: ✅ Upload compressed files
  - **CSV Upload**: ✅ Structured candidate data with validation
- **Fixed**: Container paths now use absolute paths (/app/resume/)

#### **Step 4: AI Matching**
- Select "🎯 Step 4: AI Shortlist & Matching"
- Enter Job ID and generate AI shortlist
- Review top candidates with ✅ differentiated scores
- **Fixed**: Skills match display error resolved

#### **Step 5: Schedule Interviews**
- Select "📅 Step 5: Schedule Interviews"
- Schedule interviews for shortlisted candidates
- Track interview status

#### **Step 6: Values Assessment**
- Select "📊 Step 6: Submit Values Assessment"
- Rate candidates on 5 core values
- Submit comprehensive feedback

#### **Step 7: Export Reports**
- Select "🏆 Step 7: Export Assessment Reports"
- Choose report type:
  - Complete Candidate Report
  - Values Assessment Summary
  - Shortlist Analysis Report

### **🏢 For Clients**

#### **Step 1: Access Client Portal**
- Go to Client Portal (live or local)
- Login with demo credentials

#### **Step 2: Post Jobs**
- Click "Post New Job"
- Fill job requirements and details
- Submit job posting

#### **Step 3: Monitor Applications**
- View posted jobs and applications
- Check candidate pipeline status
- Review HR team progress

---

## 📊 Testing the Platform

### **🧪 Sample Data Testing**
```bash
# Process sample resumes (local only) - ✅ 31 files processed
python tools/comprehensive_resume_extractor.py

# Create sample jobs - ✅ Real job data
python tools/dynamic_job_creator.py --count 5

# Sync to database - ✅ 68+ candidates loaded
python tools/database_sync_manager.py
```

### **🔍 API Testing**
```bash
# Test bulk candidate upload
curl -X POST "http://localhost:8000/v1/candidates/bulk" \
     -H "Authorization: Bearer myverysecureapikey123" \
     -H "Content-Type: application/json" \
     -d '{"candidates": [{"name": "Test User", "email": "test@example.com"}]}'

# Test AI matching
curl -X POST "http://localhost:9000/match" \
     -H "Content-Type: application/json" \
     -d '{"job_id": 1}'
```

---

## 🛠️ Common Operations

### **🔄 Restart Services (Local)**
```bash
# Restart all services
docker-compose -f docker-compose.production.yml restart

# Restart specific service
docker-compose -f docker-compose.production.yml restart portal

# Rebuild service with changes
docker-compose -f docker-compose.production.yml up -d --build portal
```

### **📊 Monitor System Health**
```bash
# Check service status
docker-compose -f docker-compose.production.yml ps

# View logs
docker-compose -f docker-compose.production.yml logs portal

# Monitor resources
docker stats
```

### **🗄️ Database Operations**
```bash
# Connect to database
docker exec -it bhivhraiplatform-db-1 psql -U bhiv_user -d bhiv_hr

# Check candidate count
docker exec bhivhraiplatform-db-1 psql -U bhiv_user -d bhiv_hr -c "SELECT COUNT(*) FROM candidates;"
```

---

## 🎯 Key Features to Try

### **✅ Must-Try Features**
1. **Advanced AI Matching v3.2.0**: ✅ Job-specific candidate scoring with ML algorithms
2. **Multi-Factor Scoring**: ✅ Skills (35%), Experience (25%), Values (20%), Location (10%), Interview (10%)
3. **Batch Resume Upload**: ✅ Upload multiple resumes and see extraction (31 files processed)
4. **Real-time Sync**: ✅ Post job in Client Portal, see in HR Portal instantly
5. **Values Assessment**: ✅ Complete 5-point values evaluation with algorithm integration
6. **Export Reports**: ✅ Download comprehensive assessment reports
7. **Dynamic Dashboard**: ✅ Live data from database, no hardcoded values

### **🔥 PRIORITY 1 FIXES NEEDED**
1. **Database Schema**: 34 endpoints failing due to missing tables - Run init-database.py first
2. **Parameter Validation**: Some endpoints need default parameters - Check API docs
3. **Performance**: Client Portal 3.3s response time - Needs optimization

### **🔍 Advanced Features**
1. **API Integration**: ⚠️ 90/127 endpoints functional (70.9% success rate)
2. **Job-Specific Matching**: ✅ Algorithm analyzes job requirements for targeted scoring
3. **Recruiter Preferences**: ✅ Integration with reviewer feedback and interview data
4. **Security Features**: ✅ Try 2FA setup and rate limiting
5. **Monitoring Dashboard**: ✅ View Prometheus metrics
6. **Search & Filter**: ✅ Advanced candidate search capabilities
7. **Real Data**: ✅ 68+ candidates from actual resume files
8. **Professional Codebase**: ✅ Clean structure, removed duplicates
9. **AI Agent Service**: ✅ 100% functional (15/15 endpoints)
10. **Performance**: ⚡ Average 1.038s response time, zero timeouts

---

## 📞 Support & Resources

### **📚 Documentation**
- **Project Structure**: `PROJECT_STRUCTURE.md`
- **Deployment Status**: `DEPLOYMENT_STATUS.md`
- **Current Features**: `docs/CURRENT_FEATURES.md`
- **User Guide**: `docs/USER_GUIDE.md`

### **🔗 Quick Links**
- **Live API Docs**: https://bhiv-hr-gateway.onrender.com/docs
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Batch Upload Guide**: `batch_upload_verification_guide.md`

### **⚡ Quick Commands**
```bash
# Health check all services
curl http://localhost:8000/health && echo " - Gateway OK"
curl http://localhost:8501 > /dev/null && echo "Portal OK"
curl http://localhost:9000/health && echo " - Agent OK"

# Test complete workflow
curl -H "Authorization: Bearer myverysecureapikey123" \
     http://localhost:8000/v1/jobs && echo " - Jobs API OK"
```

---

**🎯 Ready to Start!** Choose your preferred option above and begin exploring the BHIV HR Platform's comprehensive recruiting capabilities.

**Last Updated**: January 2025 | **Platform Version**: 3.2.0