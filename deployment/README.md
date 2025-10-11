# 🚀 BHIV HR Platform - Deployment Configuration

**Professional deployment setup for all environments**

## 📁 Directory Structure

```
deployment/
├── docker/                     # Docker configurations
│   └── docker-compose.production.yml
├── scripts/                    # Deployment scripts
│   ├── health-check.sh
│   └── unified-deploy.sh
└── render-deployment.yml       # Render platform config
```

## 🐳 Docker Deployment

### Local Development
```bash
# Start all services
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Check service health
./deployment/scripts/health-check.sh

# Stop services
docker-compose -f deployment/docker/docker-compose.production.yml down
```

### Production Deployment
```bash
# Deploy to production
./deployment/scripts/unified-deploy.sh production

# Monitor deployment
./deployment/scripts/health-check.sh --production
```

## ☁️ Cloud Deployment (Render)

### Configuration
- **Platform**: Render Cloud (Oregon, US West)
- **Config File**: `render-deployment.yml`
- **Auto-Deploy**: GitHub integration enabled
- **SSL**: Automatic HTTPS certificates

### Services
| Service | URL | Status |
|---------|-----|--------|
| Gateway | bhiv-hr-gateway-46pz.onrender.com | 🟢 Live |
| Agent | bhiv-hr-agent-m1me.onrender.com | 🟢 Live |
| HR Portal | bhiv-hr-portal-cead.onrender.com | 🟢 Live |
| Client Portal | bhiv-hr-client-portal-5g33.onrender.com | 🟢 Live |

## 🔧 Environment Configuration

### Required Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Security
API_KEY_SECRET=your_secure_api_key
JWT_SECRET=your_jwt_secret

# Services
GATEWAY_URL=http://gateway:8000
AGENT_URL=http://agent:9000
```

### Configuration Files
- **Local**: `.env`
- **Production**: Environment variables on Render
- **Staging**: `config/.env.staging`

## 📊 Health Monitoring

### Health Check Endpoints
```bash
# Gateway service
curl https://bhiv-hr-gateway-46pz.onrender.com/health

# Agent service  
curl https://bhiv-hr-agent-m1me.onrender.com/health

# Detailed health with metrics
curl https://bhiv-hr-gateway-46pz.onrender.com/health/detailed
```

### Monitoring Dashboard
- **Metrics**: `/metrics` (Prometheus format)
- **Dashboard**: `/metrics/dashboard`
- **System Health**: `/health/detailed`

## 🔄 Deployment Process

### Automated Deployment
1. **Code Push**: Push to main branch
2. **Auto-Build**: Render builds services automatically
3. **Health Check**: Automated health verification
4. **Go Live**: Services become available

### Manual Deployment
1. **Prepare**: Update environment variables
2. **Build**: `docker-compose build`
3. **Deploy**: `docker-compose up -d`
4. **Verify**: Run health checks
5. **Monitor**: Check logs and metrics

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Database schema updated
- [ ] Dependencies updated
- [ ] Tests passing
- [ ] Security scan completed

### Post-Deployment
- [ ] All services healthy
- [ ] API endpoints responding
- [ ] Database connectivity verified
- [ ] Monitoring active
- [ ] Performance metrics normal

## 🚨 Troubleshooting

### Common Issues
1. **Service Not Starting**: Check environment variables
2. **Database Connection**: Verify DATABASE_URL
3. **API Errors**: Check API_KEY_SECRET
4. **Performance Issues**: Monitor resource usage

### Debug Commands
```bash
# Check service logs
docker-compose logs gateway

# Test database connection
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://bhiv-hr-gateway-46pz.onrender.com/test-candidates

# Verify API endpoints
curl https://bhiv-hr-gateway-46pz.onrender.com/docs
```

---

**Last Updated**: January 2025  
**Status**: 🟢 All Services Operational  
**Cost**: $0/month (Free tier)