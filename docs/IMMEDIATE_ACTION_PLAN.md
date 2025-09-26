# 🚨 IMMEDIATE ACTION PLAN - SERVICE CONNECTIVITY ISSUES

**BHIV HR Platform - Critical Issues Resolution**

**Date**: September 26, 2025  
**Priority**: URGENT  
**Estimated Resolution Time**: 2-4 hours  

---

## 🔥 CRITICAL ISSUES REQUIRING IMMEDIATE ACTION

### **1. AI Agent Service Down (PRODUCTION) - CRITICAL**
**Status**: 🔴 Service Unavailable (502 Bad Gateway)  
**Impact**: AI matching functionality completely unavailable  
**Business Impact**: HIGH - Core platform feature non-functional  

#### **Immediate Actions:**
```bash
# 1. Check Render deployment status
curl -I https://bhiv-hr-agent-o6nx.onrender.com/health

# 2. Check Render dashboard for service logs
# Navigate to: https://dashboard.render.com/web/srv-[service-id]/logs

# 3. Restart service if needed
# Use Render dashboard manual restart option

# 4. Verify service after restart
curl https://bhiv-hr-agent-o6nx.onrender.com/health
```

#### **Root Cause Analysis:**
- Service container may have crashed
- Memory/CPU limits exceeded
- Database connection issues
- Deployment configuration problems

---

### **2. Portal Services Health Endpoints Missing - HIGH**
**Status**: 🟡 Services running but health checks failing  
**Impact**: Monitoring and health verification not working  
**Business Impact**: MEDIUM - Services functional but not monitorable  

#### **Immediate Actions:**
1. **Add health endpoints to Streamlit applications**
2. **Standardize JSON response format**
3. **Test health endpoints locally**

#### **Code Changes Required:**

**For HR Portal (`services/portal/app.py`):**
```python
import streamlit as st
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import threading
import uvicorn

# Add FastAPI health endpoint
health_app = FastAPI()

@health_app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "service": "BHIV HR Portal",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

# Run health server in background thread
def run_health_server():
    uvicorn.run(health_app, host="0.0.0.0", port=8503)

if __name__ == "__main__":
    # Start health server
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # Start Streamlit app
    st.run()
```

**For Client Portal (`services/client_portal/app.py`):**
```python
# Similar implementation with port 8504
```

---

## 📋 STEP-BY-STEP RESOLUTION GUIDE

### **Phase 1: Immediate Fixes (0-2 hours)**

#### **Step 1: Fix AI Agent Service**
```bash
# 1. Access Render Dashboard
# URL: https://dashboard.render.com

# 2. Navigate to AI Agent service
# Service: bhiv-hr-agent-o6nx

# 3. Check recent logs for errors
# Look for: Memory issues, database connection errors, startup failures

# 4. Manual restart if needed
# Click "Manual Deploy" or "Restart Service"

# 5. Verify fix
curl https://bhiv-hr-agent-o6nx.onrender.com/health
# Expected: {"status": "healthy", "service": "BHIV AI Agent", ...}
```

#### **Step 2: Add Portal Health Endpoints**
```bash
# 1. Update portal applications locally
# Add health endpoint code (see above)

# 2. Test locally
curl http://localhost:8503/health  # HR Portal health
curl http://localhost:8504/health  # Client Portal health

# 3. Deploy to production
git add .
git commit -m "Add health endpoints to portal services"
git push origin main

# 4. Verify deployment
curl https://bhiv-hr-portal-xk2k.onrender.com/health
curl https://bhiv-hr-client-portal-zdbt.onrender.com/health
```

### **Phase 2: Verification (2-3 hours)**

#### **Step 3: Run Verification Again**
```bash
# Run comprehensive verification
python scripts/comprehensive_service_verification.py

# Expected improvements:
# - AI Agent: 502 → 200 (healthy)
# - Portal health: timeout → 200 (healthy)
# - Client Portal health: error → 200 (healthy)
# - Overall success rate: 76.5% → 95%+
```

