# BHIV HR Platform - Testing Suite

## 🎯 Streamlined Testing Framework

Comprehensive testing for 73+ live endpoints across all BHIV HR Platform services.

## 📁 Test Structure
```
tests/
├── test_live_endpoints.py   # ✅ Live endpoint testing (PRIMARY)
├── test_endpoints.py        # API endpoint validation
├── test_security.py         # Security testing
├── test_config.py          # Configuration validation
├── test_complete_system.py # System integration
└── requirements.txt        # Test dependencies
```

## 🚀 Quick Testing

### Live Endpoint Testing (Recommended)
```bash
# Test all live production endpoints
python tests/test_live_endpoints.py

# Expected output:
# ✅ 73+ endpoints tested
# ✅ Response times measured
# ✅ Success rate calculated
```

### Automated CI/CD Testing
- **Comprehensive Endpoint Check**: Every 6 hours
- **Fast Health Check**: Every 30 minutes
- **Unified Pipeline**: On every push to main

## 🔍 Test Categories

### 1. Health Endpoints (7 endpoints)
- `/health`, `/health/detailed`, `/health/ready`
- `/health/live`, `/health/probe`
- Agent health and status endpoints

### 2. API Endpoints (25+ endpoints)
- Authentication: `/auth/login`, `/auth/validate`
- Candidates: `/candidates`, `/candidates/stats`
- Jobs: `/jobs`, `/jobs/stats`
- AI Matching: `/match/candidates`

### 3. System Endpoints (15+ endpoints)
- System info: `/system/modules`, `/system/architecture`
- Metrics: `/metrics`, `/metrics/json`
- Root and documentation endpoints

### 4. Integration Endpoints (6 endpoints)
- `/integration/status`
- `/integration/endpoints`
- `/integration/test-sequence`
- `/integration/module-info`

### 5. Portal Accessibility (2 services)
- HR Portal: https://bhiv-hr-portal-cead.onrender.com
- Client Portal: https://bhiv-hr-client-portal-5g33.onrender.com

## 🌐 Live Service URLs

```bash
# Production Services
GATEWAY_URL="https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL="https://bhiv-hr-agent-m1me.onrender.com"
PORTAL_URL="https://bhiv-hr-portal-cead.onrender.com"
CLIENT_PORTAL_URL="https://bhiv-hr-client-portal-5g33.onrender.com"

# API Authentication
API_KEY="prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
```

## ⚡ Performance Metrics

### Target Response Times
- Health endpoints: < 1 second
- API endpoints: < 100ms
- System endpoints: < 200ms
- Portal loading: < 3 seconds

### Success Rate Targets
- Critical endpoints: 100%
- API endpoints: > 95%
- Overall system: > 98%

## 🔄 Automated Testing Workflows

### GitHub Actions Workflows
1. **comprehensive-endpoint-check.yml**
   - Tests all 73+ endpoints
   - Performance measurement
   - Detailed reporting
   - Runs every 6 hours

2. **fast-check.yml**
   - Critical health checks only
   - 3-minute execution
   - Runs every 30 minutes

3. **unified-pipeline.yml**
   - Full CI/CD with testing
   - Quality gates
   - Deployment verification

## 📊 Test Reports

### Live Testing Output
```
🚀 BHIV HR Platform - Live Endpoint Testing
==================================================
🔍 Testing Health Endpoints...
  ✅ https://bhiv-hr-gateway-46pz.onrender.com/health (45ms)
  ✅ https://bhiv-hr-agent-m1me.onrender.com/health (32ms)

📋 COMPREHENSIVE ENDPOINT TEST REPORT
============================================
Total Endpoints Tested: 73
Successful: 73
Failed: 0
Success Rate: 100.0%
Average Response Time: 67.45ms
```

## 🛠️ Manual Testing

### Quick Health Check
```bash
# Test critical services
curl https://bhiv-hr-gateway-46pz.onrender.com/health
curl https://bhiv-hr-agent-m1me.onrender.com/health
```

### API Testing
```bash
# Test with authentication
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/candidates
```

## 🎯 Testing Best Practices

1. **Live Testing First**: Always test against production endpoints
2. **Automated Monitoring**: Use CI/CD workflows for continuous testing
3. **Performance Tracking**: Monitor response times and success rates
4. **Comprehensive Coverage**: Test all endpoint categories
5. **Regular Validation**: Automated testing every 30 minutes

## 🔧 Troubleshooting

### Common Issues
- **Timeout errors**: Check service availability
- **401 Unauthorized**: Verify API key
- **503 Service Unavailable**: Service may be starting up
- **Network errors**: Check internet connection

### Debug Commands
```bash
# Test specific endpoint
curl -v https://bhiv-hr-gateway-46pz.onrender.com/health

# Check service status
curl -I https://bhiv-hr-gateway-46pz.onrender.com/
```

---

**Status**: ✅ All 73+ endpoints tested and operational  
**Last Updated**: January 2025  
**Success Rate**: 100% (Target: >98%)  
**Avg Response Time**: <100ms (Target: <200ms)