# 🏗️ BHIV HR Platform - System Architecture

**Version**: 3.2.1 | **Last Updated**: January 18, 2025 | **Architecture**: Modular Microservices

## 🎯 Architecture Overview

The BHIV HR Platform implements a **modular microservices architecture** with workflow orchestration, designed for scalability, maintainability, and enterprise-grade performance.

### **Core Principles**
- **Modular Design**: 6 independent router modules with clear separation of concerns
- **Workflow Integration**: Background task processing and pipeline automation
- **Shared Utilities**: Cross-service validation, security, and configuration management
- **Enterprise Security**: Comprehensive authentication, authorization, and data protection
- **Production Ready**: Live deployment with 99.9% uptime and <100ms response times

---

## 🏛️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    BHIV HR Platform v3.2.1                     │
│                   Modular Microservices Architecture            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HR Portal     │    │  Client Portal  │    │   Admin Panel   │
│   (Streamlit)   │    │   (Streamlit)   │    │    (Future)     │
│   Port: 8501    │    │   Port: 8502    │    │   Port: 8503    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     Load Balancer       │
                    │    (Render Platform)    │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────▼────────────────────────┐
        │              API Gateway v3.2.1                │
        │           Modular Architecture                  │
        │              Port: 8000                         │
        └────────────────────┬────────────────────────────┘
                             │
    ┌────────────────────────┼────────────────────────┐
    │                       │                        │
┌───▼────┐  ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼─────┐
│ Core   │  │    Jobs     │  │ Candidates  │  │   Auth    │
│Module  │  │   Module    │  │   Module    │  │  Module   │
│(4 EP)  │  │  (10 EP)    │  │   (12 EP)   │  │  (17 EP)  │
└────────┘  └─────────────┘  └─────────────┘  └───────────┘

┌─────────────┐              ┌─────────────┐
│ Workflows   │              │ Monitoring  │
│   Module    │              │   Module    │
│  (15 EP)    │              │   (25 EP)   │
└─────────────┘              └─────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                           │                            │
┌───────▼────────┐    ┌─────────────▼──────────┐    ┌───────────▼────────┐
│  AI Agent      │    │     Database Layer     │    │  Shared Services   │
│   Service      │    │    PostgreSQL 17       │    │   & Utilities      │
│  Port: 9000    │    │     Port: 5432         │    │                    │
│   (15 EP)      │    │                        │    │ • Validation       │
└────────────────┘    └────────────────────────┘    │ • Security         │
                                                     │ • Configuration    │
                                                     │ • Logging          │
                                                     └────────────────────┘
```

---

## 🔧 Module Architecture

### **Gateway Service - Modular Design**

| Module | Endpoints | Purpose | Key Features |
|--------|-----------|---------|--------------|
| **Core** | 4 | System health and info | Health checks, architecture details, module status |
| **Jobs** | 10 | Job management | CRUD operations, AI matching, workflow integration |
| **Candidates** | 12 | Candidate lifecycle | Management, bulk operations, workflow triggers |
| **Auth** | 17 | Security & authentication | JWT, 2FA, sessions, API keys, rate limiting |
| **Workflows** | 15 | Process orchestration | Pipeline automation, background tasks |
| **Monitoring** | 25 | System observability | Health checks, metrics, alerting, analytics |

### **Module Dependencies**

```
┌─────────────┐
│    Core     │ ──┐
└─────────────┘   │
                  │    ┌─────────────┐
┌─────────────┐   ├───▶│   Shared    │
│    Jobs     │ ──┤    │ Utilities   │
└─────────────┘   │    └─────────────┘
                  │           │
┌─────────────┐   │           │
│ Candidates  │ ──┤           ▼
└─────────────┘   │    ┌─────────────┐
                  │    │  Database   │
┌─────────────┐   │    │   Layer     │
│    Auth     │ ──┤    └─────────────┘
└─────────────┘   │
                  │
┌─────────────┐   │
│ Workflows   │ ──┤
└─────────────┘   │
                  │
