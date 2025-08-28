# 🚀 BHIV HR Platform - Deployment Guide

## 📋 Prerequisites

### System Requirements
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository
- **Minimum RAM**: 4GB
- **Minimum Storage**: 10GB free space

### Supported Platforms
- ✅ **Windows 10/11** (with Docker Desktop)
- ✅ **macOS** (with Docker Desktop)
- ✅ **Linux** (Ubuntu 20.04+, CentOS 8+, RHEL 8+)

## 🏗️ Project Structure Overview

```
bhiv-hr-platform/
├── services/           # Microservices
│   ├── gateway/       # API Gateway (FastAPI)
│   ├── agent/         # Talah AI Agent
│   ├── portal/        # Client Portal (Streamlit)
│   └── db/            # Database initialization
├── data/              # Data files and logs
├── resume/            # Resume storage
├── scripts/           # Utility scripts
├── config/            # Configuration files
├── docs/              # Documentation
└── docker-compose.yml # Service orchestration
```

## 🚀 Quick Deployment

### 1. Clone Repository
```bash
git clone <repository-url>
cd bhiv-hr-platform
```

### 2. Environment Setup
```bash
# Copy environment template
cp config/.env.example .env

# Edit environment variables (optional)
# Default values work for local development
```

### 3. Start All Services
```bash
# Build and start all services
docker compose up --build

# Or run in background
docker compose up --build -d
```

### 4. Verify Deployment
- **🎯 Client Portal**: http://localhost:8501
- **📚 API Gateway**: http://localhost:8000/docs
- **🤖 Talah AI Agent**: http://localhost:9000/docs
- **🗄️ Database**: localhost:5432

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Database Configuration
POSTGRES_USER=bhiv_user
POSTGRES_PASSWORD=bhiv_pass
POSTGRES_DB=bhiv_hr
DATABASE_URL=postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr

# API Security
API_KEY=myverysecureapikey123

# Service URLs
AGENT_SERVICE_URL=http://agent:9000
API_BASE_URL=http://gateway:8000
```

### Port Configuration
| Service | Port | Purpose |
|---------|------|---------|
| Gateway | 8000 | API endpoints and Swagger UI |
| Portal  | 8501 | Client web interface |
| Agent   | 9000 | AI agent API |
| Database| 5432 | PostgreSQL database |

## 🔧 Development Deployment

### Local Development Setup
```bash
# Start services with live reload
docker compose up --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Individual Service Development
```bash
# Start only database
docker compose up db

# Start gateway only
docker compose up gateway

# Start specific services
docker compose up db gateway agent
```

### Database Management
```bash
# Connect to database
docker exec -it bhiv-hr-platform-db-1 psql -U bhiv_user -d bhiv_hr

# Initialize tables
python scripts/init_tables.py

# View database logs
docker compose logs db
```

## 🏭 Production Deployment

### Production Environment Variables
```env
# Use strong passwords in production
POSTGRES_PASSWORD=<strong-password>
API_KEY=<secure-api-key>

# Production database URL
DATABASE_URL=postgresql://bhiv_user:<password>@db:5432/bhiv_hr
```

### Production Docker Compose
```yaml
# docker-compose.prod.yml
services:
  gateway:
    build: ./services/gateway
    ports:
      - "80:8000"  # Map to port 80
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
    restart: always
    
  # ... other services with restart: always
```

### SSL/HTTPS Setup
```bash
# Use reverse proxy (nginx/traefik) for SSL
# Example nginx configuration:
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;  # Portal
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;  # Gateway
    }
}
```

## 🔍 Monitoring and Logs

### Service Health Checks
```bash
# Check all services
docker compose ps

# Check specific service
docker compose ps gateway

# View service logs
docker compose logs gateway
docker compose logs portal
docker compose logs agent
docker compose logs db
```

### Database Health
```bash
# Check database connection
docker exec bhiv-hr-platform-db-1 pg_isready -U bhiv_user -d bhiv_hr

# View database size
docker exec bhiv-hr-platform-db-1 psql -U bhiv_user -d bhiv_hr -c "SELECT pg_size_pretty(pg_database_size('bhiv_hr'));"
```

### API Health Checks
```bash
# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:9000/health

# Test with API key
curl -H "X-API-KEY: myverysecureapikey123" http://localhost:8000/v1/jobs
```

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # macOS/Linux
```

#### Database Connection Issues
```bash
# Check database logs
docker compose logs db

# Restart database
docker compose restart db

# Reset database
docker compose down
docker volume rm bhiv-hr-platform_db_data
docker compose up --build
```

#### Service Build Failures
```bash
# Clean build
docker compose down
docker system prune -a
docker compose up --build --no-cache
```

### Performance Optimization

#### Resource Limits
```yaml
# docker-compose.yml
services:
  gateway:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

#### Database Optimization
```sql
-- Connect to database and run
CREATE INDEX idx_candidates_job_id ON candidates(job_id);
CREATE INDEX idx_feedback_candidate_id ON feedback(candidate_id);
VACUUM ANALYZE;
```

## 📊 Data Management

### Backup and Restore
```bash
# Backup database
docker exec bhiv-hr-platform-db-1 pg_dump -U bhiv_user bhiv_hr > backup.sql

# Restore database
docker exec -i bhiv-hr-platform-db-1 psql -U bhiv_user -d bhiv_hr < backup.sql
```

### Data Migration
```bash
# Export data
python scripts/export_data.py

# Import data
python scripts/import_data.py
```

## 🔐 Security Considerations

### Production Security Checklist
- [ ] Change default passwords
- [ ] Use strong API keys
- [ ] Enable SSL/HTTPS
- [ ] Restrict database access
- [ ] Use environment variables for secrets
- [ ] Enable firewall rules
- [ ] Regular security updates

### Network Security
```yaml
# docker-compose.yml
networks:
  bhiv_network:
    driver: bridge
    internal: true  # Restrict external access
```

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.scale.yml
services:
  gateway:
    deploy:
      replicas: 3
  
  agent:
    deploy:
      replicas: 2
```

### Load Balancing
```bash
# Use nginx or traefik for load balancing
# Example with docker-compose scale
docker compose up --scale gateway=3 --scale agent=2
```

## 🎯 Success Verification

### Deployment Checklist
- [ ] All services running (`docker compose ps`)
- [ ] Database accessible
- [ ] API endpoints responding
- [ ] Portal loading correctly
- [ ] AI agent functional
- [ ] Sample data uploaded
- [ ] End-to-end workflow tested

### Test Commands
```bash
# Test complete workflow
python scripts/test_api.py

# Upload sample data
python scripts/upload_now.py

# Process resumes
python scripts/resume_processor.py
```

---

## 📞 Support

For deployment issues:
- **Documentation**: Check README.md and PROJECT_STRUCTURE.md
- **Logs**: Use `docker compose logs <service>`
- **Health**: Check service health endpoints
- **Community**: GitHub issues and discussions

---

*This deployment guide ensures reliable, secure, and scalable deployment of the BHIV HR Platform across different environments.*