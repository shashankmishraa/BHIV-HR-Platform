# 🏗️ BHIV HR Platform - System Architecture

## 📋 Architecture Overview

**BHIV HR Platform** is a microservices-based AI-powered recruiting platform designed for enterprise-scale deployment with comprehensive security, monitoring, and scalability features.

---

## 🎯 System Design Principles

### **Core Principles**
- **Microservices Architecture**: Independent, scalable services
- **API-First Design**: RESTful APIs with comprehensive documentation
- **Security by Design**: Enterprise-grade authentication and authorization
- **Observability**: Comprehensive monitoring, logging, and metrics
- **Scalability**: Horizontal scaling with containerized deployment

### **Technology Stack**
- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Streamlit (Multi-portal architecture)
- **Database**: PostgreSQL 17
- **Containerization**: Docker
- **Deployment**: Render Cloud Platform
- **Monitoring**: Prometheus + Custom metrics

---

## 🏛️ Service Architecture

### **Service Topology**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HR Portal     │    │  Client Portal  │    │  External APIs  │
│  (Streamlit)    │    │  (Streamlit)    │    │   (Future)      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼───────────────┐
                    │      API Gateway            │
                    │     (FastAPI 3.1.0)        │
                    │  • Authentication           │
                    │  • Rate Limiting            │
                    │  • Request Routing          │
                    │  • Monitoring               │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │      AI Agent               │
                    │     (FastAPI 2.1.0)        │
                    │  • Semantic Matching        │
                    │  • Candidate Analysis       │
                    │  • ML Model Management      │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │     PostgreSQL              │
                    │   (Database Layer)          │
                    │  • Candidate Data           │
                    │  • Job Postings             │
                    │  • Analytics                │
                    └─────────────────────────────┘
