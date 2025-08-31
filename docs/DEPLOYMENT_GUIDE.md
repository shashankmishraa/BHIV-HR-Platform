# BHIV HR Platform - Deployment Guide

## 🚀 **Quick Start (Minimal Setup)**

### **Option 1: Essential Services Only**
```bash
# Use minimal configuration (4 services)
docker-compose -f docker-compose.minimal.yml up -d

# Access points
# Portal: http://localhost:8501
# API: http://localhost:8000/docs
# AI Agent: http://localhost:9000/docs
```

### **Option 2: Full Setup**
```bash
# Use complete configuration
docker-compose up -d
```

## 📋 **Prerequisites**

### **System Requirements**
- Docker & Docker Compose
- 4GB RAM minimum
- 2GB disk space
- Ports 5432, 8000, 8501, 9000 available

### **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings (optional for development)
# DATABASE_URL, API_KEY_SECRET, etc.
```

## 🐳 **Service Architecture**

### **Minimal Setup (Recommended)**
```yaml
services:
  db:       # PostgreSQL Database (Port 5432)
  gateway:  # FastAPI Backend (Port 8000)
  agent:    # AI Matching Service (Port 9000)
  portal:   # Streamlit Frontend (Port 8501)
```

### **What's Removed from Full Setup**
- ❌ nginx (not needed for development)
- ❌ client-portal (duplicate of portal)
- ❌ Additional monitoring services

## 🔧 **Configuration Options**

### **Development (Default)**
```bash
# Quick start with defaults
docker-compose -f docker-compose.minimal.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### **Production**
```bash
# Generate secure API key
openssl rand -hex 32

# Update .env file
API_KEY_SECRET=your_generated_key_here
DATABASE_URL=postgresql://user:pass@host:5432/db

# Deploy with production settings
docker-compose -f docker-compose.minimal.yml up -d
```

## 📊 **Verification Steps**

### **1. Check Service Health**
```bash
# All services running
docker-compose ps

# Expected output:
# db       Up (healthy)
# gateway  Up
# agent    Up  
# portal   Up
```

### **2. Test API Endpoints**
```bash
# Health check
curl http://localhost:8000/health

# Statistics
curl -H "Authorization: Bearer myverysecureapikey123" \
  http://localhost:8000/candidates/stats
```

### **3. Test Portal Access**
```bash
# Open in browser
http://localhost:8501

# Should show: "BHIV HR Client Portal"
```

### **4. Run Complete Test Suite**
```bash
python test_endpoints.py
# Expected: 9/9 tests passed
```

## 📈 **Data Setup**

### **Load Sample Data**
```bash
# Process resumes (if not done)
python scripts/enhanced_resume_processor.py

# Upload candidates
python upload_csv_candidates.py

# Create demo jobs
python create_demo_jobs.py
```

### **Verify Data**
```bash
# Check database content
curl -H "Authorization: Bearer myverysecureapikey123" \
  http://localhost:8000/candidates/stats

# Expected response:
# {"total_candidates": 17, "total_jobs": 4, "total_feedback": 2}
```

## 🔒 **Security Configuration**

### **API Keys**
```bash
# Generate secure keys
openssl rand -hex 32

# Update .env
API_KEY_SECRET=your_secure_key_here
JWT_SECRET_KEY=your_jwt_key_here
```

### **Database Security**
```bash
# Change default passwords in .env
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://bhiv_user:your_secure_password@db:5432/bhiv_hr
```

### **CORS Configuration**
```bash
# Update allowed origins in .env
CORS_ORIGINS=http://localhost:8501,https://yourdomain.com
```

## 🛠️ **Troubleshooting**

### **Common Issues**

**Port Conflicts:**
```bash
# Check port usage
netstat -an | findstr "8000\|8501\|9000\|5432"

# Stop conflicting services or change ports
```

**Database Connection:**
```bash
# Check database logs
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up -d
```

**Service Dependencies:**
```bash
# Restart in correct order
docker-compose down
docker-compose up -d db
# Wait for db to be healthy
docker-compose up -d gateway agent portal
```

### **Performance Issues**
```bash
# Check resource usage
docker stats

# Increase memory if needed
# Restart services
docker-compose restart
```

## 📋 **Maintenance**

### **Updates**
```bash
# Pull latest images
docker-compose pull

# Rebuild services
docker-compose build --no-cache

# Restart
docker-compose down && docker-compose up -d
```

### **Backup**
```bash
# Backup database
docker exec bhivhraiplatform-db-1 pg_dump -U bhiv_user bhiv_hr > backup.sql

# Backup volumes
docker run --rm -v bhivhraiplatform_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/db_backup.tar.gz /data
```

### **Monitoring**
```bash
# Check service health
curl http://localhost:8000/health
curl http://localhost:9000/health

# View metrics
curl -H "Authorization: Bearer myverysecureapikey123" \
  http://localhost:8000/candidates/stats
```

## 🌐 **Access Information**

### **Development URLs**
- **Portal**: http://localhost:8501 (Main Interface)
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **AI Agent**: http://localhost:9000/docs (AI Service)
- **Database**: localhost:5432 (PostgreSQL)

### **Default Credentials**
- **API Key**: `myverysecureapikey123` (change in production)
- **Database**: `bhiv_user:bhiv_pass` (change in production)

## 🎯 **Production Deployment**

### **Cloud Deployment**
```bash
# For AWS/Azure/GCP
# 1. Update .env with production values
# 2. Use external database
# 3. Add SSL termination
# 4. Configure monitoring
```

### **SSL/HTTPS Setup**
```bash
# Add nginx reverse proxy
# Configure SSL certificates
# Update CORS origins
```

### **Scaling**
```bash
# Scale services
docker-compose up -d --scale gateway=2 --scale agent=2

# Load balancer configuration needed
```

## ✅ **Deployment Checklist**

### **Pre-Deployment**
- [ ] Docker and Docker Compose installed
- [ ] Ports 5432, 8000, 8501, 9000 available
- [ ] .env file configured
- [ ] Sufficient system resources

### **Deployment**
- [ ] Services started: `docker-compose up -d`
- [ ] All services healthy: `docker-compose ps`
- [ ] API responding: `curl http://localhost:8000/health`
- [ ] Portal accessible: http://localhost:8501

### **Post-Deployment**
- [ ] Sample data loaded
- [ ] API tests passing: `python test_endpoints.py`
- [ ] Portal functionality verified
- [ ] Security settings configured

### **Production Additional**
- [ ] Secure API keys generated
- [ ] Database passwords changed
- [ ] SSL certificates configured
- [ ] Monitoring setup
- [ ] Backup procedures in place

**The BHIV HR Platform is now ready for production use with a complete, scalable microservices architecture.**