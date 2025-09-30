# 🔍 Mock, Pre-loaded & Hardcoded Content Analysis

**Complete inventory of all mock data, hardcoded values, and pre-loaded content in BHIV HR Platform**

---

## 📊 **Executive Summary**

| Category | Count | Status | Impact |
|----------|-------|--------|---------|
| **Hardcoded Credentials** | 8+ | ⚠️ Security Risk | High |
| **Mock API Responses** | 15+ | 🔄 Functional | Medium |
| **Pre-loaded Data** | 31 candidates | ✅ Real Data | Low |
| **Demo Accounts** | 2 clients | 🔧 Demo Purpose | Low |
| **Fallback Values** | 20+ | 🛡️ Safety Net | Low |

---

## 🔐 **1. HARDCODED CREDENTIALS & SECRETS**

### **🚨 Critical Security Issues**

#### **API Keys & Tokens**
```python
# Gateway Service (main.py)
API_KEY_SECRET = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
JWT_SECRET = "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA"

# Agent Service (app.py) 
DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"

# Portal Services
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
```

#### **Database Credentials**
```python
# Multiple services contain:
DB_HOST = "dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com"
DB_USER = "bhiv_user"  
DB_PASSWORD = "3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2"
DB_NAME = "bhiv_hr_jcuu"
```

#### **Demo Client Passwords**
```python
# Client Portal Auth Service (auth_service.py)
DEFAULT_CLIENT_PASSWORD = os.getenv('DEFAULT_CLIENT_PASSWORD', 'TempPass123!')

# Gateway API (main.py)
valid_clients = {
    "TECH001": "demo123",
    "STARTUP01": "startup123", 
    "ENTERPRISE01": "enterprise123"
}
```

#### **2FA Demo Secrets**
```python
# Gateway Service - 2FA endpoints
stored_secret = "JBSWY3DPEHPK3PXP"  # Hardcoded TOTP secret
demo_secret = "JBSWY3DPEHPK3PXP"
test_codes = ["123456", "654321", "111111"]
```

---

## 🎭 **2. MOCK API RESPONSES & FALLBACK DATA**

### **Gateway Service Mock Responses**

#### **Client Authentication Mock**
```python
# /v1/client/login endpoint
valid_clients = {
    "TECH001": "demo123",
    "STARTUP01": "startup123", 
    "ENTERPRISE01": "enterprise123"
}
```

#### **Security Testing Mock Data**
```python
# /v1/security/blocked-ips
blocked_ips = [
    {"ip": "192.168.1.100", "reason": "Rate limit exceeded"},
    {"ip": "10.0.0.50", "reason": "Suspicious activity"}
]

# /v1/security/csp-violations  
violations = [{
    "violated_directive": "script-src",
    "blocked_uri": "https://malicious-site.com/script.js"
}]
```

#### **Assessment & Workflow Mock**
```python
# /v1/feedback endpoint - Returns mock success without database storage
# /v1/offers endpoint - Returns mock offer creation
# Password generation - Uses random generation but returns mock strength scores
```

### **Agent Service Mock Scoring**

#### **AI Matching Fallback**
```python
# When semantic matching fails, returns hardcoded scores:
matches = [{
    "score": 85.5,
    "skills_match": row[3] or "",
    "experience_match": 80.0,
    "values_alignment": 4.2,
    "recommendation_strength": "Strong Match"
}]
```

#### **Skills Matching Mock Logic**
```python
# Hardcoded skill categories and scoring
tech_keywords = {
    'programming': ['python', 'java', 'javascript'],
    'web_frontend': ['react', 'angular', 'vue'],
    'database': ['sql', 'mysql', 'postgresql']
}
```

### **Portal Services Mock Data**

#### **Dashboard Statistics Mock**
```python
# HR Portal (app.py) - Fallback metrics when API fails
total_candidates = 31  # Real database count
total_jobs = 4        # Real jobs count  
total_feedback = 0    # Mock feedback count

# Skills distribution (hardcoded based on 31 candidates)
prog_skills = {
    'Python': 25, 'JavaScript': 18, 'Java': 20, 'C++': 8, 'Go': 31
}
```

