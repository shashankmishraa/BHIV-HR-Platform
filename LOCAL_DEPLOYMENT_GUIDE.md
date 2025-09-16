# BHIV HR Platform - Local Deployment Guide

## Prerequisites
- Docker Desktop installed and running
- Docker Compose v2.0+
- 8GB+ RAM available
- Ports 5432, 8000, 8501, 8502, 9000 available

## Quick Start Commands

### 1. Start All Services
```bash
# Navigate to project directory
cd "c:\bhiv hr ai platform"

# Start all services in background
docker-compose -f docker-compose.production.yml up -d

# View logs (optional)
docker-compose -f docker-compose.production.yml logs -f
```

### 2. Check Service Status
```bash
# Check all containers
docker-compose -f docker-compose.production.yml ps

# Check specific service
docker-compose -f docker-compose.production.yml ps gateway
```

### 3. View Service Logs
```bash
# All services
docker-compose -f docker-compose.production.yml logs

# Specific service
docker-compose -f docker-compose.production.yml logs gateway
docker-compose -f docker-compose.production.yml logs db
docker-compose -f docker-compose.production.yml logs agent
```

### 4. Stop Services
```bash
# Stop all services
docker-compose -f docker-compose.production.yml down

# Stop and remove volumes (clean slate)
docker-compose -f docker-compose.production.yml down -v
```

## Service Access URLs

Once deployed locally:
- **API Gateway**: http://localhost:8000/docs
- **HR Portal**: http://localhost:8501
- **Client Portal**: http://localhost:8502
- **AI Agent**: http://localhost:9000/docs
- **Database**: localhost:5432

## Test Credentials
- **Client ID**: TECH001
- **Password**: demo123
- **API Key**: myverysecureapikey123

## Deployment Steps

### Step 1: Environment Setup
```bash
# Ensure .env file exists with correct values
cat .env
```

### Step 2: Build and Start
```bash
# Build images and start services
docker-compose -f docker-compose.production.yml up --build -d

# Wait for services to be healthy (2-3 minutes)
docker-compose -f docker-compose.production.yml ps
```

### Step 3: Verify Database
```bash
# Check database is running
docker-compose -f docker-compose.production.yml exec db psql -U bhiv_user -d bhiv_hr -c "SELECT COUNT(*) FROM clients;"

# Should return: count = 3 (sample clients)
```

### Step 4: Test API Gateway
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test database connectivity
curl -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/test-db
```

### Step 5: Test Client Authentication
```bash
# Test client login
curl -X POST http://localhost:8000/v1/client/login \
  -H "Content-Type: application/json" \
  -d '{"client_id": "TECH001", "password": "demo123"}'
```

## Troubleshooting

### Common Issues

#### Docker Desktop 500 Error
```bash
# Error: request returned 500 Internal Server Error for API route

# Root cause: Docker Desktop API compatibility issue
# Fix: Restart Docker Desktop completely
# 1. Close Docker Desktop from system tray
# 2. Wait 10 seconds
# 3. Restart Docker Desktop
# 4. Wait for green status icon
# 5. Then run:
docker-compose -f docker-compose.production.yml up --build -d
```

#### Port Conflicts
```bash
# Check what's using ports
netstat -an | findstr :8000
netstat -an | findstr :5432

# Kill processes if needed
taskkill /F /PID <process_id>
```

#### Database Connection Issues
```bash
# Restart database service
docker-compose -f docker-compose.production.yml restart db

# Check database logs
docker-compose -f docker-compose.production.yml logs db
```

#### Service Build Failures
```bash
# Clean rebuild
docker-compose -f docker-compose.production.yml down
docker system prune -f
docker-compose -f docker-compose.production.yml up --build -d
```

### Health Check Commands
```bash
# Gateway health
curl http://localhost:8000/health

# Agent health  
curl http://localhost:9000/health

# Database test
curl -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/test-candidates
```

## Development Workflow

### Making Changes
```bash
# After code changes, rebuild specific service
docker-compose -f docker-compose.production.yml up --build gateway -d

# Or rebuild all
docker-compose -f docker-compose.production.yml up --build -d
```

### Viewing Real-time Logs
```bash
# Follow logs for all services
docker-compose -f docker-compose.production.yml logs -f

# Follow specific service
docker-compose -f docker-compose.production.yml logs -f gateway
```

### Database Operations
```bash
# Connect to database
docker-compose -f docker-compose.production.yml exec db psql -U bhiv_user -d bhiv_hr

# Backup database
docker-compose -f docker-compose.production.yml exec db pg_dump -U bhiv_user bhiv_hr > backup.sql

# Restore database
docker-compose -f docker-compose.production.yml exec -T db psql -U bhiv_user -d bhiv_hr < backup.sql
```

## Performance Monitoring

### Resource Usage
```bash
# Check container resource usage
docker stats

# Check specific container
docker stats bhiv-hr-ai-platform-gateway-1
```

### Service Metrics
```bash
# Gateway metrics (Prometheus format)
curl http://localhost:8000/metrics

# Detailed health check
curl http://localhost:8000/health/detailed
```

## Production Readiness Checklist

- [ ] All services start successfully
- [ ] Database connectivity confirmed
- [ ] Client authentication working (TECH001/demo123)
- [ ] API endpoints responding
- [ ] HR Portal accessible (localhost:8501)
- [ ] Client Portal accessible (localhost:8502)
- [ ] No error logs in services
- [ ] Health checks passing

## Next Steps After Local Success

1. **Commit changes to Git**
2. **Push to GitHub repository**
3. **Deploy to Render platform**
4. **Update production environment variables**
5. **Test production deployment**

## Quick Test Script
```bash
# Save as test_deployment.bat
@echo off
echo Testing BHIV HR Platform Local Deployment...
echo.

echo 1. Testing Gateway Health...
curl -s http://localhost:8000/health
echo.

echo 2. Testing Database...
curl -s -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/test-db
echo.

echo 3. Testing Client Login...
curl -s -X POST http://localhost:8000/v1/client/login -H "Content-Type: application/json" -d "{\"client_id\": \"TECH001\", \"password\": \"demo123\"}"
echo.

echo 4. Testing Agent Health...
curl -s http://localhost:9000/health
echo.

echo Deployment test complete!
```