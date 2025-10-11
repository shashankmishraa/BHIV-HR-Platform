#!/bin/bash
# BHIV HR Platform - Quick Deployment Script

echo "🚀 BHIV HR Platform - Quick Deployment"
echo "======================================"

# Navigate to project root
cd "$(dirname "$0")/../.."

# 1. Stop everything
echo "1. Stopping all services..."
docker-compose -f deployment/docker/docker-compose.production.yml down

# 2. Clean everything
echo "2. Cleaning Docker system..."
docker system prune -a --volumes --force

# 3. Rebuild and start
echo "3. Rebuilding and starting services..."
docker-compose -f deployment/docker/docker-compose.production.yml up -d --build

# 4. Wait for services to start
echo "4. Waiting for services to start..."
sleep 30

# 5. Check status
echo "5. Checking service status..."
docker ps

# 6. Health checks
echo "6. Running health checks..."
echo "Gateway Health:"
curl -s http://localhost:8000/health || echo "Gateway not ready"

echo "Agent Health:"
curl -s http://localhost:9000/health || echo "Agent not ready"

echo ""
echo "✅ Deployment completed!"
echo "Services available at:"
echo "- Gateway: http://localhost:8000"
echo "- Agent: http://localhost:9000" 
echo "- HR Portal: http://localhost:8501"
echo "- Client Portal: http://localhost:8502"