#### **Client Portal Mock Calculations**
```python
# Client Portal (app.py) - Hash-based client ID conversion
client_id_num = hash(client_id_str) % 1000  # Convert string to number

# Mock values alignment calculation
values_alignment = min(5.0, candidate.get('score', 0) / 20)
```

---

## 📋 **3. PRE-LOADED DEMO DATA**

### **Demo Client Accounts**
```python
# Auto-created during database initialization
default_clients = [
    {
        'client_id': 'TECH001',
        'company_name': 'TechCorp Solutions', 
        'email': 'admin@techcorp.com',
        'password': 'TempPass123!' or env.DEFAULT_CLIENT_PASSWORD
    },
    {
        'client_id': 'STARTUP01',
        'company_name': 'InnovateLab',
        'email': 'hello@innovatelab.com', 
        'password': 'TempPass123!' or env.DEFAULT_CLIENT_PASSWORD
    }
]
```

### **Real Candidate Data (31 Records)**
**Source**: `data/candidates.csv`
- **Names**: Adarshyadav, Anmol, Anurag, Arulselvamjegan, etc.
- **Locations**: Mumbai (18), Pune (3), Delhi (2), Nashik (2), Others (6)
- **Skills**: Python (25), JavaScript (18), Java (20), Go (31), etc.
- **Education**: All have Masters degree
- **Experience**: Mostly "Fresher" with 2-4 years for some

### **Dynamic Job Templates**
**Source**: `tools/dynamic_job_creator.py`
```python
job_templates = {
    "software_engineer": {
        "levels": ["Junior", "Mid-Level", "Senior", "Lead", "Principal"],
        "salary_ranges": {"Junior": "$60k-80k", "Senior": "$120k-160k"}
    },
    "data_scientist": {
        "trending_skills": ["Python", "R", "SQL", "TensorFlow", "PyTorch"]
    }
}
```

---

## 🔧 **4. CONFIGURATION HARDCODED VALUES**

### **Service URLs & Endpoints**
```python
# Default service URLs when environment variables missing
API_BASE = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"  
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-5g33.onrender.com"
HR_PORTAL_URL = "https://bhiv-hr-portal-cead.onrender.com"
```

### **Rate Limiting Configuration**
```python
# Gateway Service - Hardcoded rate limits
RATE_LIMITS = {
    "default": {
        "/v1/jobs": 100,
        "/v1/candidates/search": 50,
        "/v1/match": 20,
        "default": 60
    },
    "premium": {
        "/v1/jobs": 500,
        "/v1/candidates/search": 200
    }
}
```

### **Algorithm Parameters**
```python
# Agent Service - Hardcoded scoring weights
base_multiplier = 75
skill_bonus_threshold = 3
experience_bonus_rates = {
    "5+ years": 0.2,
    "3-5 years": 0.15, 
    "2-3 years": 0.1
}
```

---

## 📊 **5. MOCK BUSINESS LOGIC**

### **Values Assessment Mock**
```python
# HR Portal - Mock values scoring when no real assessment
if assessment_completed == 'Yes':
    average_values_score = '4.2/5'
    top_strength = 'Honesty'
    development_area = 'Discipline'
    cultural_fit_rating = 'Excellent'
else:
    # All values return 'Not Assessed'
```

### **Pipeline Conversion Mock**
```python
# Client Portal - Mock conversion rates
applied_to_screened = 100%  # Always 100%
screened_to_reviewed = 100%  # Always 100%
interview_rate = interviews_scheduled/total_applications * 100
offer_rate = offers_made/interviews_scheduled * 100 if interviews > 0 else 0
```

### **AI Scoring Mock Logic**
```python
# Agent Service - Enhanced scoring with mock variations
candidate_variation = (cand_id % 13) * 1.2  # ID-based variation
skill_diversity_bonus = len(set(matched_skills)) * 2
experience_multiplier = 1 + (exp_years_val * 0.05)

# Score range enforcement
overall_score = max(45.0, min(92.0, calculated_score))
```

---

## 🎯 **6. DEMO & TESTING CONTENT**

### **Security Testing Mock**
```python
# Password strength testing with hardcoded responses
strength_levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
sample_passwords = [
    {"password": "weak", "expected_strength": "Very Weak"},
    {"password": "StrongPass123!", "expected_strength": "Very Strong"}
]
```

