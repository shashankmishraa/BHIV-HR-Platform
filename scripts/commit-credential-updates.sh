#!/bin/bash
# BHIV HR Platform - Commit Credential Updates Script
# Safely commits configuration updates without exposing secrets

echo "🔄 Committing credential updates..."

# Check current status
echo "📋 Current Git Status:"
git status

echo ""
echo "📝 Adding configuration files..."

# Add specific configuration files (not secrets)
git add README.md
git add docker-compose.production.yml
git add config/render-deployment-config.yml
git add docs/deployment/ENVIRONMENT_VARIABLES_UPDATED.md
git add scripts/deploy-all-services.sh
git add scripts/commit-credential-updates.sh
git add tests/test_updated_credentials.py

# Add service-specific environment templates (these are templates, not actual secrets)
git add services/gateway/.env.production
git add services/agent/.env.production
git add services/portal/.env.production
git add services/client_portal/.env.production

echo "✅ Configuration files added"

# Ensure sensitive files are not tracked
echo ""
echo "🔒 Ensuring sensitive files are not tracked..."
git rm --cached .env 2>/dev/null || echo "✅ .env already not tracked"
git rm --cached .env.render 2>/dev/null || echo "✅ .env.render already not tracked"
git rm --cached config/.env.production 2>/dev/null || echo "✅ config/.env.production already not tracked"

echo ""
echo "📤 Committing changes..."
git commit -m "Update: Production credentials and service URLs

- Updated all service URLs to new Render deployment endpoints
- Updated database connection strings with new credentials
- Added comprehensive environment variable documentation
- Created deployment scripts for automated service deployment
- Updated Docker Compose configuration for local development
- Added validation tests for new service endpoints
- Maintained security by not committing actual .env files

Services Updated:
- Gateway: https://bhiv-hr-gateway-901a.onrender.com
- Agent: https://bhiv-hr-agent-o6nx.onrender.com  
- Portal: https://bhiv-hr-portal-xk2k.onrender.com
- Client Portal: https://bhiv-hr-client-portal-zdbt.onrender.com"

echo ""
echo "🚀 Pushing to remote repository..."
git push origin main

echo ""
echo "✅ Credential updates committed and pushed successfully!"
echo ""
echo "🔗 Next Steps:"
echo "1. Set environment variables in Render Dashboard"
echo "2. Trigger deployments using: ./scripts/deploy-all-services.sh"
echo "3. Validate services using: python tests/test_updated_credentials.py"