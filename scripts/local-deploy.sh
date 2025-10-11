#!/bin/bash
echo "BHIV HR Platform - Local Deployment"
echo "===================================="

cd "$(dirname "$0")/.."

echo "Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker."
    exit 1
fi

echo "Starting services..."
docker-compose -f deployment/docker/docker-compose.production.yml up -d

echo "Waiting for services to start..."
sleep 30

echo "Checking service health..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "Gateway: HEALTHY"
else
    echo "WARNING: Gateway service may still be starting..."
fi

if curl -s http://localhost:9000/health > /dev/null; then
    echo "Agent: HEALTHY"
else
    echo "WARNING: Agent service may still be starting..."
fi

echo ""
echo "Services started! Access URLs:"
echo "- Gateway API: http://localhost:8000/docs"
echo "- AI Agent: http://localhost:9000/docs"
echo "- HR Portal: http://localhost:8501"
echo "- Client Portal: http://localhost:8502"
echo ""
echo "To stop: docker-compose -f deployment/docker/docker-compose.production.yml down"