```

---

## 🔧 Service Details

### **1. API Gateway Service**
**Purpose**: Central API management and security enforcement  
**Technology**: FastAPI 3.1.0  
**Port**: 8000 (Production: Dynamic)  

**Responsibilities**:
- **Authentication & Authorization**: Bearer token + JWT validation
- **Rate Limiting**: Granular limits per endpoint and user tier
- **Request Routing**: Intelligent request distribution
- **Security Headers**: CSP, XSS protection, HSTS
- **Monitoring**: Prometheus metrics, health checks
- **API Documentation**: Interactive OpenAPI/Swagger docs

**Key Endpoints**:
```
Core API (4):           /, /health, /test-candidates, /http-methods-test
Job Management (2):     POST /v1/jobs, GET /v1/jobs
Candidate Mgmt (3):     GET /v1/candidates/*, POST /v1/candidates/bulk
AI Matching (1):        GET /v1/match/{job_id}/top
Security (15):          Rate limiting, 2FA, password management
Analytics (2):          GET /candidates/stats, /v1/reports/*
Monitoring (6):         /metrics, /health/*, /monitoring/*
```

### **2. AI Agent Service**
**Purpose**: Advanced semantic candidate matching and analysis  
**Technology**: FastAPI 2.1.0 + Custom ML Pipeline  
**Port**: 9000 (Production: Dynamic)  

**Responsibilities**:
- **Semantic Matching**: Advanced AI-powered candidate-job alignment
- **Candidate Analysis**: Detailed profile analysis and scoring
- **ML Model Management**: Model artifacts and embeddings
- **Batch Processing**: High-volume candidate processing
- **Bias Mitigation**: Fairness algorithms and bias detection

**AI Components**:
- **SemanticJobMatcher**: Core matching algorithms
- **AdvancedSemanticMatcher**: Enhanced matching with bias mitigation
- **ModelManager**: ML model lifecycle management
- **SemanticProcessor**: Text processing and feature extraction

### **3. HR Portal Service**
**Purpose**: Human Resources dashboard and management interface  
**Technology**: Streamlit 1.28.1  
**Port**: 8501 (Production: Dynamic)  

**Features**:
- **Dashboard**: Real-time analytics and metrics
- **Candidate Search**: Advanced filtering and search
- **Job Management**: Create, edit, and manage job postings
- **AI Matching**: Interactive candidate matching interface
- **Batch Upload**: Resume processing and candidate import
- **Values Assessment**: 5-point evaluation system

### **4. Client Portal Service**
**Purpose**: Enterprise client interface for job posting and candidate review  
**Technology**: Streamlit 1.28.0  
**Port**: 8502 (Production: Dynamic)  

**Features**:
- **Client Authentication**: Enterprise login system
- **Job Posting**: Client-specific job creation
- **Candidate Review**: Filtered candidate access
- **Interview Scheduling**: Integrated scheduling system
- **Reporting**: Client-specific analytics and reports

### **5. Database Service**
**Purpose**: Centralized data storage and management  
**Technology**: PostgreSQL 17  
**Port**: 5432  

**Schema Design**:
```sql
-- Core Tables
candidates          -- Candidate profiles and resumes
jobs               -- Job postings and requirements
interviews         -- Interview scheduling and status
applications       -- Candidate-job applications
clients            -- Enterprise client management

-- Analytics Tables
candidate_analytics -- Performance metrics
job_analytics      -- Job posting effectiveness
matching_history   -- AI matching audit trail
```

---

## 🔄 Data Flow Architecture

### **Request Flow**
```
1. Client Request → Load Balancer (Render)
2. Load Balancer → API Gateway
3. API Gateway → Authentication & Rate Limiting
4. API Gateway → Service Routing (Agent/Database)
5. Service Processing → Business Logic
6. Response → API Gateway → Client
```

### **AI Matching Flow**
```
1. Job Requirements → Semantic Processing
2. Candidate Pool → Feature Extraction
3. Semantic Matching → Scoring Algorithm
4. Bias Mitigation → Fairness Validation
5. Ranked Results → Response Formatting
6. Audit Logging → Analytics Storage
```

---

## 🔐 Security Architecture

### **Authentication Layers**
```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                      │
├─────────────────────────────────────────────────────────┤
│  1. Network Security (HTTPS/TLS)                        │
│  2. API Gateway Authentication (Bearer Token)           │
│  3. Service-to-Service Communication (Internal)         │
│  4. Database Access Control (Connection Pooling)        │
│  5. Application-Level Authorization (Role-Based)        │
└─────────────────────────────────────────────────────────┘
```

### **Security Features**
- **API Key Management**: Secure token-based authentication
- **2FA Support**: TOTP integration (Google/Microsoft/Authy)
- **Rate Limiting**: Dynamic limits with DoS protection
- **Input Validation**: XSS/SQL injection prevention
- **Security Headers**: Comprehensive header security
- **Audit Logging**: Complete request/response logging

---

## 📊 Monitoring & Observability

### **Monitoring Stack**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │    │    System       │    │   Business      │
│   Metrics       │    │   Metrics       │    │   Metrics       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • API Latency   │    │ • CPU Usage     │    │ • Match Quality │
│ • Error Rates   │    │ • Memory Usage  │    │ • User Activity │
│ • Request Count │    │ • Disk I/O      │    │ • Conversion    │
│ • Response Time │    │ • Network I/O   │    │ • Success Rate  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼───────────────┐
                    │    Prometheus Metrics       │
                    │      Collection             │
                    └─────────────────────────────┘
```

### **Health Check System**
- **Simple Health**: Basic service availability
- **Detailed Health**: Comprehensive system validation
- **Dependency Checks**: External service monitoring
- **Database Health**: Connection and query validation
- **AI Model Health**: Model availability and performance

---

## 🚀 Deployment Architecture

### **Container Strategy**
```
┌─────────────────────────────────────────────────────────┐
│                 Render Cloud Platform                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │   Gateway   │ │    Agent    │ │   Portal    │       │
│  │  Container  │ │  Container  │ │  Container  │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
│  ┌─────────────┐ ┌─────────────────────────────────┐   │
│  │   Client    │ │        PostgreSQL               │   │
│  │  Container  │ │       Database                  │   │
│  └─────────────┘ └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### **Build Strategy**
- **Individual Contexts**: Each service builds independently
- **Shared Dependencies**: Local copies in each service
- **Layer Caching**: Optimized Docker layer caching
- **Multi-stage Builds**: Minimal production images

---

## 📈 Scalability Considerations

### **Horizontal Scaling**
- **Stateless Services**: All services designed for horizontal scaling
- **Database Scaling**: Connection pooling and read replicas
- **Load Balancing**: Automatic load distribution
- **Auto-scaling**: Resource-based scaling triggers

### **Performance Optimization**
- **Caching Strategy**: Multi-level caching (Application + Database)
- **Connection Pooling**: Efficient database connections
- **Async Processing**: Non-blocking I/O operations
- **Batch Operations**: Optimized bulk processing

---

## 🔮 Future Architecture Enhancements

### **Planned Improvements**
- **Message Queue**: Async job processing (Redis/RabbitMQ)
- **Caching Layer**: Redis for session and data caching
- **CDN Integration**: Static asset optimization
- **Multi-region Deployment**: Geographic distribution
- **Advanced Analytics**: Real-time data pipeline

### **Technology Roadmap**
- **Kubernetes Migration**: Container orchestration
- **Service Mesh**: Advanced service communication
- **Event-Driven Architecture**: Microservices communication
- **ML Pipeline**: Automated model training and deployment

---

**Architecture Version**: 3.1.0  
**Last Updated**: January 17, 2025  
**Next Review**: Quarterly architecture review