### **2FA Demo Setup**
```python
# Hardcoded demo QR code and test tokens
demo_qr_url = "https://chart.googleapis.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/BHIV%20HR%20Platform:demo_user%3Fsecret%3DJBSWY3DPEHPK3PXP"
backup_codes = [f"BACKUP-{secrets.token_hex(4).upper()}" for _ in range(10)]
```

### **Export Mock Data**
```python
# When exporting reports, includes mock assessment data
mock_feedback_score = 'Not Assessed'
mock_values_assessment = 'Not Assessed' 
mock_shortlist_status = 'Under Review'
mock_hiring_decision = 'Pending Review'
```

---

## ⚠️ **7. SECURITY & PRODUCTION CONCERNS**

### **🚨 High Priority Issues**

1. **Exposed Production Credentials**
   - Database passwords in source code
   - API keys hardcoded in multiple files
   - JWT secrets visible in plain text

2. **Predictable Demo Accounts**
   - Default passwords like "demo123", "TempPass123!"
   - Hardcoded client IDs and company names

3. **Mock Security Features**
   - Hardcoded 2FA secrets
   - Predictable test tokens
   - Mock blocked IP addresses

### **🔧 Medium Priority Issues**

1. **Fallback Logic Dependencies**
   - Services rely on hardcoded fallbacks when APIs fail
   - Mock scoring algorithms may not reflect real performance

2. **Configuration Hardcoding**
   - Service URLs embedded in code
   - Rate limits not configurable
   - Algorithm parameters fixed

### **✅ Low Priority (Acceptable)**

1. **Real Candidate Data**
   - 31 actual candidates from resume processing
   - Legitimate skill distributions
   - Real location and experience data

2. **Dynamic Job Creation**
   - Market-based job templates
   - Configurable skill trends
   - Realistic salary ranges

---

## 🔄 **8. RECOMMENDATIONS**

### **Immediate Actions (Security)**
1. **Move all credentials to environment variables**
2. **Remove hardcoded API keys and database passwords**
3. **Generate unique demo passwords per deployment**
4. **Remove hardcoded 2FA secrets**

### **Short-term Improvements**
1. **Replace mock API responses with database queries**
2. **Implement real values assessment storage**
3. **Add configurable algorithm parameters**
4. **Create proper fallback mechanisms**

### **Long-term Enhancements**
1. **Implement real-time assessment tracking**
2. **Add configurable business rules**
3. **Create admin interface for demo data management**
4. **Implement proper audit logging**

---

## 📈 **9. IMPACT ASSESSMENT**

### **Production Readiness Score: 6.5/10**

| Component | Score | Notes |
|-----------|-------|-------|
| **Security** | 4/10 | Hardcoded credentials, exposed secrets |
| **Functionality** | 8/10 | Most features work with real data |
| **Scalability** | 7/10 | Good architecture, some hardcoded limits |
| **Maintainability** | 6/10 | Mixed real/mock data complicates maintenance |
| **User Experience** | 8/10 | Smooth demo experience with realistic data |

### **Deployment Risk Level: MEDIUM-HIGH**
- **High**: Security vulnerabilities from exposed credentials
- **Medium**: Functional dependencies on mock data
- **Low**: User experience and core functionality

---

## 🎯 **10. CONCLUSION**

The BHIV HR Platform contains a **strategic mix of real and mock content**:

**✅ Strengths:**
- 31 real candidates with actual skills and experience
- Functional AI matching with real database integration
- Comprehensive API with 46 working endpoints
- Professional demo experience for clients

**⚠️ Concerns:**
- Critical security vulnerabilities from hardcoded credentials
- Mixed real/mock data creates maintenance complexity
- Some business logic relies on fallback mock responses

**🎯 Priority Actions:**
1. **Secure all hardcoded credentials immediately**
2. **Implement proper environment variable management**
3. **Replace critical mock responses with real database operations**
4. **Maintain demo functionality while improving security**

**Overall Assessment**: The platform demonstrates strong technical capability with real data integration, but requires immediate security hardening before production deployment.

---

*Last Updated: January 2025 | Status: Comprehensive Analysis Complete*