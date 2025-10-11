# 🚀 Local Deployment Guide

## Quick Start

### Windows
```cmd
scripts\local-deploy.cmd
```

### Linux/Mac
```bash
chmod +x scripts/local-deploy.sh
./scripts/local-deploy.sh
```

### Manual Deployment
```bash
# From project root
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Check status
docker-compose -f deployment/docker/docker-compose.production.yml ps

# View logs
docker-compose -f deployment/docker/docker-compose.production.yml logs -f

# Stop services
docker-compose -f deployment/docker/docker-compose.production.yml down
```

## Access URLs
- **Gateway API**: http://localhost:8000/docs
- **AI Agent**: http://localhost:9000/docs
- **HR Portal**: http://localhost:8501
- **Client Portal**: http://localhost:8502

## Environment Variables
All required variables have fallback values:
- `DB_PASSWORD`: bhiv_local_password_2025
- `API_KEY_SECRET`: prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
- `JWT_SECRET`: prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA

## Prerequisites
- Docker Desktop
- 4GB+ RAM available
- Ports 5432, 8000, 8501, 8502, 9000 available

## Troubleshooting
- Wait 2-3 minutes for all services to start
- Check `docker-compose logs` for errors
- Ensure no other services using the ports