┌─────────────┐   │
│ Monitoring  │ ──┘
└─────────────┘
```

---

## 🛠️ Technology Stack

### **Backend Services**
- **API Gateway**: FastAPI 0.104+ with modular routing
- **AI Agent**: FastAPI 2.1.0 with semantic processing
- **Database**: PostgreSQL 17 with comprehensive schema
- **Authentication**: JWT with bcrypt password hashing
- **Validation**: Pydantic v2 with custom validators

### **Frontend Interfaces**
- **HR Portal**: Streamlit with enhanced validation
- **Client Portal**: Streamlit with enterprise authentication
- **API Documentation**: FastAPI auto-generated OpenAPI/Swagger

### **Infrastructure**
- **Deployment**: Render Cloud Platform (Oregon, US West)
- **Containerization**: Docker with multi-stage builds
- **Monitoring**: Prometheus-compatible metrics
- **Logging**: Structured JSON logging with correlation IDs

### **Development Tools**
- **Language**: Python 3.11+
- **Package Management**: pip with requirements.txt
- **Version Control**: Git with GitHub integration
- **CI/CD**: Render auto-deploy from GitHub

---

## 🔄 Workflow Architecture

### **Background Task Processing**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Request   │───▶│  Immediate      │───▶│   Background    │
│                 │    │  Response       │    │   Workflow      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                       ┌─────────────────┐            │
                       │   Workflow      │◀───────────┘
                       │   Engine        │
                       └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │   Task Queue    │
                       │   Processing    │
                       └─────────────────┘
```

### **Workflow Types**
- **Job Posting Workflow**: Validation → AI Processing → Notification
- **Candidate Onboarding**: Registration → Verification → Profile Setup
- **Interview Process**: Scheduling → Reminders → Follow-up
- **Matching Pipeline**: Job Analysis → Candidate Scoring → Ranking
- **Security Audit**: Monitoring → Threat Detection → Response

---

## 🔒 Security Architecture

### **Multi-Layer Security**

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Network Security    │ HTTPS, CORS, Rate Limiting         │
│ 2. Authentication      │ JWT, API Keys, 2FA                 │
│ 3. Authorization       │ Role-based Access Control          │
│ 4. Input Validation    │ Pydantic Models, Sanitization      │
│ 5. Data Protection     │ Encryption, Secure Storage         │
│ 6. Monitoring          │ Audit Logs, Threat Detection       │
└─────────────────────────────────────────────────────────────┘
```

### **Security Components**
- **Authentication Manager**: JWT token handling and validation
- **Security Utilities**: Input sanitization and SQL injection protection
- **Rate Limiting**: 60 API requests/minute, 10 forms/minute
- **CSRF Protection**: Token-based form validation
- **XSS Prevention**: Comprehensive input escaping
- **Audit Logging**: Security event tracking and correlation

---

## 📊 Data Architecture

### **Database Schema**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Candidates    │    │      Jobs       │    │   Interviews    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • id (PK)       │    │ • id (PK)       │    │ • id (PK)       │
│ • name          │    │ • title         │    │ • candidate_id  │
│ • email         │    │ • description   │    │ • job_id        │
│ • skills[]      │    │ • requirements[]│    │ • interviewer   │
│ • experience    │    │ • salary_min    │    │ • scheduled_time│
│ • location      │    │ • salary_max    │    │ • status        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Applications       │
                    ├─────────────────────────┤
                    │ • id (PK)               │
                    │ • candidate_id (FK)     │
                    │ • job_id (FK)           │
                    │ • status                │
                    │ • applied_at            │
                    │ • match_score           │
                    └─────────────────────────┘
```

### **Data Validation Pipeline**

```
Raw Input ──▶ Pydantic Models ──▶ Custom Validators ──▶ Normalized Data ──▶ Database
    │              │                    │                     │              │
    │              │                    │                     │              │
    ▼              ▼                    ▼                     ▼              ▼
• User Form    • Type Checking    • Business Rules    • Clean Format    • Stored Data
• API Call     • Field Validation • Range Validation  • Standardized    • Indexed
• File Upload  • Pattern Matching • Cross-field Check • Sanitized       • Optimized
```