#### **Step 4: Test Core Functionality**
```bash
# Test AI matching
curl -X POST https://bhiv-hr-agent-o6nx.onrender.com/match \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}'

# Test Gateway endpoints
curl https://bhiv-hr-gateway-901a.onrender.com/v1/jobs
curl https://bhiv-hr-gateway-901a.onrender.com/v1/candidates

# Test Portal access
# Navigate to: https://bhiv-hr-portal-xk2k.onrender.com
# Navigate to: https://bhiv-hr-client-portal-zdbt.onrender.com
```

### **Phase 3: Monitoring Setup (3-4 hours)**

#### **Step 5: Implement Monitoring**
```bash
# 1. Set up health check monitoring
# Create monitoring script for continuous health checks

# 2. Add alerting for service failures
# Configure email/Slack notifications for 502 errors

# 3. Implement service restart automation
# Auto-restart services on health check failures
```

---

## 🔧 TECHNICAL FIXES REQUIRED

### **1. AI Agent Service Configuration**
**File**: `services/agent/Dockerfile`
```dockerfile
# Ensure proper resource allocation
FROM python:3.11-slim

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:9000/health || exit 1

# Increase memory limits if needed
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
```

### **2. Portal Health Endpoints**
**Implementation**: Add FastAPI health servers to Streamlit apps

### **3. Service Discovery Configuration**
**File**: `docker-compose.production.yml`
```yaml
# Add health checks to all services
services:
  agent:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## 📊 SUCCESS METRICS

### **Before Fixes:**
- ❌ AI Agent: 502 Bad Gateway
- ❌ Portal Health: Timeout/JSON errors
- ❌ Overall Success Rate: 76.5%
- ❌ Failed Checks: 16/68

### **After Fixes (Expected):**
- ✅ AI Agent: 200 Healthy
- ✅ Portal Health: 200 Healthy
- ✅ Overall Success Rate: 95%+
- ✅ Failed Checks: <5/68

---

## 🚀 DEPLOYMENT CHECKLIST

### **Pre-Deployment:**
- [ ] Code changes tested locally
- [ ] Health endpoints responding correctly
- [ ] Database connections verified
- [ ] Environment variables configured

### **Deployment:**
- [ ] AI Agent service restarted on Render
- [ ] Portal services updated with health endpoints
- [ ] All services responding to health checks
- [ ] Cross-service integration working

### **Post-Deployment:**
- [ ] Comprehensive verification run
- [ ] All critical endpoints accessible
- [ ] Success rate >95%
- [ ] Monitoring alerts configured

---

## 📞 ESCALATION CONTACTS

### **If Issues Persist:**
1. **Check Render Service Logs**: Dashboard → Service → Logs
2. **Database Connectivity**: Verify PostgreSQL connection
3. **Resource Limits**: Check memory/CPU usage on Render
4. **Configuration**: Verify environment variables

### **Emergency Rollback:**
```bash
# If new deployment causes issues
git revert HEAD
git push origin main

# Or use Render dashboard to rollback to previous deployment
```

---

## 🎯 EXPECTED TIMELINE

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Phase 1** | 0-2 hours | Fix AI Agent, Add health endpoints |
| **Phase 2** | 2-3 hours | Verify fixes, Test functionality |
| **Phase 3** | 3-4 hours | Setup monitoring, Documentation |

**Total Estimated Time**: 4 hours  
**Priority**: URGENT - Start immediately  

---

## 📈 POST-RESOLUTION MONITORING

### **Continuous Monitoring:**
```bash
# Set up automated health checks every 5 minutes
*/5 * * * * curl -f https://bhiv-hr-agent-o6nx.onrender.com/health || echo "Agent down"
*/5 * * * * curl -f https://bhiv-hr-gateway-901a.onrender.com/health || echo "Gateway down"
*/5 * * * * curl -f https://bhiv-hr-portal-xk2k.onrender.com/health || echo "Portal down"
```

### **Success Validation:**
- All services return 200 on health checks
- AI matching functionality working
- Portal interfaces accessible
- Database connections stable
- Overall system success rate >95%

---

**Action Required**: Begin Phase 1 immediately  
**Next Review**: 4 hours after implementation  
**Success Criteria**: All services healthy, success rate >95%