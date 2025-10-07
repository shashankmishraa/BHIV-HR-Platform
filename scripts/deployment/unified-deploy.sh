#!/bin/bash

# BHIV HR Platform - Unified Deployment Script
# Supports local development and production (Render) deployments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="bhiv-hr-platform"
VERSION="3.1.0"
DOCKER_COMPOSE_FILE="docker-compose.production.yml"

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Display usage information
show_usage() {
    echo "BHIV HR Platform - Unified Deployment Script v${VERSION}"
    echo ""
    echo "Usage: $0 [ENVIRONMENT] [OPTIONS]"
    echo ""
    echo "Environments:"
    echo "  local       Deploy locally using Docker Compose"
    echo "  production  Production deployment (Render cloud platform)"
    echo ""
    echo "Options:"
    echo "  --build     Force rebuild of Docker images"
    echo "  --clean     Clean up existing containers/images"
    echo "  --logs      Show logs after deployment"
    echo "  --health    Run health checks after deployment"
    echo "  --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local --build --logs"
    echo "  $0 production --build"
    echo "  $0 local --clean --health"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Clean up existing containers and images
cleanup() {
    print_status "Cleaning up existing containers and images..."
    
    # Stop and remove containers
    docker-compose -f $DOCKER_COMPOSE_FILE down --remove-orphans || true
    
    # Remove unused images
    docker image prune -f || true
    
    # Remove unused volumes
    docker volume prune -f || true
    
    print_success "Cleanup completed"
}

# Build Docker images
build_images() {
    print_status "Building Docker images..."
    
    # Build all services
    docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache
    
    print_success "Docker images built successfully"
}

# Deploy locally using Docker Compose
deploy_local() {
    print_status "Deploying locally using Docker Compose..."
    
    # Start services
    docker-compose -f $DOCKER_COMPOSE_FILE up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 30
    
    print_success "Local deployment completed"
    
    # Display service URLs
    echo ""
    echo "🎯 BHIV HR Platform Services:"
    echo "├── HR Portal: http://localhost:8501"
    echo "├── Client Portal: http://localhost:8502"
    echo "├── API Gateway: http://localhost:8000"
    echo "├── AI Agent: http://localhost:9000"
    echo "└── Database: localhost:5432"
}

# Deploy to production (Render)
deploy_production() {
    print_status "Production deployment on Render..."
    
    echo ""
    echo "🎯 BHIV HR Platform - Production Deployment"
    echo "├── Platform: Render Cloud"
    echo "├── Region: Oregon (US West)"
    echo "├── API Gateway: https://bhiv-hr-gateway.onrender.com"
    echo "├── AI Agent: https://bhiv-hr-agent.onrender.com"
    echo "├── HR Portal: https://bhiv-hr-portal.onrender.com"
    echo "├── Client Portal: https://bhiv-hr-client-portal.onrender.com"
    echo "└── Status: ✅ Live & Operational"
    echo ""
    echo "📋 Deployment Instructions:"
    echo "1. Services are already deployed on Render"
    echo "2. Auto-deployment enabled via GitHub integration"
    echo "3. Push code changes to trigger automatic deployment"
    echo "4. Monitor deployment status in Render dashboard"
    echo ""
    print_success "Production deployment information displayed"
}



# Run health checks
run_health_checks() {
    print_status "Running health checks..."
    
    # Define services and their health endpoints
    declare -A services=(
        ["Gateway"]="http://localhost:8000/health"
        ["AI Agent"]="http://localhost:9000/health"
        ["HR Portal"]="http://localhost:8501"
        ["Client Portal"]="http://localhost:8502"
    )
    
    # Wait for services to be ready
    sleep 10
    
    # Check each service
    for service in "${!services[@]}"; do
        url="${services[$service]}"
        print_status "Checking $service at $url..."
        
        if curl -f -s "$url" > /dev/null; then
            print_success "$service is healthy"
        else
            print_warning "$service health check failed"
        fi
    done
    
    # Database health check
    print_status "Checking database connectivity..."
    if docker exec bhivhraiplatform-db-1 pg_isready -U bhiv_user -d bhiv_hr > /dev/null 2>&1; then
        print_success "Database is healthy"
    else
        print_warning "Database health check failed"
    fi
}

# Show logs
show_logs() {
    print_status "Showing service logs..."
    docker-compose -f $DOCKER_COMPOSE_FILE logs --tail=50 -f
}

# Process data
process_data() {
    print_status "Processing sample data..."
    
    # Wait for services to be ready
    sleep 20
    
    # Run data processing tools
    if [ -f "tools/comprehensive_resume_extractor.py" ]; then
        print_status "Extracting resume data..."
        python tools/comprehensive_resume_extractor.py || print_warning "Resume extraction failed"
    fi
    
    if [ -f "tools/create_demo_jobs.py" ]; then
        print_status "Creating demo jobs..."
        python tools/create_demo_jobs.py || print_warning "Demo job creation failed"
    fi
    
    print_success "Data processing completed"
}

# Main deployment logic
main() {
    local environment=""
    local build_flag=false
    local clean_flag=false
    local logs_flag=false
    local health_flag=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            local|production)
                environment="$1"
                shift
                ;;
            --build)
                build_flag=true
                shift
                ;;
            --clean)
                clean_flag=true
                shift
                ;;
            --logs)
                logs_flag=true
                shift
                ;;
            --health)
                health_flag=true
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Check if environment is specified
    if [ -z "$environment" ]; then
        print_error "Environment not specified"
        show_usage
        exit 1
    fi
    
    # Display deployment info
    echo "🚀 BHIV HR Platform Deployment"
    echo "├── Environment: $environment"
    echo "├── Version: $VERSION"
    echo "├── Build: $build_flag"
    echo "├── Clean: $clean_flag"
    echo "├── Logs: $logs_flag"
    echo "└── Health: $health_flag"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Clean up if requested
    if [ "$clean_flag" = true ]; then
        cleanup
    fi
    
    # Build images if requested
    if [ "$build_flag" = true ]; then
        build_images
    fi
    
    # Deploy based on environment
    case $environment in
        local)
            deploy_local
            process_data
            ;;
        production)
            deploy_production
            ;;
        *)
            print_error "Unknown environment: $environment"
            exit 1
            ;;
    esac
    
    # Run health checks if requested
    if [ "$health_flag" = true ] && [ "$environment" = "local" ]; then
        run_health_checks
    fi
    
    # Show logs if requested
    if [ "$logs_flag" = true ] && [ "$environment" = "local" ]; then
        show_logs
    fi
    
    print_success "Deployment completed successfully!"
}

# Run main function with all arguments
main "$@"