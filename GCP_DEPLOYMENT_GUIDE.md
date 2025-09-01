# BHIV HR Platform - GCP Deployment Guide

## 🚀 Step-by-Step GCP Deployment

### Prerequisites Setup (10 minutes)

#### 1. Create GCP Account
```bash
# Go to: https://cloud.google.com/
# Click "Get started for free"
# Sign up with Google account
# Get $300 free credit (no payment method required initially)
```

#### 2. Install Google Cloud CLI
```bash
# Download for Windows:
# https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe

# Run installer and follow prompts
# Restart PowerShell after installation

# Verify installation:
gcloud --version
```

#### 3. Initialize GCP CLI
```bash
# Login to your GCP account:
gcloud auth login

# Set up project:
gcloud projects create bhiv-hr-platform --name="BHIV HR Platform"
gcloud config set project bhiv-hr-platform

# Enable required APIs:
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
```

### Deployment Options

## Option A: Compute Engine (VM) Deployment

#### 1. Create VM Instance
```bash
# Create firewall rules:
gcloud compute firewall-rules create bhiv-hr-ports \
  --allow tcp:8000,tcp:8501,tcp:8502 \
  --source-ranges 0.0.0.0/0 \
  --description "BHIV HR Platform ports"

# Create VM instance:
gcloud compute instances create bhiv-hr-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --tags=http-server,https-server
```

#### 2. SSH and Setup
```bash
# SSH into instance:
gcloud compute ssh bhiv-hr-vm --zone=us-central1-a

# Install Docker:
sudo apt update
sudo apt install -y docker.io docker-compose git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Clone repository (you'll need to upload your code):
git clone https://github.com/your-username/bhiv-hr-platform.git
cd bhiv-hr-platform

# Deploy:
docker-compose -f docker-compose.production.yml up -d
```

#### 3. Get External IP
```bash
# Get VM external IP:
gcloud compute instances describe bhiv-hr-vm \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

# Access URLs:
# HR Portal: http://[EXTERNAL_IP]:8501
# Client Portal: http://[EXTERNAL_IP]:8502
# API Gateway: http://[EXTERNAL_IP]:8000
```

## Option B: Cloud Run (Serverless) Deployment

#### 1. Create GCP Deployment Script
```bash
# Create: scripts/deploy-gcp.sh
#!/bin/bash

PROJECT_ID="bhiv-hr-platform"
REGION="us-central1"

echo "🚀 BHIV HR Platform - GCP Cloud Run Deployment"

# Build and push images
gcloud builds submit --tag gcr.io/$PROJECT_ID/bhiv-gateway services/gateway
gcloud builds submit --tag gcr.io/$PROJECT_ID/bhiv-portal services/portal
gcloud builds submit --tag gcr.io/$PROJECT_ID/bhiv-client-portal services/client_portal

# Deploy services
gcloud run deploy bhiv-gateway \
  --image gcr.io/$PROJECT_ID/bhiv-gateway \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000

gcloud run deploy bhiv-portal \
  --image gcr.io/$PROJECT_ID/bhiv-portal \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8501

gcloud run deploy bhiv-client-portal \
  --image gcr.io/$PROJECT_ID/bhiv-client-portal \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8502

echo "✅ Deployment complete!"
gcloud run services list --platform managed --region $REGION
```

#### 2. Run GCP Deployment
```bash
# Make script executable:
chmod +x scripts/deploy-gcp.sh

# Run deployment:
./scripts/deploy-gcp.sh
```

## Quick Setup Commands

### Complete GCP Setup (Copy-Paste Ready)
```bash
# 1. Install GCP CLI (run installer first)
gcloud --version

# 2. Login and setup project
gcloud auth login
gcloud projects create bhiv-hr-platform-$(date +%s) --name="BHIV HR Platform"
gcloud config set project $(gcloud projects list --format="value(projectId)" --filter="name:'BHIV HR Platform'")

# 3. Enable APIs
gcloud services enable compute.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# 4. Create firewall rule
gcloud compute firewall-rules create bhiv-hr-ports \
  --allow tcp:8000,tcp:8501,tcp:8502 \
  --source-ranges 0.0.0.0/0

# 5. Create VM
gcloud compute instances create bhiv-hr-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --metadata=startup-script='#!/bin/bash
apt update
apt install -y docker.io docker-compose git
systemctl start docker
systemctl enable docker
usermod -aG docker $(whoami)
'

# 6. Get external IP
gcloud compute instances describe bhiv-hr-vm \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

### Manual VM Setup
```bash
# SSH into VM:
gcloud compute ssh bhiv-hr-vm --zone=us-central1-a

# Setup application:
sudo apt update
sudo apt install -y docker.io docker-compose git
sudo systemctl start docker
sudo usermod -aG docker $USER

# Logout and login again, then:
# Upload your project files or clone from git
# cd to project directory
docker-compose -f docker-compose.production.yml up -d
```

## Verification Steps

#### 1. Check VM Status
```bash
# List running instances:
gcloud compute instances list

# Check VM logs:
gcloud compute instances get-serial-port-output bhiv-hr-vm --zone=us-central1-a
```

#### 2. Test Application
```bash
# Get external IP:
EXTERNAL_IP=$(gcloud compute instances describe bhiv-hr-vm \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Test endpoints:
curl http://$EXTERNAL_IP:8000/health

# Access in browser:
echo "HR Portal: http://$EXTERNAL_IP:8501"
echo "Client Portal: http://$EXTERNAL_IP:8502"
echo "API Gateway: http://$EXTERNAL_IP:8000"
```

## Cost Management

```bash
# Stop VM when not needed:
gcloud compute instances stop bhiv-hr-vm --zone=us-central1-a

# Start VM when needed:
gcloud compute instances start bhiv-hr-vm --zone=us-central1-a

# Delete VM (permanent):
gcloud compute instances delete bhiv-hr-vm --zone=us-central1-a

# Delete project (removes everything):
gcloud projects delete bhiv-hr-platform
```

## Troubleshooting

### Common Issues

#### GCP CLI Not Found
```bash
# Reinstall GCP CLI:
# Download: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
# Restart PowerShell after installation
```

#### Permission Denied
```bash
# Re-authenticate:
gcloud auth login
gcloud auth application-default login
```

#### VM Creation Failed
```bash
# Check quotas:
gcloud compute project-info describe --project=$(gcloud config get-value project)

# Try different zone:
gcloud compute instances create bhiv-hr-vm --zone=us-east1-b
```

#### Application Not Loading
```bash
# SSH into VM and check:
gcloud compute ssh bhiv-hr-vm --zone=us-central1-a
sudo docker ps
sudo docker logs [container-name]
```

## Success Checklist

- [ ] GCP account created with $300 credit
- [ ] Google Cloud CLI installed and configured
- [ ] Project created and APIs enabled
- [ ] VM instance running
- [ ] Firewall rules configured
- [ ] Application deployed and accessible
- [ ] All services responding on external IP

## Demo URLs

Once deployed, share these URLs:

```
🌐 BHIV HR Platform Demo (GCP)
===============================
HR Portal: http://[EXTERNAL_IP]:8501
Client Portal: http://[EXTERNAL_IP]:8502  
API Documentation: http://[EXTERNAL_IP]:8000/docs
Health Check: http://[EXTERNAL_IP]:8000/health

Login Credentials:
- Client Portal Access Code: google123
- API Key: myverysecureapikey123
```

**Estimated Total Time**: 15 minutes (10 min setup + 5 min deployment)
**Free Tier**: $300 credit covers months of usage