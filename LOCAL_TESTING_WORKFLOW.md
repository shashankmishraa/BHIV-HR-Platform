# 🧪 Local Testing Workflow Guide

## 🚀 **Setup Local Environment**

### **1. Start All Services**
```bash
cd BHIV-HR-Platform
docker-compose -f deployment/docker/docker-compose.production.yml up -d
```

### **2. Verify Services**
```bash
# Check all services are running
curl http://localhost:8000/health  # Gateway
curl http://localhost:9000/health  # Agent
curl http://localhost:8501         # HR Portal
curl http://localhost:8502         # Client Portal
curl http://localhost:8503         # Candidate Portal
```

---

## 📝 **Complete Testing Workflow**

### **Step 1: Client Registration**
1. **Open Client Portal**: http://localhost:8502
2. **Click "Register" Tab**
3. **Fill Registration Form**:
   - Client ID: `TESTCLIENT01`
   - Company Name: `Test Company Ltd`
   - Contact Email: `admin@testcompany.com`
   - Password: `SecurePass123!`
   - Confirm Password: `SecurePass123!`
4. **Click "Secure Registration"**
5. **Verify Success Message**: "Registration successful! You can now login securely."

### **Step 2: Client Login**
1. **Click "Login" Tab**
2. **Enter Credentials**:
   - Client ID: `TESTCLIENT01`
   - Password: `SecurePass123!`
3. **Click "Secure Login"**
4. **Verify**: Client portal dashboard loads with company name

### **Step 3: Client Creates Job**
1. **In Client Portal**: Navigate to "📝 Job Posting"
2. **Fill Job Form**:
   - Job Title: `Senior Python Developer`
   - Department: `Engineering`
   - Location: `San Francisco, CA`
   - Experience Level: `Senior`
   - Type: `Full-time`
   - Salary Range: `$120,000 - $150,000`
   - Description: `We need a senior Python developer with FastAPI experience`
   - Required Skills: `Python, FastAPI, PostgreSQL, Docker, AWS`
3. **Click "🚀 Post Job"**
4. **Verify**: Job posted successfully with Job ID

### **Step 4: Candidate Registration**
1. **Open Candidate Portal**: http://localhost:8503
2. **Click "Register" (if available) or use API**:

**API Registration**:
```bash
curl -X POST http://localhost:8000/v1/candidate/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "password": "CandidatePass123!",
    "phone": "+1-555-0123",
    "location": "San Francisco, CA",
    "experience_years": 5,
    "technical_skills": "Python, FastAPI, PostgreSQL, Docker",
    "education_level": "Bachelor",
    "seniority_level": "Senior"
  }'
```

### **Step 5: Candidate Login**
**API Login**:
```bash
curl -X POST http://localhost:8000/v1/candidate/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.smith@example.com",
    "password": "CandidatePass123!"
  }'
```
**Save the returned token for next steps**

### **Step 6: Candidate Views Jobs**
```bash
# Get all jobs
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/v1/jobs
```

### **Step 7: Candidate Applies for Job**
```bash
# Apply for job (use job_id from step 3 and candidate_id from step 4)
curl -X POST http://localhost:8000/v1/candidate/apply \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "cover_letter": "I am very interested in this Senior Python Developer position. My 5 years of experience with Python and FastAPI make me a perfect fit."
  }'
```

### **Step 8: Client Reviews Candidates**
1. **In Client Portal**: Navigate to "👥 Candidate Review"
2. **Select Job**: Choose "Senior Python Developer (ID: 1)"
3. **View AI Matches**: Click "🤖 Get AI Matches"
4. **Review Candidate**: John Smith should appear with AI score
5. **Actions Available**:
   - ✅ Approve (for interview)
   - ❌ Reject

### **Step 9: Client Schedules Interview**
```bash
# Schedule interview
curl -X POST http://localhost:8000/v1/interviews \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "interview_date": "2025-01-15T10:00:00",
    "interview_type": "Technical",
    "interviewer": "Jane Smith",
    "location": "Conference Room A"
  }'
```

