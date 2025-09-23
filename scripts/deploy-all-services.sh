#!/bin/bash
# BHIV HR Platform - Deploy All Services Script
# Triggers deployment for all Render services

echo "🚀 Deploying BHIV HR Platform Services..."

# Service URLs and Deploy Hooks
GATEWAY_HOOK="https://api.render.com/deploy/srv-d3744qje5dus7390foq0?key=V6wlJ-fv6EY"
AGENT_HOOK="https://api.render.com/deploy/srv-d3747q3uibrs738n539g?key=cto8n-Ctivw"
PORTAL_HOOK="https://api.render.com/deploy/srv-d374emmmcj7s73fdbbb0?key=dTyTmqjQwu4"
CLIENT_PORTAL_HOOK="https://api.render.com/deploy/srv-d374kkre5dus7390tlgg?key=aV7OERRhxS4"

echo "📡 Triggering Gateway deployment..."
curl -X POST "$GATEWAY_HOOK"
echo "✅ Gateway deployment triggered"

echo "🤖 Triggering Agent deployment..."
curl -X POST "$AGENT_HOOK"
echo "✅ Agent deployment triggered"

echo "🖥️ Triggering Portal deployment..."
curl -X POST "$PORTAL_HOOK"
echo "✅ Portal deployment triggered"

echo "👥 Triggering Client Portal deployment..."
curl -X POST "$CLIENT_PORTAL_HOOK"
echo "✅ Client Portal deployment triggered"

echo ""
echo "🎯 All deployments triggered successfully!"
echo ""
echo "📊 Service URLs:"
echo "Gateway:       https://bhiv-hr-gateway-901a.onrender.com"
echo "Agent:         https://bhiv-hr-agent-o6nx.onrender.com"
echo "Portal:        https://bhiv-hr-portal-xk2k.onrender.com"
echo "Client Portal: https://bhiv-hr-client-portal-zdbt.onrender.com"
echo ""
echo "⏱️ Deployments typically take 2-3 minutes to complete."
echo "🔍 Monitor progress in Render Dashboard"