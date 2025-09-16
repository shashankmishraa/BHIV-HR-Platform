# Render Environment Variables Configuration

## Required Environment Variables for Each Service

### Gateway Service
```
DATABASE_URL=postgresql://[render_postgres_url]
API_KEY_SECRET=myverysecureapikey123
```

### Agent Service  
```
DATABASE_URL=postgresql://[render_postgres_url]
```

### Portal Services (HR & Client)
```
GATEWAY_URL=https://bhiv-hr-gateway.onrender.com
API_KEY_SECRET=myverysecureapikey123
```

## Steps to Fix Render Deployment

1. **Get PostgreSQL URL from Render Dashboard**
   - Go to your PostgreSQL service in Render
   - Copy the "External Database URL"

2. **Update Environment Variables**
   - Gateway Service: Add DATABASE_URL
   - Agent Service: Add DATABASE_URL  
   - Portal Services: Add GATEWAY_URL and API_KEY_SECRET

3. **Redeploy Services**
   - Trigger manual deploy for each service after updating env vars

## Current Issues Fixed
- ✅ Agent service now uses DATABASE_URL (same as Gateway)
- ✅ Fallback to individual DB params for local development
- ✅ Consistent database connection across all services