### **Step 10: Client Provides Feedback**
```bash
# Submit values assessment
curl -X POST http://localhost:8000/v1/feedback \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "integrity": 5,
    "honesty": 5,
    "discipline": 4,
    "hard_work": 5,
    "gratitude": 4,
    "comments": "Excellent candidate with strong technical skills and values alignment"
  }'
```

### **Step 11: Client Makes Job Offer**
```bash
# Create job offer
curl -X POST http://localhost:8000/v1/offers \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "salary": 125000,
    "start_date": "2025-02-01",
    "terms": "Full-time position with health insurance, 401k, and PTO"
  }'
```

### **Step 12: Candidate Checks Applications**
```bash
# Get candidate applications
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/v1/candidate/applications/1
```

---

## 🔍 **Verification Points**

### **Database Verification**
```bash
# Connect to local database
psql postgresql://bhiv_user:bhiv_local_password_2025@localhost:5432/bhiv_hr

# Check data
SELECT * FROM clients WHERE client_id = 'TESTCLIENT01';
SELECT * FROM candidates WHERE email = 'john.smith@example.com';
SELECT * FROM jobs WHERE title = 'Senior Python Developer';
SELECT * FROM job_applications WHERE candidate_id = 1 AND job_id = 1;
SELECT * FROM interviews WHERE candidate_id = 1;
SELECT * FROM feedback WHERE candidate_id = 1;
SELECT * FROM offers WHERE candidate_id = 1;
```

### **Portal Verification**
1. **Client Portal** (http://localhost:8502):
   - Login with `TESTCLIENT01` / `SecurePass123!`
   - Check "👥 Candidate Review" shows John Smith
   - Check "🎯 Match Results" shows AI matching
   - Check "📊 Reports & Analytics" shows updated metrics

2. **HR Portal** (http://localhost:8501):
   - View all candidates (should include John Smith)
   - View all jobs (should include Senior Python Developer)
   - Check AI matching functionality

---

## 🧪 **Test Scenarios**

### **Scenario A: Happy Path**
✅ Client registers → ✅ Client posts job → ✅ Candidate registers → ✅ Candidate applies → ✅ Client reviews → ✅ Interview scheduled → ✅ Offer made

### **Scenario B: Multiple Candidates**
1. Register 3 different candidates with varying skills
2. Have all apply for the same job
3. Check AI matching ranks them correctly
4. Test batch operations

### **Scenario C: Error Handling**
1. Try duplicate client registration (should fail)
2. Try duplicate candidate email (should fail)
3. Try applying for same job twice (should fail)
4. Test invalid credentials

---

## 📊 **Expected Results**

### **Client Portal Dashboard**
- Active Jobs: 1
- Total Applications: 1
- Interviews Scheduled: 1
- Offers Made: 1

### **AI Matching**
- John Smith should score 80+ for Python Developer role
- Skills match should highlight: Python, FastAPI, PostgreSQL
- Location match should be positive (both San Francisco)

### **Database Records**
- 1 client record in `clients` table
- 1 candidate record in `candidates` table
- 1 job record in `jobs` table
- 1 application in `job_applications` table
- 1 interview in `interviews` table
- 1 feedback in `feedback` table
- 1 offer in `offers` table

---

## 🚨 **Troubleshooting**

### **Services Not Starting**
```bash
# Check logs
docker-compose -f deployment/docker/docker-compose.production.yml logs gateway
docker-compose -f deployment/docker/docker-compose.production.yml logs db
```

### **Database Connection Issues**
```bash
# Reset database
docker-compose -f deployment/docker/docker-compose.production.yml down -v
docker-compose -f deployment/docker/docker-compose.production.yml up -d
```

### **Portal Not Loading**
```bash
# Check Streamlit health
curl http://localhost:8501/_stcore/health
curl http://localhost:8502/_stcore/health
curl http://localhost:8503/_stcore/health
```

---

## ✅ **Success Criteria**

1. ✅ Client can register and login
2. ✅ Client can post jobs
3. ✅ Candidate can register and login
4. ✅ Candidate can apply for jobs
5. ✅ Client can see candidate applications
6. ✅ AI matching works and shows scores
7. ✅ Interview scheduling works
8. ✅ Feedback system works
9. ✅ Job offers can be created
10. ✅ All data persists in database

**Complete end-to-end workflow testing ready!** 🎉