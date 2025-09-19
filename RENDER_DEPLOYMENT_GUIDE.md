# 🚀 Render Deployment Guide

Complete guide for deploying BHIV HR Platform on Render cloud platform.

## 🎯 Quick Deploy (5 Minutes)

### **Prerequisites**
- GitHub account with repository access
- Render account (free tier available)
- Environment variables configured

### **One-Click Deploy**
```bash
# 1. Fork/Clone Repository
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git

# 2. Connect to Render
# Visit: https://render.com/
# Connect GitHub repository

# 3. Deploy Services (Auto-detected)
# Render will auto-detect services from render.yaml
```

---

## 🏗️ Service Configuration

### **Service Architecture**
| Service | Type | Port | Build Command | Start Command |
|---------|------|------|---------------|---------------|
| **Gateway** | Web Service | 8000 | `pip install -r requirements.txt` | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| **Agent** | Web Service | 9000 | `pip install -r requirements.txt` | `uvicorn app:app --host 0.0.0.0 --port 9000` |
| **Portal** | Web Service | 8501 | `pip install -r requirements.txt` | `streamlit run app.py --server.port 8501` |
| **Client Portal** | Web Service | 8502 | `pip install -r requirements.txt` | `streamlit run app.py --server.port 8502` |
| **Database** | PostgreSQL | 5432 | N/A | Managed Service |

---

## 🔧 Environment Variables

### **Required Variables**
```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security
API_KEY=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key

# Services
GATEWAY_URL=https://bhiv-hr-gateway.onrender.com
AGENT_URL=https://bhiv-hr-agent.onrender.com
PORTAL_URL=https://bhiv-hr-portal.onrender.com
CLIENT_PORTAL_URL=https://bhiv-hr-client-portal.onrender.com

# Optional
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### **Setting Environment Variables**
1. **Render Dashboard** → Service → Environment
2. **Add each variable** from the list above
3. **Deploy** to apply changes

---

## 📋 Step-by-Step Deployment

### **Step 1: Database Setup**
```bash
# 1. Create PostgreSQL Database
# Render Dashboard → New → PostgreSQL
# Name: bhiv-hr-database
# Plan: Free (256MB)

# 2. Get Connection String
# Copy DATABASE_URL from database info
```

### **Step 2: Gateway Service**
```bash
# 1. Create Web Service
# Repository: your-repo/services/gateway
# Build Command: pip install -r requirements.txt
# Start Command: uvicorn app.main:app --host 0.0.0.0 --port 8000
# Environment: Add all variables from above
```

### **Step 3: Agent Service**
```bash
# 1. Create Web Service  
# Repository: your-repo/services/agent
# Build Command: pip install -r requirements.txt
# Start Command: uvicorn app:app --host 0.0.0.0 --port 9000
```

### **Step 4: Portal Services**
```bash
# 1. HR Portal
# Repository: your-repo/services/portal
# Start Command: streamlit run app.py --server.port 8501

# 2. Client Portal
# Repository: your-repo/services/client_portal  
# Start Command: streamlit run app.py --server.port 8502
```

---

## ✅ Verification

### **Health Checks**
```bash
# Gateway
curl https://your-gateway.onrender.com/health

# Agent
curl https://your-agent.onrender.com/health

# Portal (Browser)
https://your-portal.onrender.com/

# Client Portal (Browser)
https://your-client-portal.onrender.com/
```

### **API Testing**
```bash
# Test Authentication
curl -H "Authorization: Bearer your-api-key" \
     https://your-gateway.onrender.com/v1/jobs

# Test AI Matching
curl -X POST https://your-agent.onrender.com/match \
     -H "Content-Type: application/json" \
     -d '{"job_id": "test", "candidate_id": "test"}'
```

---

## 🔧 Troubleshooting

### **Common Issues**

#### **Build Failures**
```bash
# Issue: Dependencies not installing
# Solution: Check requirements.txt path
# Fix: Ensure requirements.txt in service root

# Issue: Python version mismatch  
# Solution: Add runtime.txt
echo "python-3.11.0" > runtime.txt
```

#### **Environment Variables**
```bash
# Issue: Variables not loading
# Solution: Check variable names (case-sensitive)
# Fix: Restart service after adding variables
```

#### **Database Connection**
```bash
# Issue: Database connection failed
# Solution: Check DATABASE_URL format
# Format: postgresql://user:pass@host:port/db
```

### **Service Logs**
```bash
# View logs in Render Dashboard
# Service → Logs → Real-time logs
# Filter by: Error, Warning, Info
```

---

## 🚀 Production Optimization

### **Performance Settings**
```bash
# Gateway Service
# Instance Type: Free (512MB RAM)
# Auto-Deploy: Enabled
# Health Check: /health

# Database
# Connection Pooling: Enabled
# Backup: Daily (Free tier)
```

### **Monitoring**
```bash
# Built-in Metrics
# CPU Usage, Memory, Response Time
# Available in Render Dashboard

# Custom Monitoring
curl https://your-gateway.onrender.com/metrics
curl https://your-gateway.onrender.com/monitoring/dashboard
```

---

## 💰 Cost Optimization

### **Free Tier Limits**
- **Web Services**: 750 hours/month (sleeps after 15min inactivity)
- **Database**: 256MB storage, 1GB transfer
- **Bandwidth**: 100GB/month
- **Build Minutes**: 500/month

### **Cost Management**
```bash
# Monitor Usage
# Render Dashboard → Billing → Usage

# Optimize Sleep Settings
# Services sleep after 15min inactivity
# Wake up on first request (~30 seconds)
```

---

## 🔒 Security Configuration

### **SSL/TLS**
- **Automatic HTTPS** - Enabled by default
- **Custom Domains** - Available on paid plans
- **Security Headers** - Configured in application

### **Access Control**
```bash
# Environment Variables (Sensitive)
# Never commit to repository
# Use Render environment settings

# API Keys
# Rotate regularly
# Use strong, unique keys
```

---

## 📊 Monitoring & Maintenance

### **Health Monitoring**
```bash
# Automated Health Checks
# Render monitors /health endpoint
# Auto-restart on failures

# Manual Monitoring
./scripts/health-check.sh production
```

### **Updates & Deployment**
```bash
# Auto-Deploy from GitHub
# Push to main branch → Auto-deploy
# Manual deploy from Render Dashboard

# Rollback
# Render Dashboard → Deployments → Rollback
```

---

## 🆘 Support

### **Render Support**
- **Documentation**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

### **Project Support**
- **GitHub Issues**: Repository issues page
- **Documentation**: docs/ folder
- **Live Demo**: https://bhiv-hr-gateway.onrender.com/docs

---

**Last Updated**: January 17, 2025 | **Status**: Production Ready | **Cost**: $0/month