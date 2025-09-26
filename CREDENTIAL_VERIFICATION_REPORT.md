# Credential Verification Report
Generated: 2025-09-27 03:16:21

## Environment Files
- PASS: .env
- PASS: .env.production
- PASS: services/gateway/.env.production
- PASS: services/agent/.env.production
- PASS: services/portal/.env.production
- PASS: services/client_portal/.env.production

## Service URLs
- FAIL: gateway (ERROR)
  - Error: HTTPSConnectionPool(host='bhiv-hr-gateway-46pz.onrender.com', port=443): Read timed out. (read timeout=10)
- FAIL: agent (ERROR)
  - Error: HTTPSConnectionPool(host='bhiv-hr-agent-m1me.onrender.com', port=443): Read timed out. (read timeout=10)
- FAIL: portal (502)
- FAIL: client_portal (502)

## Configuration Files
- PASS: config/environments.yml
- PASS: config/settings.json
- PASS: config/render-deployment-config.yml
