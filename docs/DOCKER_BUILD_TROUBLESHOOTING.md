# 🐳 Docker Build Troubleshooting Guide

## 🚨 Common Build Issues

### 1. **Pip Timeout Errors**

**Error**: `TimeoutError: The read operation timed out`

**Cause**: Network timeout during package download from PyPI

**Solutions**:
```dockerfile
# Increase timeout and add retries
RUN pip install --no-cache-dir --timeout 300 --retries 3 -r requirements.txt

# Alternative: Use different index
RUN pip install --no-cache-dir --index-url https://pypi.org/simple/ -r requirements.txt
```

### 2. **Build Performance Issues**

**Optimization Strategies**:
```dockerfile
# 1. Use multi-stage builds
FROM python:3.12.7-slim as builder
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12.7-slim
COPY --from=builder /root/.local /root/.local
COPY . .

# 2. Optimize layer caching
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # This layer only rebuilds when code changes
```

### 3. **Memory Issues**

**Solutions**:
```bash
# Increase Docker memory limit
docker build --memory=2g -t service-name .

# Use slim base images
FROM python:3.12.7-slim  # Instead of python:3.12.7
```

## 🔧 Quick Fixes

### **Immediate Solutions**:
```bash
# 1. Retry build with increased timeout
docker build --build-arg PIP_TIMEOUT=300 .

# 2. Use different network
docker build --network=host .

# 3. Clear Docker cache
docker system prune -a
docker builder prune
```

### **Production Build Command**:
```bash
# Optimized build with all fixes
docker build \
  --build-arg PIP_TIMEOUT=300 \
  --build-arg PIP_RETRIES=3 \
  --memory=2g \
  --no-cache \
  -t bhiv-hr-service .
```

## 📊 Build Monitoring

### **Check Build Progress**:
```bash
# Monitor build with verbose output
docker build --progress=plain -t service-name .

# Check Docker daemon logs
docker system events

# Monitor system resources
docker system df
```

### **Performance Metrics**:
- **Build Time**: Target <5 minutes per service
- **Image Size**: Target <500MB per service
- **Layer Count**: Target <10 layers per service

## 🚀 Optimized Dockerfile Pattern

```dockerfile
FROM python:3.12.7-slim

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 --retries 3 --upgrade pip && \
    pip install --no-cache-dir --timeout 300 --retries 3 -r requirements.txt

# Copy application code
COPY . .

# Set proper permissions
RUN chmod +x *.py

EXPOSE 8000
CMD ["python", "app.py"]
```

## 🔍 Debugging Commands

```bash
# Check pip configuration
pip config list

# Test package installation manually
docker run -it python:3.12.7-slim bash
pip install --timeout 300 fastapi

# Check network connectivity
docker run --rm python:3.12.7-slim ping files.pythonhosted.org

# Inspect failed build layers
docker build --rm=false .
docker run -it <failed-layer-id> bash
```

---

**Last Updated**: January 2025  
**Status**: All Dockerfiles updated with timeout handling