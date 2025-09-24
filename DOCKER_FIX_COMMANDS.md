# Docker Database Fix - Quick Commands

## 🚨 **Issue**: Missing tables (interviews, feedback) and connection pooling problems

## ⚡ **Quick Fix Commands**

### **Step 1: Stop and Clean**
```bash
cd "c:\bhiv hr ai platform"
docker-compose -f docker-compose.production.yml down -v
```

### **Step 2: Rebuild with Fixed Schema**
```bash
docker-compose -f docker-compose.production.yml up --build -d
```

### **Step 3: Wait and Test**
```bash
# Wait 30 seconds for startup
timeout 30

# Test database connection
curl http://localhost:8000/health
```

### **Step 4: Verify Tables**
```bash
# Check database health
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/v1/health

# Expected response should show all tables with counts
```

### **Step 5: Test CRUD Operations**
```bash
# Test job creation
curl -X POST \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Job","department":"Testing","location":"Remote","experience_level":"Mid-Level","requirements":"Test","description":"Test job"}' \
  http://localhost:8000/v1/jobs

# Test candidates list
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/v1/candidates

# Test interviews list  
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     http://localhost:8000/v1/interviews
```

## ✅ **Expected Results**

### **Health Check Response:**
```json
{
  "database_status": "healthy",
  "connection_status": "connected", 
  "tables": {
    "candidates": 3,
    "jobs": 3,
    "interviews": 3,
    "feedback": 3,
    "client_auth": 1
  }
}
```

### **Success Indicators:**
- ✅ All 5 services start successfully
- ✅ Database shows all 5 tables with data
- ✅ CRUD operations work
- ✅ No connection pool errors in logs

## 🔧 **If Issues Persist:**

### **Check Logs:**
```bash
docker-compose -f docker-compose.production.yml logs db
docker-compose -f docker-compose.production.yml logs gateway
```

### **Manual Database Check:**
```bash
docker exec -it bhiv-hr-platform-db-1 psql -U bhiv_user -d bhiv_hr_nqzb -c "\dt"
```

### **Reset Everything:**
```bash
docker-compose -f docker-compose.production.yml down -v
docker system prune -f
docker-compose -f docker-compose.production.yml up --build -d
```

## 📊 **Verification Script:**
```bash
python services/gateway/QUICK_SYNC_CHECK.py
```

**Expected Output:**
```
✅ Gateway: Healthy
✅ AI Agent: Healthy  
✅ HR Portal: Healthy
✅ Client Portal: Healthy
✅ Database Tests: 5/5
🎯 Overall Status: ✅ SERVICES IN SYNC
```