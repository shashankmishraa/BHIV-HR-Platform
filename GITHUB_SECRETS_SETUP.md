# 🔐 GitHub Repository Secrets Setup Guide

## Required GitHub Secrets

Navigate to: **GitHub Repository → Settings → Secrets and variables → Actions**

### **Production Secrets**
```bash
DATABASE_URL=postgresql://username:password@host:port/database
JWT_SECRET=your-secure-jwt-secret-minimum-32-characters
API_KEY_SECRET=your-secure-api-key-secret-minimum-32-characters
SECRET_KEY=your-secure-secret-key-minimum-32-characters
```

### **Service URLs**
```bash
GATEWAY_URL=https://bhiv-hr-gateway-46pz.onrender.com
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
PORTAL_URL=https://bhiv-hr-portal-cead.onrender.com
CLIENT_PORTAL_URL=https://bhiv-hr-client-portal-5g33.onrender.com
```

### **Deployment Secrets**
```bash
RENDER_API_KEY=your-render-api-key
POSTGRES_PASSWORD=your-database-password
```

## Setup Instructions

1. **Go to Repository Settings**
   - Navigate to your GitHub repository
   - Click on "Settings" tab
   - Select "Secrets and variables" → "Actions"

2. **Add Each Secret**
   - Click "New repository secret"
   - Enter the name (e.g., `DATABASE_URL`)
   - Enter the value
   - Click "Add secret"

3. **Verify Secrets**
   - Ensure all required secrets are added
   - Check that secret names match exactly

## Security Best Practices

- **Never commit secrets to code**
- **Use strong, unique values for each secret**
- **Rotate secrets regularly (every 90 days)**
- **Use different secrets for different environments**

## Testing

After adding secrets, test with:
```bash
# Trigger GitHub Actions workflow
git push origin main
```

Check workflow logs to ensure secrets are loaded correctly.