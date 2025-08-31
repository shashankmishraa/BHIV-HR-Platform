# BHIV HR Platform - Quick Start Guide

## 🚀 **1-Minute Setup**

```bash
# Clone and start
git clone <repository-url>
cd bhiv-hr-platform

# Start essential services
docker-compose -f docker-compose.minimal.yml up -d

# Access portal
http://localhost:8501
```

## 📊 **Current System Status**

### **✅ Ready to Use**
- **17 Candidates** with real profiles
- **4 Active Jobs** across departments
- **AI Matching** operational (<0.02s response)
- **Values Assessment** 5-point scoring
- **Portal** fully functional

### **🔗 Access Points**
- **Portal**: http://localhost:8501 (Main Interface)
- **API**: http://localhost:8000/docs (Documentation)
- **AI Agent**: http://localhost:9000/docs (AI Service)

## 🎯 **Key Features Demo**

### **1. Search Candidates**
```bash
# Search by skills
curl -H "Authorization: Bearer myverysecureapikey123" \
  "http://localhost:8000/v1/candidates/search?skills=Python&job_id=1"
```

### **2. Get AI Shortlist**
```bash
# Top-5 AI recommendations
curl -H "Authorization: Bearer myverysecureapikey123" \
  "http://localhost:8000/v1/match/1/top"
```

### **3. Submit Values Assessment**
```bash
curl -X POST http://localhost:8000/v1/feedback \
  -H "Authorization: Bearer myverysecureapikey123" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "reviewer": "HR Manager",
    "values_scores": {"integrity": 5, "honesty": 4, "discipline": 5, "hard_work": 5, "gratitude": 4}
  }'
```

## 🧪 **Verify Everything Works**

```bash
# Run complete test suite
python test_endpoints.py

# Expected output: 9/9 tests passed
```

## 📋 **What You Get**

### **Complete Recruiting Platform**
- ✅ Job creation and management
- ✅ Candidate search and filtering
- ✅ AI-powered matching (100/100 scores)
- ✅ Values-based assessment
- ✅ Interview scheduling
- ✅ Offer management
- ✅ Real-time dashboard
- ✅ CSV reporting

### **Production-Ready**
- ✅ Microservices architecture
- ✅ Docker deployment
- ✅ API authentication
- ✅ Database persistence
- ✅ Comprehensive testing
- ✅ Complete documentation

## 🔧 **Minimal Commands**

```bash
# Start platform
docker-compose -f docker-compose.minimal.yml up -d

# Check status
docker-compose ps

# Stop platform
docker-compose down

# View logs
docker-compose logs -f
```

## 📈 **Next Steps**

1. **Explore Portal**: http://localhost:8501
2. **Try API**: http://localhost:8000/docs
3. **Add More Data**: Upload your own resumes
4. **Customize**: Modify job requirements
5. **Deploy**: Use for real recruiting

**The BHIV HR Platform is ready for immediate use with real data and full functionality.**