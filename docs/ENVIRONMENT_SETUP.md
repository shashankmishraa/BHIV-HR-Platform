# 🔧 Environment Variables Setup Guide

## 📋 Overview
Complete guide for setting up environment variables for production, staging, and development environments.

## 🚀 GitHub Repository Setup

### **1. Repository Secrets**
Go to **GitHub Settings** → **Secrets and variables** → **Actions** → **New repository secret**

#### **Production Secrets:**
```bash
JWT_SECRET
Value: prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA

API_KEY_SECRET  
Value: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

DATABASE_URL
Value: postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb
```

#### **Staging Secrets (Optional):**
```bash
STAGING_JWT_SECRET
Value: staging_jwt_secret_key_here

STAGING_API_KEY_SECRET
Value: staging_api_key_secret_here

STAGING_DATABASE_URL
Value: postgresql://staging_connection_string_here
```

### **2. Environment Variables**
Go to **GitHub Settings** → **Environments**

#### **Production Environment:**
- **Environment name**: `production`
- **Environment URL**: `https://bhiv-hr-gateway-901a.onrender.com`
- **Variables**:
  ```bash
  ENVIRONMENT = production
  PYTHON_VERSION = 3.11.11
  GATEWAY_URL = https://bhiv-hr-gateway-901a.onrender.com
  AGENT_SERVICE_URL = https://bhiv-hr-agent-o6nx.onrender.com
  ```

#### **Staging Environment:**
- **Environment name**: `staging`
- **Environment URL**: `https://staging-gateway.onrender.com`
- **Variables**:
  ```bash
  ENVIRONMENT = staging
  PYTHON_VERSION = 3.11.11
  GATEWAY_URL = https://staging-gateway.onrender.com
  AGENT_SERVICE_URL = https://staging-agent.onrender.com
  ```

## 🏗️ Render Platform Setup

### **Production Services**
Each service needs these environment variables in Render dashboard:

#### **Gateway Service:**
```bash
ENVIRONMENT = production
JWT_SECRET = prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
API_KEY_SECRET = prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
DATABASE_URL = postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb
PYTHON_VERSION = 3.11.11
```

#### **AI Agent Service:**
```bash
ENVIRONMENT = production
JWT_SECRET = prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
API_KEY_SECRET = prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
DATABASE_URL = postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb
PYTHON_VERSION = 3.11.11
```

#### **Portal Services:**
```bash
ENVIRONMENT = production
JWT_SECRET = prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
API_KEY_SECRET = prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
GATEWAY_URL = https://bhiv-hr-gateway-901a.onrender.com
AGENT_SERVICE_URL = https://bhiv-hr-agent-o6nx.onrender.com
PYTHON_VERSION = 3.11.11
```

## 💻 Local Development Setup

### **1. Environment File**
Create `.env` file in project root:
```bash
# Development Environment
ENVIRONMENT=development
PYTHON_VERSION=3.12.7

# Database
DATABASE_URL=postgresql://bhiv_user:password@localhost:5432/bhiv_hr_dev

# Security
JWT_SECRET=dev-jwt-secret-key-for-local-development
API_KEY_SECRET=dev-api-key-secret-for-local-development

# Service URLs
GATEWAY_URL=http://localhost:8000
AGENT_SERVICE_URL=http://localhost:9000
```

### **2. Docker Environment**
Update `docker-compose.production.yml`:
```yaml
environment:
  - ENVIRONMENT=development
  - DATABASE_URL=postgresql://bhiv_user:password@db:5432/bhiv_hr_dev
  - JWT_SECRET=dev-jwt-secret-key
  - API_KEY_SECRET=dev-api-key-secret
```

## 🧪 Testing Environment

### **CI/CD Pipeline**
The unified pipeline uses hardcoded test values:
```bash
ENVIRONMENT=test
JWT_SECRET=ci-test-jwt-secret-key
API_KEY_SECRET=ci-test-api-key-secret
DATABASE_URL=postgresql://test_user:test_pass@localhost:5432/test_db
```

## 🔒 Security Best Practices

### **1. Secret Management**
- ✅ **Never commit secrets** to repository
- ✅ **Use GitHub secrets** for CI/CD
- ✅ **Use Render environment variables** for production
- ✅ **Rotate secrets regularly**

### **2. Environment Separation**
- ✅ **Different secrets** for each environment
- ✅ **Environment-specific URLs**
- ✅ **Isolated databases**
- ✅ **Separate API keys**

### **3. Access Control**
- ✅ **Limit GitHub secret access**
- ✅ **Environment protection rules**
- ✅ **Required reviewers for production**
- ✅ **Audit secret usage**

## 📊 Environment Status Check

### **Verify Setup**
```bash
# Check production services
curl https://bhiv-hr-gateway-901a.onrender.com/health
curl https://bhiv-hr-agent-o6nx.onrender.com/health

# Check environment variables (in service logs)
# Should show: ENVIRONMENT=production
```

### **Troubleshooting**
1. **Service fails to start**: Check environment variables in Render dashboard
2. **Authentication errors**: Verify JWT_SECRET and API_KEY_SECRET
3. **Database connection**: Verify DATABASE_URL format
4. **CI/CD failures**: Check GitHub secrets configuration

## 🎯 Quick Setup Checklist

### **GitHub Repository:**
- [ ] Add JWT_SECRET to repository secrets
- [ ] Add API_KEY_SECRET to repository secrets  
- [ ] Add DATABASE_URL to repository secrets
- [ ] Create production environment
- [ ] Set environment variables
- [ ] Configure protection rules

### **Render Platform:**
- [ ] Set ENVIRONMENT=production for all services
- [ ] Add JWT_SECRET to all services
- [ ] Add API_KEY_SECRET to all services
- [ ] Add DATABASE_URL to backend services
- [ ] Set service URLs for portals

### **Local Development:**
- [ ] Create .env file
- [ ] Set development environment variables
- [ ] Update docker-compose configuration
- [ ] Test local services

**Environment setup complete!** 🚀