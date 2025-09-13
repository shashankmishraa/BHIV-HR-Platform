#!/bin/bash

# BHIV HR Platform - Deploy Production Fixes
echo "🚀 Deploying BHIV HR Platform fixes..."

# Set production environment variables
export GATEWAY_URL="https://bhiv-hr-gateway.onrender.com"
export AGENT_URL="https://bhiv-hr-agent.onrender.com"
export API_KEY_SECRET="myverysecureapikey123"

echo "✅ Environment variables set"

# Apply database schema fixes
echo "🔧 Applying database schema fixes..."
if [ -n "$DATABASE_URL" ]; then
    psql "$DATABASE_URL" -f scripts/fix_database_schema.sql
    echo "✅ Database schema updated"
else
    echo "⚠️ DATABASE_URL not set, skipping database fixes"
fi

# Test AI agent connectivity
echo "🧪 Testing AI agent connectivity..."
curl -f "$AGENT_URL/health" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ AI Agent is accessible"
else
    echo "❌ AI Agent connection failed"
fi

# Test API gateway
echo "🧪 Testing API gateway..."
curl -f "$GATEWAY_URL/health" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ API Gateway is accessible"
else
    echo "❌ API Gateway connection failed"
fi

echo "🎉 Fix deployment completed!"
echo ""
echo "Next steps:"
echo "1. Restart portal services if needed"
echo "2. Test AI matching: Go to Step 4 in HR Portal"
echo "3. Test interview scheduling: Go to Step 5 in HR Portal"
echo ""
echo "Live URLs:"
echo "- HR Portal: https://bhiv-hr-portal.onrender.com"
echo "- Client Portal: https://bhiv-hr-client-portal.onrender.com"
echo "- API Gateway: https://bhiv-hr-gateway.onrender.com/docs"