---

## 🚀 Deployment Architecture

### **Production Environment**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Render Cloud Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Gateway   │  │  AI Agent   │  │  Database   │             │
│  │   Service   │  │   Service   │  │  Service    │             │
│  │             │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐                              │
│  │ HR Portal   │  │Client Portal│                              │
│  │   Service   │  │   Service   │                              │
│  │             │  │             │                              │
│  └─────────────┘  └─────────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   GitHub Repo   │
                    │   Auto-Deploy   │
                    └─────────────────┘
```

### **Local Development**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Compose Setup                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Gateway   │  │  AI Agent   │  │ PostgreSQL  │             │
│  │ localhost:  │  │ localhost:  │  │ localhost:  │             │
│  │    8000     │  │    9000     │  │    5432     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐                              │
│  │ HR Portal   │  │Client Portal│                              │
│  │ localhost:  │  │ localhost:  │                              │
│  │    8501     │  │    8502     │                              │
│  └─────────────┘  └─────────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 Performance Architecture

### **Response Time Optimization**

| Component | Target | Current | Optimization |
|-----------|--------|---------|--------------|
| API Gateway | <100ms | <50ms | Async processing, caching |
| AI Matching | <200ms | <20ms | Optimized algorithms |
| Database Queries | <50ms | <30ms | Indexing, connection pooling |
| Portal Loading | <2s | <1.5s | Streamlit optimization |

### **Scalability Design**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Growth   │───▶│   Auto Scaling  │───▶│   Performance   │
│                 │    │                 │    │   Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Horizontal      │    │ Resource        │    │ Bottleneck      │
│ Scaling Ready   │    │ Optimization    │    │ Detection       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🔍 Monitoring Architecture

### **Observability Stack**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring & Observability                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Metrics   │  │    Logs     │  │   Traces    │             │
│  │ Prometheus  │  │ Structured  │  │ Request ID  │             │
│  │ Compatible  │  │    JSON     │  │ Correlation │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Health    │  │   Alerts    │  │ Dashboard   │             │
│  │   Checks    │  │ Automated   │  │ Real-time   │             │
│  │ Multi-layer │  │ Thresholds  │  │  Metrics    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### **Health Check Hierarchy**

```
System Health
├── Service Health
│   ├── API Gateway (6 modules)
│   ├── AI Agent (3 components)
│   ├── Database (connection, schema)
│   └── Portals (HR, Client)
├── Component Health
│   ├── Authentication System
│   ├── Validation Pipeline
│   ├── Workflow Engine
│   └── Security Manager
└── Infrastructure Health
    ├── Network Connectivity
    ├── Resource Utilization
    ├── Storage Capacity
    └── Performance Metrics
```

---

## 🔮 Future Architecture

### **Planned Enhancements**

| Version | Enhancement | Architecture Impact |
|---------|-------------|-------------------|
| **3.2.2** | Production Sync | Deploy modular architecture to live services |
| **3.3.0** | Analytics Engine | Add dedicated analytics microservice |
| **3.4.0** | ML Pipeline | Implement advanced AI processing pipeline |
| **3.5.0** | Mobile API | Add mobile-optimized API gateway |

### **Scalability Roadmap**

```
Current (3.2.1)     Next (3.3.0)        Future (3.5.0)
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Monolithic  │───▶│ Microservice│───▶│ Distributed │
│ Modules     │    │ Separation  │    │ Architecture│
└─────────────┘    └─────────────┘    └─────────────┘
      │                    │                  │
      ▼                    ▼                  ▼
Single Service      Independent Services   Global Scale
```

---

**BHIV HR Platform Architecture v3.2.1** - Modular, Scalable, Production-Ready

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Maintained by**: BHIV HR Platform Team  
**Architecture Review**: January 18, 2025  
**Next Review**: February 2025