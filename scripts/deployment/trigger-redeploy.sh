#!/bin/bash

# Trigger Render Service Redeployment
echo "🚀 Triggering BHIV HR Platform Service Redeployment"
echo "=================================================="

# Service deployment hooks
GATEWAY_HOOK="https://api.render.com/deploy/srv-d3bfsejuibrs73feao6g?key=W4WZMj1i9g0"
AGENT_HOOK="https://api.render.com/deploy/srv-d3747q3uibrs738n539g?key=cto8n-Ctivw"
PORTAL_HOOK="https://api.render.com/deploy/srv-d3bg3igdl3ps739btv5g?key=LXdmYEdUCTU"
CLIENT_HOOK="https://api.render.com/deploy/srv-d3bg4s56ubrc739n5ps0?key=NZPMJzMGWU0"

echo "🔄 Triggering Gateway deployment..."
curl -X POST "$GATEWAY_HOOK" && echo "✅ Gateway deployment triggered"

echo "🔄 Triggering Agent deployment..."
curl -X POST "$AGENT_HOOK" && echo "✅ Agent deployment triggered"

echo "🔄 Triggering Portal deployment..."
curl -X POST "$PORTAL_HOOK" && echo "✅ Portal deployment triggered"

echo "🔄 Triggering Client Portal deployment..."
curl -X POST "$CLIENT_HOOK" && echo "✅ Client Portal deployment triggered"

echo ""
echo "⏳ Waiting for deployments to start..."
sleep 30

echo "🔍 Checking service health..."
echo "Gateway: https://bhiv-hr-gateway-46pz.onrender.com/health"
echo "Agent: https://bhiv-hr-agent-m1me.onrender.com/health"
echo "Portal: https://bhiv-hr-portal-cead.onrender.com/"
echo "Client: https://bhiv-hr-client-portal-5g33.onrender.com/"

echo ""
echo "✅ All deployments triggered successfully!"
echo "Services will be available in 2-3 minutes."