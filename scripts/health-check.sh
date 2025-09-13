#!/bin/bash
# BHIV HR Platform - Health Check Script

echo "🏥 BHIV HR Platform Health Check"
echo "================================"

# Service endpoints
GATEWAY_URL="http://localhost:8000"
AGENT_URL="http://localhost:9000"
PORTAL_URL="http://localhost:8501"
CLIENT_PORTAL_URL="http://localhost:8502"

# API Key
API_KEY="myverysecureapikey123"

# Health check function
check_service() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Checking $name... "
    
    if command -v curl >/dev/null 2>&1; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 10)
        if [ "$response" = "$expected_status" ]; then
            echo "✅ OK ($response)"
            return 0
        else
            echo "❌ FAIL ($response)"
            return 1
        fi
    else
        echo "⚠️  SKIP (curl not available)"
        return 0
    fi
}

# Check database
echo -n "Checking Database... "
if docker exec bhivhraiplatform-db-1 pg_isready -U bhiv_user -d bhiv_hr >/dev/null 2>&1; then
    echo "✅ OK"
    db_status=0
else
    echo "❌ FAIL"
    db_status=1
fi

# Check services
check_service "Gateway API" "$GATEWAY_URL/health"
gateway_status=$?

check_service "Agent API" "$AGENT_URL/health"
agent_status=$?

check_service "HR Portal" "$PORTAL_URL"
portal_status=$?

check_service "Client Portal" "$CLIENT_PORTAL_URL"
client_portal_status=$?

# Test API endpoints
echo -n "Testing API Authentication... "
if command -v curl >/dev/null 2>&1; then
    api_response=$(curl -s -H "Authorization: Bearer $API_KEY" "$GATEWAY_URL/v1/jobs" --max-time 10)
    if echo "$api_response" | grep -q "jobs"; then
        echo "✅ OK"
        api_status=0
    else
        echo "❌ FAIL"
        api_status=1
    fi
else
    echo "⚠️  SKIP (curl not available)"
    api_status=0
fi

# Summary
echo ""
echo "📊 Health Check Summary:"
echo "========================"
echo "Database:      $([ $db_status -eq 0 ] && echo "✅ Healthy" || echo "❌ Unhealthy")"
echo "Gateway:       $([ $gateway_status -eq 0 ] && echo "✅ Healthy" || echo "❌ Unhealthy")"
echo "Agent:         $([ $agent_status -eq 0 ] && echo "✅ Healthy" || echo "❌ Unhealthy")"
echo "HR Portal:     $([ $portal_status -eq 0 ] && echo "✅ Healthy" || echo "❌ Unhealthy")"
echo "Client Portal: $([ $client_portal_status -eq 0 ] && echo "✅ Healthy" || echo "❌ Unhealthy")"
echo "API Auth:      $([ $api_status -eq 0 ] && echo "✅ Working" || echo "❌ Failed")"

# Overall status
total_failures=$((db_status + gateway_status + agent_status + portal_status + client_portal_status + api_status))

if [ $total_failures -eq 0 ]; then
    echo ""
    echo "🎉 All services are healthy!"
    exit 0
else
    echo ""
    echo "⚠️  $total_failures service(s) have issues"
    exit 1
fi