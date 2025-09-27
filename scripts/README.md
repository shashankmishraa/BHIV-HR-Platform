# BHIV HR Platform - Scripts & Automation v4.1.0

**Updated**: January 18, 2025 | **Python**: 3.12.7 | **Status**: ✅ Production Ready

## 🛠️ Script Categories

### **Deployment Scripts**
- **quick_deploy.py** - Local deployment automation
- **comprehensive_service_verification.py** - Service health validation
- **verify_observability.py** - Monitoring system verification

### **Database Scripts**
- **create_database_schema.sql** - Database schema creation
- **validate_imports.py** - Import validation and testing

### **Monitoring Scripts**
- **check_docker_logs.py** - Docker container log analysis
- **verify_endpoints.py** - API endpoint validation
- **verify_endpoints_fixed.py** - Enhanced endpoint testing

## 🚀 Quick Start

### **Service Verification**
```bash
# Verify all services are operational
python scripts/comprehensive_service_verification.py

# Check specific service health
python scripts/verify_endpoints.py

# Validate observability framework
python scripts/verify_observability.py
```

### **Deployment Automation**
```bash
# Quick local deployment
python scripts/quick_deploy.py

# Verify deployment success
python scripts/comprehensive_service_verification.py
```

## 📊 Current Production Services

### **Live Service URLs** (Updated January 18, 2025)
- **Gateway**: https://bhiv-hr-gateway-901a.onrender.com
- **AI Agent**: https://bhiv-hr-agent-o6nx.onrender.com
- **HR Portal**: https://bhiv-hr-portal-xk2k.onrender.com
- **Client Portal**: https://bhiv-hr-client-portal-zdbt.onrender.com

### **Service Status**
- **All Services**: ✅ Operational
- **Database**: ✅ Connected (PostgreSQL 17)
- **CI/CD Pipeline**: ✅ Active
- **Monitoring**: ✅ Comprehensive observability

## 🔧 Script Usage

### **Service Verification**
```bash
# Comprehensive service check
python scripts/comprehensive_service_verification.py
# Output: Service health, response times, endpoint validation

# Endpoint validation
python scripts/verify_endpoints.py
# Output: API endpoint status, response codes, performance metrics

# Observability check
python scripts/verify_observability.py  
# Output: Health checks, metrics, monitoring status
```

### **Database Management**
```bash
# Create database schema
psql -f scripts/create_database_schema.sql

# Validate database imports
python scripts/validate_imports.py
# Output: Import validation, data integrity checks
```

### **Docker & Logs**
```bash
# Check Docker container logs
python scripts/check_docker_logs.py
# Output: Container status, log analysis, error detection
```

## 📈 Performance Monitoring

### **Current Benchmarks** (January 18, 2025)
- **API Response Time**: <100ms average (Gateway)
- **AI Matching Speed**: <0.02s per candidate (Agent)
- **Database Query Time**: <50ms average
- **Service Uptime**: 99.9% target with monitoring
- **Concurrent Users**: 50+ simultaneous users supported

### **Monitoring Commands**
```bash
# Real-time service monitoring
python scripts/comprehensive_service_verification.py --monitor

# Performance benchmarking
python scripts/verify_endpoints.py --benchmark

# Health check automation
python scripts/verify_observability.py --continuous
```

## 🔒 Security & Validation

### **Security Scripts**
- **validate_imports.py** - Secure import validation
- **verify_endpoints.py** - API security testing
- **comprehensive_service_verification.py** - Security health checks

### **Validation Features**
- **Input Sanitization**: Secure data processing
- **Authentication Testing**: API key and JWT validation
- **Rate Limit Testing**: Throttling and abuse prevention
- **Error Handling**: Comprehensive error validation

## 🚨 Troubleshooting

### **Common Issues**
1. **Service Unavailable**: Check service URLs and network connectivity
2. **Authentication Errors**: Verify API keys and credentials
3. **Database Connection**: Validate database URL and credentials
4. **Performance Issues**: Run performance benchmarks

### **Debug Commands**
```bash
# Debug service connectivity
python scripts/verify_endpoints.py --debug

# Analyze service logs
python scripts/check_docker_logs.py --analyze

# Comprehensive system check
python scripts/comprehensive_service_verification.py --verbose
```

## 📋 Script Development

### **Adding New Scripts**
1. **Follow naming convention**: `[category]_[purpose].py`
2. **Include documentation**: Clear script purpose and usage
3. **Add error handling**: Comprehensive exception management
4. **Implement logging**: Structured logging for debugging
5. **Add to README**: Update documentation with new scripts

### **Best Practices**
- **Use environment variables**: Secure configuration management
- **Implement retry logic**: Handle transient failures
- **Add progress indicators**: User-friendly feedback
- **Include validation**: Input and output validation
- **Document parameters**: Clear parameter descriptions

## 🔄 Automation Integration

### **CI/CD Integration**
- **GitHub Actions**: Automated script execution
- **Health Monitoring**: Continuous service validation
- **Deployment Verification**: Post-deployment validation
- **Performance Tracking**: Automated benchmarking

### **Scheduled Tasks**
- **Health Checks**: Every 30 minutes via GitHub Actions
- **Performance Monitoring**: Daily benchmarking
- **Security Scans**: Weekly vulnerability checks
- **Database Maintenance**: Monthly optimization

## 📞 Support

### **Script Issues**
1. **Check logs**: Review script output and error messages
2. **Verify environment**: Ensure correct configuration
3. **Update dependencies**: Keep libraries current
4. **Review documentation**: Check usage examples

### **Contributing Scripts**
1. **Follow conventions**: Use established patterns
2. **Add comprehensive tests**: Validate script functionality
3. **Document thoroughly**: Clear usage and examples
4. **Include error handling**: Robust error management

---

**Last Updated**: January 18, 2025  
**Python Version**: 3.12.7  
**Status**: ✅ All scripts operational with current service URLs  
**Quality**: Enterprise-grade automation and monitoring