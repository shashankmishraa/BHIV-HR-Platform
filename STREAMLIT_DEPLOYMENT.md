# Streamlit Cloud Deployment Guide

## 🚀 Deploy BHIV HR Platform on Streamlit Cloud

### Option 1: HR Portal Deployment

1. **Push to GitHub**
   ```bash
   git add streamlit_portal.py requirements-streamlit.txt
   git commit -m "Add Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select repository: `bhiv-hr-platform`
   - Main file: `streamlit_portal.py`
   - Requirements: `requirements-streamlit.txt`

3. **Access URLs**
   - HR Portal: `https://your-app-name.streamlit.app`

### Option 2: Client Portal Deployment

1. **Deploy Client Portal**
   - Main file: `streamlit_client_portal.py`
   - Same requirements file
   - Access code: `google123`

### Option 3: Multi-App Deployment

Create `pages/` directory structure:
```
streamlit_portal.py (main app)
pages/
├── 1_🔍_Search_Candidates.py
├── 2_💼_Job_Management.py
├── 3_🤖_AI_Matching.py
└── 4_👥_Client_Portal.py
```

### Quick Deploy Commands

```bash
# 1. Prepare files
cp streamlit_portal.py app.py
cp requirements-streamlit.txt requirements.txt

# 2. Create GitHub repo
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/bhiv-hr-streamlit.git
git push -u origin main

# 3. Deploy on Streamlit Cloud
# Visit: https://share.streamlit.io
# Connect repo and deploy
```

### Environment Variables (Optional)

In Streamlit Cloud settings:
```
API_BASE_URL = "https://your-api-gateway.com"
API_KEY = "your-secure-api-key"
```

### Features Available in Cloud Version

✅ **HR Portal**
- Dashboard with metrics
- Candidate search interface
- Job management system
- AI matching simulation
- Analytics charts

✅ **Client Portal**
- Secure login (access code: google123)
- Job posting interface
- Candidate review system
- Match results display

✅ **Mock Data**
- 30+ sample candidates
- 15 active jobs
- AI match scores
- Interactive charts

### Live Demo URLs

After deployment, your apps will be available at:
- `https://bhiv-hr-portal.streamlit.app`
- `https://bhiv-client-portal.streamlit.app`

### Deployment Status

🟢 **Ready for Deployment**
- Standalone Streamlit apps created
- Mock data integrated
- No external dependencies
- Cloud-optimized configuration