# Docker BuildKit Troubleshooting Guide

## Overview

This guide addresses Docker BuildKit socket connection failures and provides comprehensive solutions for deployment issues.

## Common BuildKit Issues

### 1. Socket Connection Failure
```
Error: failed to connect to buildkit socket (unix:///run/user/1000/buildkit/buildkitd.sock)
```

**Root Causes:**
- BuildKit daemon not running
- Socket permission issues
- User namespace conflicts
- Resource exhaustion
- Docker daemon issues

### 2. Diagnostic Steps

#### Check Docker Daemon Status
```bash
# Check if Docker is running
docker info

# Start Docker daemon (if needed)
sudo systemctl start docker
sudo systemctl enable docker
```

#### Verify BuildKit Availability
```bash
# Check BuildKit version
docker buildx version

# List builders
docker buildx ls

# Inspect current builder
docker buildx inspect
```

#### Check Socket Permissions
```bash
# Check socket existence and permissions
ls -la /run/user/$(id -u)/buildkit/buildkitd.sock

# Check user permissions
id
groups
```

## Fix Strategies

### 1. Reset BuildKit
```bash
# Remove all inactive builders
docker buildx rm --all-inactive

# Prune BuildKit cache
docker buildx prune -f

# Create new builder
docker buildx create --name bhiv-builder --driver docker-container --bootstrap
docker buildx use bhiv-builder
docker buildx inspect --bootstrap
```

### 2. Fix Socket Issues
```bash
# Stop BuildKit daemon
docker buildx stop bhiv-builder

# Remove problematic builder
docker buildx rm bhiv-builder

# Recreate with proper configuration
docker buildx create --name bhiv-builder \
  --driver docker-container \
  --driver-opt network=host \
  --bootstrap

docker buildx use bhiv-builder
```

### 3. Alternative Build Methods

#### Legacy Docker Build (Fallback)
```bash
# Disable BuildKit
export DOCKER_BUILDKIT=0

# Use traditional docker build
docker build -t bhiv-gateway:latest services/gateway/
docker build -t bhiv-agent:latest services/agent/
```

#### Multi-stage Build Optimization
```dockerfile
# Optimized Dockerfile with better caching
FROM python:3.12.7-slim as base

# Install system dependencies in separate layer
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

FROM base as dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM dependencies as application
COPY app/ ./app/
COPY shared/ ./shared/
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["sh", "-c", "cd /app && python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

## Render Deployment (Recommended)

### Why Render is Better
- **No Docker Required**: Native build system
- **Automatic Optimization**: Dependency caching and optimization
- **Security**: Isolated build environments
- **Reliability**: No BuildKit socket issues
- **Performance**: Optimized for web services

### Render Configuration
```yaml
# render.yaml
services:
  - type: web
    name: bhiv-gateway
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd services/gateway && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
    
  - type: web
    name: bhiv-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd services/agent && uvicorn app:app --host 0.0.0.0 --port $PORT
```

## Automated Fix Script

Use the provided script for automated diagnosis and fixes:

```bash
# Make script executable
chmod +x scripts/deployment/docker-buildkit-fix.sh

# Run diagnostic and fix
./scripts/deployment/docker-buildkit-fix.sh
```

## Prevention Strategies

### 1. Environment Preparation
```bash
# Ensure proper Docker installation
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install BuildKit plugin
docker buildx install
```

### 2. Resource Management
```bash
# Check available resources
df -h
free -h
docker system df

# Clean up if needed
docker system prune -a -f
docker volume prune -f
```

### 3. Configuration Optimization
```bash
# Configure Docker daemon
sudo tee /etc/docker/daemon.json <<EOF
{
  "features": {
    "buildkit": true
  },
  "experimental": false,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

sudo systemctl restart docker
```

## CI/CD Integration

### GitHub Actions Configuration
```yaml
- name: Setup BuildKit
  run: |
    # Enable BuildKit
    echo "DOCKER_BUILDKIT=1" >> $GITHUB_ENV
    echo "BUILDKIT_PROGRESS=plain" >> $GITHUB_ENV
    
    # Create builder if needed
    docker buildx create --name ci-builder --use --bootstrap || true

- name: Build with Fallback
  run: |
    # Try BuildKit first
    if docker buildx build --platform linux/amd64 -t app:latest .; then
      echo "✅ BuildKit build successful"
    else
      echo "⚠️ BuildKit failed, using fallback"
      export DOCKER_BUILDKIT=0
      docker build -t app:latest .
    fi
```

## Monitoring and Alerting

### Health Checks
```bash
# BuildKit health check
docker buildx inspect --bootstrap

# Socket availability check
test -S /run/user/$(id -u)/buildkit/buildkitd.sock && echo "Socket OK" || echo "Socket Missing"

# Resource usage monitoring
docker system df
docker stats --no-stream
```

### Automated Monitoring
```bash
#!/bin/bash
# buildkit-monitor.sh

while true; do
  if ! docker buildx inspect >/dev/null 2>&1; then
    echo "$(date): BuildKit unhealthy, attempting fix..."
    docker buildx create --name monitor-builder --use --bootstrap
  fi
  sleep 300  # Check every 5 minutes
done
```

## Troubleshooting Checklist

- [ ] Docker daemon running
- [ ] BuildKit plugin installed
- [ ] User in docker group
- [ ] Socket permissions correct
- [ ] Sufficient disk space
- [ ] No resource exhaustion
- [ ] Network connectivity
- [ ] Firewall not blocking
- [ ] SELinux/AppArmor configured
- [ ] Container runtime healthy

## Support Resources

- **Docker BuildKit Documentation**: https://docs.docker.com/buildx/
- **Render Documentation**: https://render.com/docs
- **GitHub Actions Docker**: https://docs.github.com/en/actions/publishing-packages/publishing-docker-images

## Conclusion

While Docker BuildKit issues can be complex, the BHIV HR Platform uses Render's native deployment system, eliminating most Docker-related problems. The provided tools and scripts ensure robust deployment with multiple fallback strategies.