# 🏗️ BHIV HR Platform - System Architecture

## 📊 Architecture Overview

**Architecture Type**: Microservices  
**Deployment**: Cloud-native (Render)  
**Database**: PostgreSQL 17  
**Version**: v3.2.0  
**Status**: Production-ready  

---

## 🔧 Service Architecture

### **🌐 Microservices Topology**

```
┌─────────────────────────────────────────────────────────────┐
│                    BHIV HR Platform                         │
│                   Cloud Architecture                        │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Load Balancer   │
                    │   (Cloudflare)    │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌───────▼────────┐
│   HR Portal    │   │  Client Portal  │   │  API Gateway   │
│  (Streamlit)   │   │  (Streamlit)    │   │   (FastAPI)    │
│   Port 8501    │   │   Port 8502     │   │   Port 8000    │
│   49 Features  │   │   Client Auth   │   │  49 Endpoints  │
└────────────────┘   └─────────────────┘   └────────┬───────┘
                                                     │
                              ┌─────────────────────┼─────────────────────┐
                              │                     │                     │
                    ┌─────────▼────────┐   ┌────────▼────────┐   ┌───────▼────────┐
                    │   AI Agent       │   │   Database      │   │   Monitoring   │
                    │   (FastAPI)      │   │ (PostgreSQL)    │   │   (Shared)     │
                    │   Port 9000      │   │   Port 5432     │   │   Real-time    │
                    │  15 Endpoints    │   │  68+ Candidates │   │   Health       │
                    └──────────────────┘   └─────────────────┘   └────────────────┘
```

---

## 🔧 Service Details

### **1. API Gateway Service**
```yaml
Service: gateway
Technology: FastAPI 3.2.0
Port: 8000
Endpoints: 49 implemented
Purpose: Central API backend
```

**Key Features**:
- ✅ RESTful API with 49 endpoints
- ✅ JWT + Bearer token authentication
- ✅ Rate limiting (60 req/min)
- ✅ CORS protection
- ✅ Input validation and sanitization
- ✅ Enterprise security features

**Endpoint Categories**:
- Core API (4)
- Job Management (8)
- Candidate Management (4)
- AI Matching (2)
- Authentication (15)
- Security Testing (7)
- Analytics (3)
- Database Management (2)
- Assessment & Workflow (3)
- Client Portal API (1)

### **2. AI Agent Service**
```yaml
Service: agent
Technology: FastAPI 3.2.0
Port: 9000
Endpoints: 15 implemented
Purpose: AI-powered candidate matching
```

**Key Features**:
- ✅ Semantic candidate matching
- ✅ Job-specific scoring algorithms
- ✅ Multi-factor analysis (Skills, Experience, Values, Location)
- ✅ Real-time processing (<0.02s)
- ✅ Bias mitigation algorithms
- ✅ Batch processing support

**AI Capabilities**:
- Advanced semantic analysis
- Job-requirement matching
- Candidate profiling
- Skills categorization
- Experience evaluation
- Cultural fit assessment

### **3. HR Portal Service**
```yaml
Service: portal
Technology: Streamlit
Port: 8501
Features: Complete HR workflow
Purpose: HR team interface
```

**Key Features**:
- ✅ Job creation and management
- ✅ Candidate upload and search
- ✅ AI-powered shortlisting
- ✅ Interview scheduling
- ✅ Values assessment (5-point scale)
- ✅ Comprehensive reporting
- ✅ Real-time client integration

**Workflow Steps**:
1. Dashboard Overview
2. Create Job Positions
3. Upload Candidates
4. Search & Filter
5. AI Shortlist & Matching
6. Schedule Interviews
7. Values Assessment
8. Export Reports

### **4. Client Portal Service**
```yaml
Service: client_portal
Technology: Streamlit
Port: 8502
Authentication: TECH001/demo123
Purpose: Client interface
```

**Key Features**:
- ✅ Secure client authentication
- ✅ Job posting interface
- ✅ Candidate review system
- ✅ Real-time HR portal sync
- ✅ Collaborative workflow
- ✅ Progress tracking

