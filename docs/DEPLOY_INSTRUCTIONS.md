# BHIV HR Platform - Render Deployment Instructions

## Prerequisites
1. Create a Render account at https://render.com
2. Connect your GitHub repository to Render
3. Push your code to GitHub

## Deployment Order (IMPORTANT: Deploy in this exact order)

### 1. Deploy Database First
- Service Type: **PostgreSQL**
- Name: `bhiv-hr-database`
- Database Name: `bhiv_hr`
- User: `bhiv_user`
- Plan: Free
- Save the **Internal Database URL** for other services

### 2. Deploy API Gateway
- Service Type: **Web Service**
- Name: `bhiv-hr-gateway`
- Root Directory: `services/gateway`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  - `DATABASE_URL`: [Use Internal Database URL from step 1]
  - `API_KEY_SECRET`: `myverysecureapikey123`

### 3. Deploy AI Agent
- Service Type: **Web Service**
- Name: `bhiv-hr-agent`
- Root Directory: `services/agent`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  - `DATABASE_URL`: [Use Internal Database URL from step 1]

### 4. Deploy HR Portal
- Service Type: **Web Service**
- Name: `bhiv-hr-portal`
- Root Directory: `services/portal`
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Environment Variables:
  - `GATEWAY_URL`: [Use Internal URL from Gateway service]
  - `API_KEY_SECRET`: `myverysecureapikey123`

### 5. Deploy Client Portal
- Service Type: **Web Service**
- Name: `bhiv-hr-client-portal`
- Root Directory: `services/client_portal`
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Environment Variables:
  - `GATEWAY_URL`: [Use Internal URL from Gateway service]
  - `API_KEY_SECRET`: `myverysecureapikey123`

## Important Notes
- Use **Internal URLs** for service-to-service communication
- External URLs are for browser access only
- Free tier has limitations: services may sleep after 15 minutes of inactivity
- Database persists data even on free tier

## Troubleshooting
- Check logs in Render dashboard for each service
- Ensure environment variables are set correctly
- Verify build and start commands match your file structure