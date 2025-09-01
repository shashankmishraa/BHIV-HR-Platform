#!/bin/bash
# BHIV HR Platform - Cloud Deployment Script

set -e

echo "☁️ BHIV HR Platform - Cloud Deployment"
echo "======================================"

# Configuration
REGION=${AWS_REGION:-us-east-1}
INSTANCE_TYPE=${INSTANCE_TYPE:-t3.medium}
KEY_NAME=${KEY_NAME:-bhiv-hr-key}

echo "📋 Deployment Configuration:"
echo "   Region: $REGION"
echo "   Instance Type: $INSTANCE_TYPE"
echo "   Key Name: $KEY_NAME"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install AWS CLI first."
    exit 1
fi

# Create security group
echo "🔒 Creating security group..."
SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --group-name bhiv-hr-sg \
    --description "BHIV HR Platform Security Group" \
    --region $REGION \
    --query 'GroupId' \
    --output text 2>/dev/null || echo "exists")

if [ "$SECURITY_GROUP_ID" != "exists" ]; then
    # Add inbound rules
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 22 \
        --cidr 0.0.0.0/0 \
        --region $REGION

    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 8000 \
        --cidr 0.0.0.0/0 \
        --region $REGION

    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 8501 \
        --cidr 0.0.0.0/0 \
        --region $REGION

    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 8502 \
        --cidr 0.0.0.0/0 \
        --region $REGION
    
    echo "✅ Security group created: $SECURITY_GROUP_ID"
else
    SECURITY_GROUP_ID=$(aws ec2 describe-security-groups \
        --group-names bhiv-hr-sg \
        --region $REGION \
        --query 'SecurityGroups[0].GroupId' \
        --output text)
    echo "✅ Using existing security group: $SECURITY_GROUP_ID"
fi

# Launch EC2 instance
echo "🚀 Launching EC2 instance..."
USER_DATA=$(cat << 'EOF'
#!/bin/bash
yum update -y
yum install -y docker git

# Start Docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone repository
cd /home/ec2-user
git clone https://github.com/your-repo/bhiv-hr-platform.git
cd bhiv-hr-platform

# Set permissions
chown -R ec2-user:ec2-user /home/ec2-user/bhiv-hr-platform

# Deploy application
sudo -u ec2-user docker-compose -f docker-compose.production.yml up -d

# Create startup script
cat > /etc/systemd/system/bhiv-hr.service << 'EOL'
[Unit]
Description=BHIV HR Platform
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ec2-user/bhiv-hr-platform
ExecStart=/usr/local/bin/docker-compose -f docker-compose.production.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.production.yml down
User=ec2-user

[Install]
WantedBy=multi-user.target
EOL

systemctl enable bhiv-hr.service
systemctl start bhiv-hr.service
EOF
)

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --user-data "$USER_DATA" \
    --region $REGION \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=BHIV-HR-Platform}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ Instance launched: $INSTANCE_ID"

# Wait for instance to be running
echo "⏳ Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "✅ Instance is running!"
echo ""
echo "🌐 Access URLs:"
echo "   HR Portal: http://$PUBLIC_IP:8501"
echo "   Client Portal: http://$PUBLIC_IP:8502"
echo "   API Gateway: http://$PUBLIC_IP:8000"
echo "   API Docs: http://$PUBLIC_IP:8000/docs"
echo ""
echo "🔧 SSH Access:"
echo "   ssh -i $KEY_NAME.pem ec2-user@$PUBLIC_IP"
echo ""
echo "📊 Instance Details:"
echo "   Instance ID: $INSTANCE_ID"
echo "   Public IP: $PUBLIC_IP"
echo "   Region: $REGION"
echo ""
echo "⏳ Note: Application deployment may take 5-10 minutes to complete."
echo "   Check status: ssh -i $KEY_NAME.pem ec2-user@$PUBLIC_IP 'docker ps'"