#!/bin/bash

# Service Recovery Script - Comprehensive service restart and health verification
set -euo pipefail

echo "🚨 BHIV HR Platform Service Recovery"
echo "===================================="

# Service configuration
declare -A SERVICES=(
    ["Gateway"]="https://bhiv-hr-gateway-46pz.onrender.com"
    ["Agent"]="https://bhiv-hr-agent-m1me.onrender.com"
    ["Portal"]="https://bhiv-hr-portal-cead.onrender.com"
    ["Client"]="https://bhiv-hr-client-portal-5g33.onrender.com"
)

declare -A DEPLOY_HOOKS=(
    ["Gateway"]="https://api.render.com/deploy/srv-d3bfsejuibrs73feao6g?key=W4WZMj1i9g0"
    ["Agent"]="https://api.render.com/deploy/srv-d3747q3uibrs738n539g?key=cto8n-Ctivw"
    ["Portal"]="https://api.render.com/deploy/srv-d3bg3igdl3ps739btv5g?key=LXdmYEdUCTU"
    ["Client"]="https://api.render.com/deploy/srv-d3bg4s56ubrc739n5ps0?key=NZPMJzMGWU0"
)

# Function to check service health
check_service_health() {
    local name="$1"
    local url="$2"
    local endpoint="${3:-/health}"
    
    echo "🔍 Checking $name health..."
    
    for attempt in {1..3}; do
        if curl -f -s --max-time 15 "$url$endpoint" >/dev/null 2>&1; then
            echo "✅ $name: Healthy"
            return 0
        else
            echo "⏳ $name: Attempt $attempt/3 failed"
            sleep 10
        fi
    done
    
    echo "❌ $name: Unhealthy"
    return 1
}

# Function to trigger service deployment
trigger_deployment() {
    local name="$1"
    local hook="$2"
    
    echo "🚀 Triggering $name deployment..."
    
    if curl -X POST -f -s --max-time 30 "$hook" >/dev/null 2>&1; then
        echo "✅ $name: Deployment triggered"
        return 0
    else
        echo "❌ $name: Deployment failed"
        return 1
    fi
}

# Function to wait for service recovery
wait_for_recovery() {
    local name="$1"
    local url="$2"
    local max_wait=300  # 5 minutes
    local wait_time=0
    
    echo "⏳ Waiting for $name recovery (max ${max_wait}s)..."
    
    while [ $wait_time -lt $max_wait ]; do
        if curl -f -s --max-time 10 "$url/health" >/dev/null 2>&1; then
            echo "✅ $name: Recovered after ${wait_time}s"
            return 0
        fi
        
        sleep 15
        wait_time=$((wait_time + 15))
        echo "⏳ $name: Still recovering... (${wait_time}s/${max_wait}s)"
    done
    
    echo "❌ $name: Recovery timeout"
    return 1
}

# Main recovery process
main() {
    echo "📊 Initial Health Assessment"
    echo "----------------------------"
    
    failed_services=()
    
    # Check all services
    for name in "${!SERVICES[@]}"; do
        url="${SERVICES[$name]}"
        if ! check_service_health "$name" "$url"; then
            failed_services+=("$name")
        fi
    done
    
    if [ ${#failed_services[@]} -eq 0 ]; then
        echo "🎉 All services are healthy!"
        return 0
    fi
    
    echo ""
    echo "🚨 Failed Services: ${failed_services[*]}"
    echo "🔄 Starting Recovery Process"
    echo "----------------------------"
    
    # Trigger deployments for failed services
    for service in "${failed_services[@]}"; do
        hook="${DEPLOY_HOOKS[$service]}"
        trigger_deployment "$service" "$hook"
        sleep 5  # Stagger deployments
    done
    
    echo ""
    echo "⏳ Waiting for deployments to complete..."
    sleep 60  # Initial wait for deployment start
    
    # Wait for recovery
    recovered_services=()
    still_failed=()
    
    for service in "${failed_services[@]}"; do
        url="${SERVICES[$service]}"
        if wait_for_recovery "$service" "$url"; then
            recovered_services+=("$service")
        else
            still_failed+=("$service")
        fi
    done
    
    echo ""
    echo "📊 Recovery Summary"
    echo "==================="
    
    if [ ${#recovered_services[@]} -gt 0 ]; then
        echo "✅ Recovered: ${recovered_services[*]}"
    fi
    
    if [ ${#still_failed[@]} -gt 0 ]; then
        echo "❌ Still Failed: ${still_failed[*]}"
        echo ""
        echo "🔧 Manual Investigation Required:"
        for service in "${still_failed[@]}"; do
            echo "   - Check $service logs in Render dashboard"
            echo "   - Verify environment variables"
            echo "   - Check resource limits"
        done
        return 1
    fi
    
    echo "🎉 All services recovered successfully!"
    
    # Final health verification
    echo ""
    echo "🔍 Final Health Verification"
    echo "----------------------------"
    
    all_healthy=true
    for name in "${!SERVICES[@]}"; do
        url="${SERVICES[$name]}"
        if ! check_service_health "$name" "$url"; then
            all_healthy=false
        fi
    done
    
    if $all_healthy; then
        echo "✅ All services verified healthy"
        return 0
    else
        echo "❌ Some services still unhealthy"
        return 1
    fi
}

# Execute main function
main "$@"