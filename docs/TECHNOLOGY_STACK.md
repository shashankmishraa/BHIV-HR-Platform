# 🛠️ BHIV HR Platform - Technology Stack

## 🐍 Core Runtime

### **Python 3.12.7**
- **Latest Features**: Enhanced error messages, improved performance
- **Security**: Latest CVE patches and security updates
- **Performance**: 10-15% faster execution vs 3.11
- **Memory**: Improved garbage collection and memory management
- **Compatibility**: All dependencies tested and verified

---

## 🌐 Web Frameworks

### **FastAPI 0.115.6** (Gateway & Agent Services)
- **Performance**: High-performance async API framework
- **Documentation**: Automatic OpenAPI/Swagger generation
- **Validation**: Pydantic 2.10.3 data validation
- **Security**: Built-in authentication and authorization
- **Endpoints**: 53 total (48 Gateway + 5 Agent)

### **Streamlit 1.41.1** (Portal Services)
- **UI Framework**: Rapid web app development
- **Real-time**: Live data updates and interactions
- **Components**: Rich UI components and widgets
- **Deployment**: Production-ready web applications

---

## 🗄️ Database & Storage

### **PostgreSQL 17**
- **ACID Compliance**: Full transaction support
- **Performance**: Advanced indexing and query optimization
- **Scalability**: Connection pooling (pool_size=10)
- **Security**: Row-level security and encryption
- **Data**: 31 candidates from actual resumes, 15+ jobs, 11 tables with 25+ indexes

---

## 🔗 HTTP & Networking

### **httpx 0.28.1**
- **Async Support**: Full async/await compatibility
- **HTTP/2**: Modern protocol support
- **Connection Pooling**: Efficient connection management
- **Timeout Handling**: Configurable timeout policies
- **SSL/TLS**: Secure communication

### **Uvicorn 0.32.1**
- **ASGI Server**: Lightning-fast ASGI implementation
- **Production Ready**: Enterprise-grade server
- **Auto-reload**: Development mode support
- **Performance**: Optimized for FastAPI applications

---

## 📊 Data Processing

### **Pandas 2.3.2**
- **Data Analysis**: Powerful data manipulation
- **CSV Processing**: Candidate data import/export
- **Analytics**: Statistical analysis and reporting
- **Integration**: Seamless Streamlit integration

### **NumPy 1.26.4**
- **Numerical Computing**: High-performance arrays
- **Mathematical Operations**: Advanced calculations
- **AI Support**: Foundation for machine learning
- **Performance**: Optimized C implementations

---

## 🔒 Security & Authentication

### **Pydantic 2.10.3**
- **Data Validation**: Type-safe data models
- **Serialization**: JSON serialization/deserialization
- **Error Handling**: Detailed validation errors
- **Performance**: Fast validation with Rust core

### **PyJWT 2.8.0**
- **Token Authentication**: JWT token generation/validation
- **Security**: Cryptographic signing algorithms
- **Expiration**: Token lifecycle management
- **Standards**: RFC 7519 compliance

### **bcrypt 4.1.2**
- **Password Hashing**: Secure password storage
- **Salt Generation**: Automatic salt handling
- **Adaptive**: Configurable work factors
- **Security**: Resistant to rainbow table attacks

### **pyotp 2.9.0**
- **Two-Factor Auth**: TOTP implementation
- **QR Codes**: Automatic QR code generation
- **Compatibility**: Google/Microsoft/Authy support
- **Security**: Time-based one-time passwords

---

## 📈 Monitoring & Metrics

### **Prometheus Client 0.19.0**
- **Metrics Collection**: System and business metrics
- **Time Series**: Historical data tracking
- **Alerting**: Threshold-based notifications
- **Integration**: Grafana dashboard support

### **psutil 5.9.6**
- **System Monitoring**: CPU, memory, disk usage
- **Process Management**: Service health tracking
- **Performance**: Real-time system metrics
- **Cross-platform**: Windows, Linux, macOS support

---

## 🐳 Containerization

### **Docker**
- **Base Images**: python:3.12.7-slim
- **Multi-stage Builds**: Optimized container sizes
- **Security**: Non-root user execution
- **Networking**: Internal service communication

### **Docker Compose**
- **Orchestration**: Multi-service deployment
- **Networking**: Isolated service networks
- **Volumes**: Persistent data storage
- **Environment**: Configuration management

---

## 🔧 Development Tools

### **File Processing**
- **PyPDF2 3.0.1**: PDF resume extraction
- **python-docx 0.8.11**: DOCX document processing
- **Pillow 10.1.0**: Image processing and QR codes
- **werkzeug 3.0.1**: Secure file uploads

### **Utilities**
- **python-dotenv 1.0.0**: Environment variable management
- **typing-extensions 4.10.0**: Enhanced type hints
- **pathlib**: Built-in path operations (Python 3.12.7)

---

## 🌐 Deployment Platform

### **Render Cloud**
- **Region**: Oregon, US West
- **SSL**: Automatic HTTPS certificates
- **Auto-deploy**: GitHub integration
- **Scaling**: Automatic scaling
- **Cost**: $0/month (Free tier)

### **Environment**
- **Python Runtime**: 3.12.7
- **Node.js**: Not required
- **Build**: Docker-based deployment
- **Networking**: Internal service mesh

---

## 📊 Performance Specifications

### **Response Times**
- **API Gateway**: <100ms average
- **AI Agent**: <50ms average
- **Database**: <20ms average
- **Portal Loading**: <200ms average

### **Throughput**
- **API Requests**: 60-500 req/min (tiered)
- **Concurrent Users**: Multi-user support
- **Database Connections**: 10 max pool size
- **File Processing**: 1-2 seconds per resume

### **Resource Usage**
- **Memory**: <512MB per service
- **CPU**: <30% average usage
- **Storage**: <1GB total
- **Network**: <10MB/min bandwidth

---

## 🔄 Version Compatibility

### **Python Compatibility**
- **Minimum**: Python 3.12.7
- **Recommended**: Python 3.12.7
- **Tested**: Python 3.12.7
- **Features**: All latest language features

### **Dependency Compatibility**
- ✅ All dependencies tested with Python 3.12.7
- ✅ No deprecated modules (removed pathlib2, dataclasses)
- ✅ Latest security patches applied
- ✅ Performance optimizations enabled

---

## 🚀 Deployment Architecture

```
GitHub Repository
       ↓
   Render Cloud
       ↓
┌─────────────────┐
│   Load Balancer │
└─────────────────┘
       ↓
┌─────────────────┐
│   API Gateway   │ ← FastAPI 0.115.6 + Python 3.12.7
│   (Port 8000)   │
└─────────────────┘
       ↓
┌─────────────────┐
│   AI Agent      │ ← FastAPI 0.115.6 + Python 3.12.7
│   (Port 9000)   │
└─────────────────┘
       ↓
┌─────────────────┐
│   PostgreSQL    │ ← PostgreSQL 17
│   (Port 5432)   │
└─────────────────┘
       ↑
┌─────────────────┐
│   HR Portal     │ ← Streamlit 1.41.1 + Python 3.12.7
│   (Port 8501)   │
└─────────────────┘
       ↑
┌─────────────────┐
│  Client Portal  │ ← Streamlit 1.41.1 + Python 3.12.7
│   (Port 8502)   │
└─────────────────┘
```

---

**BHIV HR Platform v3.1.0** - Built with modern Python 3.12.7 stack for enterprise performance and security.

*Last Updated: January 2025 | Python: 3.12.7 | All Services: Operational*