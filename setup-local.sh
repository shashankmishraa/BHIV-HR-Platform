#!/bin/bash
echo "Setting up BHIV HR Platform for Local Development"
echo "================================================"

echo ""
echo "1. Copying local environment file..."
cp .env.local .env

echo ""
echo "2. Starting Docker services..."
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d --build

echo ""
echo "3. Waiting for services to start..."
sleep 30

echo ""
echo "4. Checking service health..."
curl -s http://localhost:8000/health
echo ""
curl -s http://localhost:9000/health

echo ""
echo "================================================"
echo "Local development setup complete!"
echo ""
echo "Services available at:"
echo "- Gateway API: http://localhost:8000"
echo "- AI Agent: http://localhost:9000"  
echo "- HR Portal: http://localhost:8501"
echo "- Client Portal: http://localhost:8502"
echo "- Database: localhost:5432"
echo ""
echo "To stop services: docker-compose -f docker-compose.production.yml down"
echo "================================================"