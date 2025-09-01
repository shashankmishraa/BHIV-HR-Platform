# BHIV HR Platform - Deployment Guide

## 🚀 Production Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### Quick Deployment
```bash
# 1. Clone repository
git clone <repository-url>
cd bhiv-hr-platform

# 2. Run deployment script
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# 3. Verify deployment
./scripts/health-check.sh
```

### Manual Deployment
```bash
# 1. Load environment
export $(cat config/production.env | grep -v '^#' | xargs)

# 2. Start services
docker-compose -f docker-compose.production.yml up -d

# 3. Initialize data
python tools/comprehensive_resume_extractor.py
python tools/create_demo_jobs.py

# 4. Test endpoints
python tests/test_endpoints.py
```

## 🔧 Configuration

### Environment Variables
Edit `config/production.env`:
```bash
# Database
DB_PASSWORD=your_secure_password
POSTGRES_PASSWORD=your_secure_password

# API Security
API_KEY_SECRET=your_secure_api_key
CLIENT_ACCESS_CODE=your_client_code

# Performance
MAX_CANDIDATES_PER_REQUEST=50
AI_MATCHING_TIMEOUT=15
```

### Service Ports
- **Gateway API**: 8000
- **Agent API**: 9000
- **HR Portal**: 8501
- **Client Portal**: 8502
- **Database**: 5432

## 🏥 Health Monitoring

### Health Check Endpoints
```bash
# Service health
curl http://localhost:8000/health
curl http://localhost:9000/health

# Database health
docker exec bhivhraiplatform-db-1 pg_isready

# Full health check
./scripts/health-check.sh
```

### Monitoring Commands
```bash
# Service status
docker-compose -f docker-compose.production.yml ps

# Service logs
docker-compose -f docker-compose.production.yml logs [service]

# Resource usage
docker stats
```

## 🔄 Data Management

### Resume Processing
```bash
# Add resumes to resume/ folder
cp *.pdf resume/

# Process automatically (if auto-sync enabled)
python tools/auto_sync_watcher.py

# Process manually
python tools/comprehensive_resume_extractor.py
python tools/database_sync_manager.py
```

### Database Backup
```bash
# Backup database
docker exec bhivhraiplatform-db-1 pg_dump -U bhiv_user bhiv_hr > backup.sql

# Restore database
docker exec -i bhivhraiplatform-db-1 psql -U bhiv_user bhiv_hr < backup.sql
```

## 🛠️ Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check Docker daemon
systemctl status docker

# Check ports
netstat -tulpn | grep :8000

# Restart services
docker-compose -f docker-compose.production.yml restart
```

**Database connection issues:**
```bash
# Check database logs
docker-compose -f docker-compose.production.yml logs db

# Reset database
docker-compose -f docker-compose.production.yml down -v
docker-compose -f docker-compose.production.yml up -d
```

**API authentication errors:**
```bash
# Verify API key
curl -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/health

# Check environment variables
docker-compose -f docker-compose.production.yml exec gateway env | grep API
```

### Performance Optimization

**Database tuning:**
```sql
-- Increase connection pool
ALTER SYSTEM SET max_connections = 200;

-- Optimize queries
CREATE INDEX idx_candidates_skills ON candidates USING gin(to_tsvector('english', technical_skills));
```

**Container resources:**
```yaml
# docker-compose.production.yml
services:
  gateway:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

## 🌐 Cloud Deployment

### AWS Deployment
```bash
# EC2 instance requirements
# - t3.medium or larger
# - 20GB EBS volume
# - Security groups: 8000, 8501, 8502

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

# Deploy platform
git clone <repository-url>
cd bhiv-hr-platform
./scripts/deploy.sh
```

### Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.production.yml bhiv-hr

# Scale services
docker service scale bhiv-hr_gateway=3
```

## 📊 Production Checklist

### Pre-deployment
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Backup strategy implemented
- [ ] Monitoring setup

### Post-deployment
- [ ] Health checks passing
- [ ] API endpoints responding
- [ ] Resume processing working
- [ ] Database populated
- [ ] User access verified

### Security
- [ ] API keys rotated
- [ ] Database passwords changed
- [ ] CORS origins restricted
- [ ] HTTPS enabled
- [ ] Access logs configured