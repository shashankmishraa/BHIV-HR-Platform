# 📚 BHIV HR Platform - Master Documentation Index

**Version**: 3.2.0 | **Updated**: January 18, 2025 | **Status**: Production Ready

## 🎯 Quick Navigation

| Category | Document | Purpose | Status |
|----------|----------|---------|--------|
| **🚀 Getting Started** | [README.md](../README.md) | Complete platform overview | ✅ Current |
| **🏗️ Architecture** | [UNIFIED_STRUCTURE.md](../UNIFIED_STRUCTURE.md) | System architecture | ✅ Current |
| **📋 Audit Report** | [COMPREHENSIVE_CODEBASE_AUDIT_2025.md](../COMPREHENSIVE_CODEBASE_AUDIT_2025.md) | Complete codebase analysis | ✅ Current |
| **🔧 Environment Setup** | [docs/ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) | Development environment | ✅ Current |

## 📖 Documentation Categories

### **🚀 Deployment & Operations**
- **[Unified Deployment Guide](UNIFIED_DEPLOYMENT_GUIDE_2025.md)** - Complete deployment instructions
- **[CI/CD Pipeline Guide](.github/workflows/README.md)** - Automated deployment workflow
- **[Environment Configuration](config/environments.yml)** - Multi-environment setup
- **[Production Configuration](config/deployment/production.yml)** - Production deployment settings

### **🔧 Development**
- **[Development Setup](ENVIRONMENT_SETUP.md)** - Local development environment
- **[API Documentation](api/COMPLETE_API_REFERENCE_2025.md)** - Complete API reference (180+ endpoints)
- **[Modular Architecture Guide](api/MODULAR_API_GUIDE.md)** - Gateway module system
- **[Testing Guide](../tests/README_E2E_TESTING.md)** - Comprehensive testing strategy

### **🔒 Security & Compliance**
- **[Security Audit](security/SECURITY_COMPLIANCE.md)** - OWASP Top 10 compliance
- **[Security Standards](../config/security/security-standards.yml)** - Security configuration
- **[Authentication System](AUTHENTICATION_SYSTEM_FIXES.md)** - Auth implementation
- **[Security Enhancements](SECURITY_ENHANCEMENTS.md)** - Security improvements

### **📊 Monitoring & Analytics**
- **[Observability Guide](COMPREHENSIVE_OBSERVABILITY_GUIDE.md)** - Complete monitoring framework
- **[Performance Benchmarks](PERFORMANCE_BENCHMARKS.md)** - System performance metrics
- **[Health Monitoring](../scripts/comprehensive_service_verification.py)** - Health check system

### **👥 User Guides**
- **[User Manual](user/USER_GUIDE.md)** - Complete user documentation
- **[Live Demo Guide](guides/LIVE_DEMO.md)** - Platform demonstration
- **[Integration Guide](INTEGRATION_GUIDE.md)** - Third-party integration

### **🤖 AI & Machine Learning**
- **[Bias Analysis](BIAS_ANALYSIS.md)** - AI bias analysis & mitigation
- **[Semantic Engine](../services/agent/semantic_engine/README.md)** - AI matching engine
- **[Model Management](../services/agent/semantic_engine/model_manager.py)** - ML model management

### **🔧 Technical References**
- **[Technical Architecture](technical/architecture.md)** - Detailed technical specs
- **[Database Schema](../services/db/)** - Complete database structure
- **[API Endpoints](api/ENDPOINT_COMPLETE_LIST.md)** - All available endpoints
- **[Workflow System](../services/gateway/app/workflow_engine.py)** - Workflow orchestration

## 🎯 Documentation Standards

### **✅ Current & Maintained**
All documents marked with ✅ are actively maintained and reflect the current system state (v3.2.0).

### **📝 Format Standards**
- **Markdown**: All documentation in GitHub-flavored Markdown
- **Structure**: Consistent heading hierarchy and formatting
- **Links**: Relative links for internal navigation
- **Status**: Clear status indicators (✅ Current, 🔄 Updating, ❌ Deprecated)

### **🔄 Update Schedule**
- **Major Updates**: With each version release
- **Minor Updates**: Monthly or as needed
- **Security Updates**: Immediately upon changes
- **Performance Updates**: Quarterly benchmarking

## 🚀 Platform Overview

### **Live Production Services**
- **API Gateway**: https://bhiv-hr-gateway-901a.onrender.com/docs
- **AI Matching Engine**: https://bhiv-hr-agent-o6nx.onrender.com/docs
- **HR Portal**: https://bhiv-hr-portal-xk2k.onrender.com/
- **Client Portal**: https://bhiv-hr-client-portal-zdbt.onrender.com/

### **System Metrics**
- **Total Endpoints**: 180+ (Gateway: 165+, Agent: 15)
- **Response Time**: <100ms average
- **Uptime**: 99.9% target
- **Cost**: $0/month (Render free tier)
- **Security**: OWASP Top 10 compliant

### **Technology Stack**
- **Backend**: FastAPI 0.109.0, Python 3.12.7
- **Frontend**: Streamlit 1.40.0
- **Database**: PostgreSQL 17
- **Deployment**: Render Cloud Platform
- **Monitoring**: Prometheus + Custom observability
- **CI/CD**: GitHub Actions unified pipeline

## 📞 Support & Resources

### **Development Support**
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Issue Tracking**: GitHub Issues
- **Documentation Updates**: Pull requests welcome

### **Production Support**
- **Health Monitoring**: Automated every 30 minutes
- **Performance Tracking**: Real-time metrics
- **Error Tracking**: Comprehensive logging
- **Deployment Status**: CI/CD pipeline notifications

---

**Last Updated**: January 18, 2025 | **Version**: v3.2.0 | **Maintainer**: BHIV Platform Team