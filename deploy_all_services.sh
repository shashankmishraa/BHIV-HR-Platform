#!/bin/bash

# BHIV HR Platform - Deploy All Services
# Triggers individual deployments for all 4 services

echo "🚀 Starting deployment of all BHIV HR Platform services..."

# Service deployment URLs
HR_PORTAL_URL="https://api.render.com/deploy/srv-d2s5vtje5dus73cr0s90?key=POyxo7foEVs"
CLIENT_PORTAL_URL="https://api.render.com/deploy/srv-d2s67pffte5s739kp99g?key=C04znxCoOwE"
GATEWAY_URL="https://api.render.com/deploy/srv-d2s0a6mmcj7s73fn3iqg?key=EwZutgywDXg"
AGENT_URL="https://api.render.com/deploy/srv-d2s0dp3e5dus73cl3a20?key=w7R-2dV-_F"

# Deploy HR Portal
echo "📊 Deploying HR Portal..."
curl -X POST "$HR_PORTAL_URL"
echo "✅ HR Portal deployment triggered"

# Deploy Client Portal  
echo "👥 Deploying Client Portal..."
curl -X POST "$CLIENT_PORTAL_URL"
echo "✅ Client Portal deployment triggered"

# Deploy Gateway
echo "🌐 Deploying API Gateway..."
curl -X POST "$GATEWAY_URL"
echo "✅ Gateway deployment triggered"

# Deploy AI Agent
echo "🤖 Deploying AI Agent..."
curl -X POST "$AGENT_URL"
echo "✅ AI Agent deployment triggered"

echo ""
echo "🎯 All deployments triggered successfully!"
echo "📊 Monitor deployment status at: https://dashboard.render.com"
echo ""
echo "🔗 Service URLs:"
echo "   HR Portal: https://bhiv-hr-portal.onrender.com/"
echo "   Client Portal: https://bhiv-hr-client-portal.onrender.com/"
echo "   Gateway: https://bhiv-hr-gateway.onrender.com/docs"
echo "   AI Agent: https://bhiv-hr-agent.onrender.com/docs"