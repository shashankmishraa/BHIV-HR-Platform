# BHIV HR Platform - Complete Deployment Guide

## 🚀 Step-by-Step AWS Deployment

### Prerequisites Setup (5 minutes)

#### 1. Install AWS CLI
```bash
# Windows (PowerShell as Administrator)
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify installation
aws --version
```

#### 2. Get AWS Credentials
```bash
# Go to AWS Console → IAM → Users → Create User
# Attach policy: AmazonEC2FullAccess
# Create Access Key → Download credentials

# Configure AWS CLI
aws configure
# AWS Access Key ID: [YOUR_ACCESS_KEY]
# AWS Secret Access Key: [YOUR_SECRET_KEY]  
# Default region name: us-east-1
# Default output format: json
```

#### 3. Create SSH Key Pair
```bash
# Create key pair for EC2 access
aws ec2 create-key-pair --key-name bhiv-hr-key --query 'KeyMaterial' --output text > bhiv-hr-key.pem

# Set permissions (Git Bash/WSL)
chmod 400 bhiv-hr-key.pem
```

### Deployment Execution (10 minutes)

#### 1. Navigate to Project
```bash
cd "c:\bhiv hr ai platform"
```

#### 2. Run Deployment Script
```bash
# Option A: Git Bash/WSL
chmod +x scripts/deploy-cloud.sh
./scripts/deploy-cloud.sh

# Option B: PowerShell
bash scripts/deploy-cloud.sh

# Option C: Command Prompt
"C:\Program Files\Git\bin\bash.exe" scripts/deploy-cloud.sh
```

#### 3. Expected Output
```bash
☁️ BHIV HR Platform - Cloud Deployment
======================================
📋 Deployment Configuration:
   Region: us-east-1
   Instance Type: t3.medium
   Key Name: bhiv-hr-key

🔒 Creating security group...
✅ Security group created: sg-0123456789abcdef0

🚀 Launching EC2 instance...
✅ Instance launched: i-0123456789abcdef0

⏳ Waiting for instance to be running...
✅ Instance is running!

🌐 Access URLs:
   HR Portal: http://54.123.45.67:8501
   Client Portal: http://54.123.45.67:8502
   API Gateway: http://54.123.45.67:8000
   API Docs: http://54.123.45.67:8000/docs

🔧 SSH Access:
   ssh -i bhiv-hr-key.pem ec2-user@54.123.45.67

📊 Instance Details:
   Instance ID: i-0123456789abcdef0
   Public IP: 54.123.45.67
   Region: us-east-1

⏳ Note: Application deployment may take 5-10 minutes to complete.
```

### Verification Steps (5 minutes)

#### 1. Check Instance Status
```bash
# Check if instance is running
aws ec2 describe-instances --instance-ids i-0123456789abcdef0 --query 'Reservations[0].Instances[0].State.Name'

# Should return: "running"
```

#### 2. SSH into Instance (Optional)
```bash
# Connect to instance
ssh -i bhiv-hr-key.pem ec2-user@54.123.45.67

# Check Docker containers
docker ps

# Should show 5 running containers:
# - bhiv-hr-platform_db_1
# - bhiv-hr-platform_gateway_1  
# - bhiv-hr-platform_agent_1
# - bhiv-hr-platform_portal_1
# - bhiv-hr-platform_client_portal_1
```

#### 3. Test Application URLs
```bash
# Test API Gateway
curl http://54.123.45.67:8000/health

# Expected response:
# {"status":"healthy","service":"BHIV HR Gateway","version":"3.0.0"}

# Test HR Portal (in browser)
# http://54.123.45.67:8501

# Test Client Portal (in browser)  
# http://54.123.45.67:8502
```

## 🛠️ Alternative: Local Deployment

If AWS deployment fails, run locally:

```bash
# 1. Start local services
docker-compose -f docker-compose.production.yml up -d

# 2. Process sample data
python tools/comprehensive_resume_extractor.py
python tools/create_demo_jobs.py

# 3. Access locally
# HR Portal: http://localhost:8501
# Client Portal: http://localhost:8502
# API Gateway: http://localhost:8000
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### AWS CLI Not Configured
```bash
# Error: "Unable to locate credentials"
# Solution: Run aws configure with valid credentials
aws configure list
```

#### Permission Denied
```bash
# Error: "An error occurred (UnauthorizedOperation)"
# Solution: Add EC2 permissions to IAM user
# Go to IAM → Users → Attach Policy → AmazonEC2FullAccess
```

#### Instance Launch Failed
```bash
# Error: "InvalidKeyPair.NotFound"
# Solution: Create key pair first
aws ec2 create-key-pair --key-name bhiv-hr-key --query 'KeyMaterial' --output text > bhiv-hr-key.pem
```

#### Application Not Loading
```bash
# Wait 5-10 minutes for Docker containers to start
# Check instance logs:
ssh -i bhiv-hr-key.pem ec2-user@[PUBLIC_IP]
sudo journalctl -u bhiv-hr.service -f
```

### Manual Deployment (If Script Fails)

```bash
# 1. Launch instance manually
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type t3.medium \
  --key-name bhiv-hr-key \
  --security-groups default

# 2. Get public IP
aws ec2 describe-instances --query 'Reservations[0].Instances[0].PublicIpAddress'

# 3. SSH and deploy manually
ssh -i bhiv-hr-key.pem ec2-user@[PUBLIC_IP]
sudo yum update -y
sudo yum install -y docker git
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and deploy
git clone [YOUR_REPO_URL]
cd bhiv-hr-platform
docker-compose -f docker-compose.production.yml up -d
```

## 📊 Success Checklist

- [ ] AWS CLI installed and configured
- [ ] SSH key pair created
- [ ] Deployment script executed successfully
- [ ] EC2 instance running
- [ ] All 5 Docker containers running
- [ ] API Gateway responding (port 8000)
- [ ] HR Portal accessible (port 8501)
- [ ] Client Portal accessible (port 8502)
- [ ] Sample data loaded and searchable

## 🎯 Demo URLs

Once deployed, share these URLs for demonstration:

```
🌐 BHIV HR Platform Demo
========================
HR Portal: http://[PUBLIC_IP]:8501
Client Portal: http://[PUBLIC_IP]:8502  
API Documentation: http://[PUBLIC_IP]:8000/docs
Health Check: http://[PUBLIC_IP]:8000/health

Login Credentials:
- Client Portal Access Code: google123
- API Key: myverysecureapikey123
```

## 💰 Cost Management

```bash
# Stop instance when not needed
aws ec2 stop-instances --instance-ids i-0123456789abcdef0

# Start instance when needed
aws ec2 start-instances --instance-ids i-0123456789abcdef0

# Terminate instance (permanent deletion)
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0
```

## 📞 Support

If deployment fails:
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify region: `aws configure get region`
3. Check permissions: Ensure EC2FullAccess policy attached
4. Try local deployment as fallback
5. Review AWS CloudTrail logs for detailed error messages

**Estimated Total Time**: 20 minutes (5 min setup + 10 min deployment + 5 min verification)

**Free Tier Usage**: ~750 hours/month available for t2.micro instances