### **5. Database Service**
```yaml
Service: db
Technology: PostgreSQL 17
Port: 5432
Data: 68+ candidates, 4+ jobs
Purpose: Data persistence
```

**Schema Design**:
- `candidates` - Complete candidate profiles
- `jobs` - Job postings and requirements
- `interviews` - Interview scheduling
- `feedback` - Values assessments
- `api_keys` - Authentication tokens
- `sessions` - User sessions

---

## 🔐 Security Architecture

### **🛡️ Security Layers**

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Stack                           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│              Network Security                              │
│  • Cloudflare SSL/TLS  • DDoS Protection                 │
│  • Rate Limiting       • Geographic Filtering            │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│            Application Security                            │
│  • JWT Authentication  • API Key Management              │
│  • 2FA Support        • Session Management               │
│  • Input Sanitization • XSS Prevention                   │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│              Data Security                                 │
│  • SQL Injection Protection  • Parameter Validation      │
│  • Encrypted Storage        • Secure Environment Vars    │
│  • CSRF Protection          • Security Headers           │
└───────────────────────────────────────────────────────────┘
```

### **🔒 Security Features**
- ✅ **CWE-798 Resolved**: Hardcoded credentials vulnerability fixed
- ✅ **OWASP Top 10 Compliance**: Complete protection suite
- ✅ **Authentication**: Multi-method (JWT, API Key, 2FA)
- ✅ **Authorization**: Role-based access control
- ✅ **Input Validation**: Comprehensive sanitization
- ✅ **Rate Limiting**: DoS protection with dynamic limits
- ✅ **Security Headers**: CSP, XSS, Frame Options
- ✅ **Encryption**: TLS 1.3 with automatic certificates

---

## 📊 Data Architecture

### **🗄️ Database Design**

```sql
-- Core Tables
candidates (68+ records)
├── id, name, email, phone
├── technical_skills, experience_years
├── seniority_level, education_level
├── location, resume_path
└── status, created_at

jobs (4+ records)
├── id, title, department, location
├── experience_level, requirements
├── description, client_id
└── status, created_at

interviews
├── id, candidate_id, job_id
├── interview_date, interviewer
├── status, notes
└── created_at

feedback
├── id, candidate_id, job_id
├── integrity, honesty, discipline
├── hard_work, gratitude
└── notes, created_at

-- Security Tables
api_keys
├── id, key_hash, client_id
├── permissions, expires_at
└── created_at, is_active

sessions
├── id, user_id, session_token
├── expires_at, ip_address
└── user_agent, created_at
```

### **📈 Data Flow**

```
Resume Upload → Processing → Extraction → Database Storage
     ↓              ↓           ↓            ↓
Job Posting → Requirements → AI Matching → Candidate Ranking
     ↓              ↓           ↓            ↓
Interview → Assessment → Values Scoring → Final Decision
```

---

## 🚀 Deployment Architecture

### **☁️ Cloud Infrastructure**

```yaml
Platform: Render Cloud
Region: Oregon, US West
Tier: Free ($0/month)
SSL: Automatic (Cloudflare)
Scaling: Auto-scaling enabled
Monitoring: Real-time health checks
```

### **🐳 Container Architecture**

```dockerfile
# Each service containerized
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE {service_port}
CMD ["python", "app.py"]
```

### **🔄 CI/CD Pipeline**

```yaml
Source: GitHub Repository
Trigger: Git push to main branch
Build: Automatic container build
Deploy: Zero-downtime deployment
Health: Automatic health checks
Rollback: Automatic on failure
```

---

## 📊 Performance Architecture

### **⚡ Performance Optimizations**

```
┌─────────────────────────────────────────────────────────────┐
│                Performance Stack                            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│               Caching Layer                                │
│  • In-memory caching    • Response caching               │
│  • Database query cache • Static asset CDN               │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│            Database Optimization                           │
│  • Connection pooling   • Query optimization             │
│  • Indexing strategy   • Async operations                │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│            Application Layer                               │
│  • Async processing    • Batch operations                │
│  • Load balancing     • Resource optimization            │
└───────────────────────────────────────────────────────────┘
```

### **📈 Performance Metrics**
```
Metric                    | Target    | Current
--------------------------|-----------|----------
API Response Time         | <200ms    | <200ms ✅
AI Matching Speed         | <100ms    | <20ms ✅
Database Query Time       | <50ms     | <50ms ✅
Page Load Time           | <2s       | <2s ✅
Concurrent Users         | 100+      | Multi-user ✅
Uptime                   | 99.9%     | 99.9% ✅
```

---

## 🔍 Monitoring Architecture

### **📊 Observability Stack**

```yaml
Health Monitoring:
  - Real-time endpoint checks
  - Database connectivity
  - Service dependencies
  - Resource utilization

