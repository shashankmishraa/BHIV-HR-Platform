#!/bin/bash
# BHIV HR Platform - Production Deployment Script

set -e

echo "🚀 BHIV HR Platform - Production Deployment"
echo "============================================"

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed."; exit 1; }

# Load environment variables
if [ -f config/production.env ]; then
    echo "📁 Loading production environment..."
    export $(cat config/production.env | grep -v '^#' | xargs)
else
    echo "⚠️  Production environment file not found, using defaults"
fi

# Stop existing services
echo "🛑 Stopping existing services..."
docker-compose -f docker-compose.production.yml down

# Pull latest images
echo "📥 Pulling latest images..."
docker-compose -f docker-compose.production.yml pull

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.production.yml up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Health check
echo "🏥 Performing health checks..."
./scripts/health-check.sh

# Initialize data if needed
echo "📊 Initializing data..."
if [ -f "tools/comprehensive_resume_extractor.py" ]; then
    python tools/comprehensive_resume_extractor.py
fi

if [ -f "tools/create_demo_jobs.py" ]; then
    python tools/create_demo_jobs.py
fi

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Access URLs:"
echo "   HR Portal: http://localhost:8501"
echo "   Client Portal: http://localhost:8502"
echo "   API Gateway: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 Management Commands:"
echo "   Status: docker-compose -f docker-compose.production.yml ps"
echo "   Logs: docker-compose -f docker-compose.production.yml logs"
echo "   Stop: docker-compose -f docker-compose.production.yml down"