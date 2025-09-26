#!/bin/bash

# Docker BuildKit Fix Script
# Addresses BuildKit socket connection failures and provides fallback strategies

set -euo pipefail

echo "🔧 Docker BuildKit Diagnostic & Fix Script"
echo "=========================================="

# Function to check Docker daemon status
check_docker_daemon() {
    echo "📋 Checking Docker daemon status..."
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Docker daemon not running"
        echo "💡 Starting Docker daemon..."
        sudo systemctl start docker || {
            echo "❌ Failed to start Docker daemon"
            return 1
        }
    fi
    echo "✅ Docker daemon is running"
}

# Function to check BuildKit availability
check_buildkit() {
    echo "📋 Checking BuildKit availability..."
    if docker buildx version >/dev/null 2>&1; then
        echo "✅ BuildKit is available"
        docker buildx ls
        return 0
    else
        echo "❌ BuildKit not available"
        return 1
    fi
}

# Function to fix BuildKit socket issues
fix_buildkit_socket() {
    echo "🔧 Fixing BuildKit socket issues..."
    
    # Check socket permissions
    BUILDKIT_SOCKET="/run/user/$(id -u)/buildkit/buildkitd.sock"
    if [ -S "$BUILDKIT_SOCKET" ]; then
        echo "📁 BuildKit socket exists: $BUILDKIT_SOCKET"
        ls -la "$BUILDKIT_SOCKET"
    else
        echo "❌ BuildKit socket not found: $BUILDKIT_SOCKET"
    fi
    
    # Reset BuildKit
    echo "🔄 Resetting BuildKit..."
    docker buildx rm --all-inactive || true
    docker buildx prune -f || true
    
    # Create new builder
    echo "🏗️ Creating new BuildKit builder..."
    docker buildx create --name bhiv-builder --driver docker-container --bootstrap
    docker buildx use bhiv-builder
    docker buildx inspect --bootstrap
}

# Function to test builds
test_builds() {
    echo "🧪 Testing Docker builds..."
    
    # Test Gateway build
    echo "📦 Testing Gateway build..."
    cd services/gateway
    if docker buildx build --platform linux/amd64 -t bhiv-gateway:test --load .; then
        echo "✅ Gateway build successful"
    else
        echo "❌ Gateway build failed"
        return 1
    fi
    
    # Test Agent build
    echo "📦 Testing Agent build..."
    cd ../agent
    if docker buildx build --platform linux/amd64 -t bhiv-agent:test --load .; then
        echo "✅ Agent build successful"
    else
        echo "❌ Agent build failed"
        return 1
    fi
    
    cd ../..
}

# Function to use fallback build strategy
fallback_build() {
    echo "🔄 Using fallback build strategy (legacy Docker)..."
    
    # Disable BuildKit
    export DOCKER_BUILDKIT=0
    
    # Build Gateway
    echo "📦 Building Gateway (legacy)..."
    cd services/gateway
    docker build -t bhiv-gateway:fallback .
    
    # Build Agent
    echo "📦 Building Agent (legacy)..."
    cd ../agent
    docker build -t bhiv-agent:fallback .
    
    cd ../..
    echo "✅ Fallback builds completed"
}

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    docker buildx rm bhiv-builder || true
    docker system prune -f || true
    echo "✅ Cleanup completed"
}

# Main execution
main() {
    echo "🚀 Starting BuildKit fix process..."
    
    # Check prerequisites
    check_docker_daemon || {
        echo "❌ Cannot proceed without Docker daemon"
        exit 1
    }
    
    # Try to fix BuildKit issues
    if check_buildkit; then
        echo "✅ BuildKit working, testing builds..."
        if test_builds; then
            echo "🎉 All builds successful with BuildKit"
            cleanup
            return 0
        else
            echo "⚠️ Builds failed with BuildKit, trying fixes..."
            fix_buildkit_socket
            if test_builds; then
                echo "🎉 Builds successful after BuildKit fix"
                cleanup
                return 0
            fi
        fi
    fi
    
    # Fallback to legacy Docker
    echo "🔄 BuildKit issues persist, using fallback strategy..."
    fallback_build
    
    echo "📋 BuildKit Fix Summary:"
    echo "- Docker daemon: ✅ Running"
    echo "- BuildKit: ⚠️ Issues detected, fallback used"
    echo "- Builds: ✅ Completed with fallback strategy"
    echo ""
    echo "💡 Recommendation: Use Render's native deployment (no Docker required)"
    
    cleanup
}

# Error handling
trap cleanup EXIT

# Run main function
main "$@"