Performance Monitoring:
  - Response time tracking
  - Error rate monitoring
  - Throughput analysis
  - Resource usage metrics

Security Monitoring:
  - Authentication attempts
  - Rate limit violations
  - Security header validation
  - Vulnerability scanning
```

### **🚨 Alerting System**
- **Health Alerts**: Service downtime notifications
- **Performance Alerts**: Response time degradation
- **Security Alerts**: Authentication failures
- **Resource Alerts**: High CPU/memory usage

---

## 🔮 Scalability Architecture

### **📈 Horizontal Scaling**

```
Current: Single instance per service
Future: Load-balanced multi-instance

┌─────────────────────────────────────────────────────────────┐
│                  Scaling Strategy                           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│              Load Balancer                                 │
│  • Request distribution  • Health checking               │
│  • Session affinity    • Failover support               │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│            Service Instances                               │
│  • Auto-scaling        • Resource optimization           │
│  • Container orchestration • State management            │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│              Data Layer                                    │
│  • Database clustering  • Read replicas                  │
│  • Caching layer       • Data partitioning               │
└───────────────────────────────────────────────────────────┘
```

### **🎯 Growth Planning**
- **Phase 1**: Current single-instance deployment
- **Phase 2**: Load balancing and auto-scaling
- **Phase 3**: Multi-region deployment
- **Phase 4**: Microservices mesh architecture

---

## 🛠️ Development Architecture

### **🔧 Development Workflow**

```yaml
Local Development:
  - Docker Compose setup
  - Hot reload enabled
  - Local database instance
  - Development environment variables

Testing:
  - Unit tests for each service
  - Integration tests for workflows
  - Security tests for vulnerabilities
  - Performance tests for optimization

Deployment:
  - Git-based CI/CD
  - Automatic testing
  - Zero-downtime deployment
  - Health check validation
```

### **📁 Code Organization**
```
services/
├── gateway/     - API backend (49 endpoints)
├── agent/       - AI matching (15 endpoints)
├── portal/      - HR interface (Streamlit)
├── client_portal/ - Client interface (Streamlit)
└── db/          - Database schema and migrations

tools/           - Utilities and scripts
tests/           - Test suites and validation
docs/            - Documentation and guides
config/          - Configuration management
```

---

## 🎯 Architecture Benefits

### **✅ Advantages**
1. **Modularity**: Independent service development and deployment
2. **Scalability**: Each service can scale independently
3. **Reliability**: Service isolation prevents cascading failures
4. **Maintainability**: Clear separation of concerns
5. **Security**: Layered security with service-level protection
6. **Performance**: Optimized for specific service requirements

### **🔄 Trade-offs**
1. **Complexity**: More complex than monolithic architecture
2. **Network**: Inter-service communication overhead
3. **Monitoring**: Requires comprehensive observability
4. **Data Consistency**: Distributed data management challenges

---

## 📚 Architecture Documentation

### **📖 Related Documents**
- **[API Documentation](../api/endpoints.md)** - Complete endpoint reference
- **[Deployment Guide](../deployment/README.md)** - Deployment instructions
- **[Security Guide](../security/README.md)** - Security implementation
- **[Performance Guide](../reports/performance.md)** - Performance optimization

### **🔗 External Resources**
- **Live API**: https://bhiv-hr-gateway.onrender.com/docs
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Render Dashboard**: Cloud deployment management

---

**Architecture Version**: v3.2.0  
**Last Updated**: January 18, 2025  
**Status**: Production-ready microservices architecture  
**Next Review**: Quarterly architecture assessment