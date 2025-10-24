# 🔧 Render Environment Variables Guide

⚠️ **SECURITY WARNING**: This guide uses placeholder values. Never commit actual credentials to version control.

## 📋 Service-Specific Environment Variables

### **Gateway Service (bhiv-hr-gateway)**
```bash
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_JWT_SECRET_KEY]
CANDIDATE_JWT_SECRET=[YOUR_CANDIDATE_JWT_SECRET]
AGENT_SERVICE_URL=https://[YOUR_AGENT_SERVICE_URL]
```

### **Agent Service (bhiv-hr-agent)**
```bash
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_JWT_SECRET_KEY]
```

### **HR Portal Service (bhiv-hr-portal)**
```bash
GATEWAY_URL=https://[YOUR_GATEWAY_URL]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
AGENT_SERVICE_URL=https://[YOUR_AGENT_SERVICE_URL]
```

### **Client Portal Service (bhiv-hr-client-portal)**
```bash
GATEWAY_URL=https://[YOUR_GATEWAY_URL]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_JWT_SECRET_KEY]
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
AGENT_SERVICE_URL=https://[YOUR_AGENT_SERVICE_URL]
```

### **Candidate Portal Service (bhiv-hr-candidate-portal)**
```bash
GATEWAY_URL=https://[YOUR_GATEWAY_URL]
API_KEY=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_CANDIDATE_JWT_SECRET]
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
```

## 🔒 Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate credentials** regularly
4. **Use strong, unique secrets** for each environment
5. **Limit access** to production credentials

## 🔧 Setup Instructions

1. Access Render Dashboard
2. Select your service
3. Go to Environment tab
4. Add variables with your actual values
5. Deploy changes

## 🧪 Testing

```bash
# Test with your actual API key
curl -H "Authorization: Bearer [YOUR_API_KEY]" \
     https://[YOUR_GATEWAY_URL]/health
```

*Last Updated: October 23, 2025*