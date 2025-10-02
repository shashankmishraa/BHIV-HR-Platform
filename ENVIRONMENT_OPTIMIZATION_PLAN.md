# BHIV HR Platform - Environment Management Optimization

## Current Environment Issues & Solutions

### 🔴 CRITICAL: Security Vulnerabilities
**Issue**: Hardcoded production credentials in repository
**Risk**: API keys and passwords exposed in version control
**Impact**: High security risk for production deployment

### 🟡 MEDIUM: Environment Inconsistency  
**Issue**: Different variable names across services
**Risk**: Configuration errors during deployment
**Impact**: Service communication failures

### 🟢 LOW: Development Experience
**Issue**: Manual environment setup for new developers
**Risk**: Inconsistent local development environments
**Impact**: Reduced development productivity

## Optimized Environment Structure

### 1. Environment Hierarchy
```
environments/
├── local/
│   ├── .env                    # Local development variables
│   ├── docker-compose.yml      # Local Docker setup
│   └── config.yaml            # Local service configuration
├── staging/
│   ├── .env.staging           # Staging environment variables
│   ├── docker-compose.staging.yml
│   └── render-staging.yml     # Staging Render config
├── production/
│   ├── .env.template          # Production template (no secrets)
│   ├── docker-compose.production.yml
│   └── render-production.yml  # Production Render config
└── shared/
    ├── base.env               # Common variables across environments
    ├── database.env           # Database configuration templates
    └── security.env           # Security configuration templates
```

### 2. Standardized Variable Naming
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=bhiv_hr
DATABASE_USER=bhiv_user
DATABASE_PASSWORD=secure_password
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30

# Service URLs (Internal Communication)
GATEWAY_SERVICE_URL=http://gateway:8000
AGENT_SERVICE_URL=http://agent:9000
PORTAL_SERVICE_URL=http://portal:8501
CLIENT_PORTAL_SERVICE_URL=http://client_portal:8502

# External URLs (Public Access)
GATEWAY_PUBLIC_URL=https://bhiv-hr-gateway-46pz.onrender.com
AGENT_PUBLIC_URL=https://bhiv-hr-agent-m1me.onrender.com
PORTAL_PUBLIC_URL=https://bhiv-hr-portal-cead.onrender.com
CLIENT_PORTAL_PUBLIC_URL=https://bhiv-hr-client-portal-5g33.onrender.com

# Security Configuration
API_KEY_SECRET=${API_KEY_SECRET}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
BCRYPT_ROUNDS=12

# Rate Limiting
RATE_LIMIT_DEFAULT=60
RATE_LIMIT_PREMIUM=300
RATE_LIMIT_WINDOW_MINUTES=1
RATE_LIMIT_BURST_MULTIPLIER=2

# Performance Settings
MAX_CANDIDATES_PER_REQUEST=50
AI_MATCHING_TIMEOUT_SECONDS=15
HTTP_TIMEOUT_SECONDS=10
CONNECTION_POOL_SIZE=20

# Feature Flags
ENABLE_2FA=true
ENABLE_RATE_LIMITING=true
ENABLE_MONITORING=true
ENABLE_CACHING=false
ENABLE_DEBUG_MODE=false

# Monitoring & Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
PROMETHEUS_PORT=9090
```

### 3. Environment-Specific Configurations

#### Local Development (.env.local)
```bash
# Local Development Environment
ENVIRONMENT=local
DEBUG=true

# Database (Local PostgreSQL)
DATABASE_URL=postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Service URLs (Docker Compose)
GATEWAY_SERVICE_URL=http://localhost:8000
AGENT_SERVICE_URL=http://localhost:9000
PORTAL_SERVICE_URL=http://localhost:8501
CLIENT_PORTAL_SERVICE_URL=http://localhost:8502

# Security (Development Keys)
API_KEY_SECRET=dev_api_key_12345
JWT_SECRET_KEY=dev_jwt_secret_67890

# Performance (Relaxed for Development)
RATE_LIMIT_DEFAULT=1000
AI_MATCHING_TIMEOUT_SECONDS=30
LOG_LEVEL=DEBUG

# Feature Flags (Development)
ENABLE_DEBUG_MODE=true
ENABLE_CACHING=false
```

#### Staging Environment (.env.staging)
```bash
# Staging Environment
ENVIRONMENT=staging
DEBUG=false

# Database (Staging PostgreSQL)
DATABASE_URL=${STAGING_DATABASE_URL}
DATABASE_POOL_SIZE=5

# Service URLs (Staging Render)
GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-staging.onrender.com
AGENT_SERVICE_URL=https://bhiv-hr-agent-staging.onrender.com

# Security (Staging Keys)
API_KEY_SECRET=${STAGING_API_KEY_SECRET}
JWT_SECRET_KEY=${STAGING_JWT_SECRET_KEY}

# Performance (Staging Limits)
RATE_LIMIT_DEFAULT=100
AI_MATCHING_TIMEOUT_SECONDS=20
LOG_LEVEL=INFO

# Feature Flags (Staging)
ENABLE_DEBUG_MODE=false
ENABLE_CACHING=true
```

#### Production Environment (.env.production)
```bash
# Production Environment
ENVIRONMENT=production
DEBUG=false

# Database (Production PostgreSQL - Secrets from Render)
DATABASE_URL=${DATABASE_URL}
DATABASE_POOL_SIZE=20
DATABASE_POOL_TIMEOUT=30

# Service URLs (Production Render)
GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-46pz.onrender.com
AGENT_SERVICE_URL=https://bhiv-hr-agent-m1me.onrender.com
PORTAL_SERVICE_URL=https://bhiv-hr-portal-cead.onrender.com
CLIENT_PORTAL_SERVICE_URL=https://bhiv-hr-client-portal-5g33.onrender.com

# Security (Production Secrets - From Render Environment)
API_KEY_SECRET=${API_KEY_SECRET}
JWT_SECRET_KEY=${JWT_SECRET_KEY}

# Performance (Production Optimized)
RATE_LIMIT_DEFAULT=60
RATE_LIMIT_PREMIUM=300
AI_MATCHING_TIMEOUT_SECONDS=15
HTTP_TIMEOUT_SECONDS=10
LOG_LEVEL=INFO

# Feature Flags (Production)
ENABLE_DEBUG_MODE=false
ENABLE_CACHING=true
ENABLE_MONITORING=true
```

## Implementation Plan

### Phase 1: Environment Restructure (Day 1-2)
1. **Create environment directories**
2. **Move existing configurations**
3. **Standardize variable names**
4. **Update .gitignore**

### Phase 2: Service Configuration Update (Day 3-4)
1. **Update all service configurations**
2. **Implement environment detection**
3. **Add configuration validation**
4. **Test local deployment**

### Phase 3: Render Environment Setup (Day 5)
1. **Configure Render environment variables**
2. **Remove secrets from repository**
3. **Test production deployment**
4. **Verify all services**

### Phase 4: Documentation & Scripts (Day 6-7)
1. **Update deployment documentation**
2. **Create setup scripts**
3. **Add environment validation**
4. **Create troubleshooting guide**

## Configuration Management Code

### Environment Loader
```python
# config/environment.py
import os
from typing import Dict, Any
from pathlib import Path

class EnvironmentConfig:
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'local')
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration based on environment"""
        config_file = Path(f"environments/{self.environment}/.env")
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        config = {}
        with open(config_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = os.getenv(key, value)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def validate(self) -> bool:
        """Validate required configuration"""
        required_vars = [
            'DATABASE_URL',
            'API_KEY_SECRET',
            'JWT_SECRET_KEY'
        ]
        
        missing = [var for var in required_vars if not self.get(var)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
        
        return True

# Usage in services
config = EnvironmentConfig()
config.validate()

DATABASE_URL = config.get('DATABASE_URL')
API_KEY_SECRET = config.get('API_KEY_SECRET')
```

### Docker Compose Environment Integration
```yaml
# docker-compose.yml (Environment-aware)
version: '3.8'

services:
  gateway:
    build: ./services/gateway
    ports:
      - "${GATEWAY_PORT:-8000}:8000"
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-local}
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY_SECRET=${API_KEY_SECRET}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    env_file:
      - environments/${ENVIRONMENT:-local}/.env
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  agent:
    build: ./services/agent
    ports:
      - "${AGENT_PORT:-9000}:9000"
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-local}
      - DATABASE_URL=${DATABASE_URL}
      - GATEWAY_SERVICE_URL=${GATEWAY_SERVICE_URL}
    env_file:
      - environments/${ENVIRONMENT:-local}/.env
    depends_on:
      - db
      - gateway
```

### Deployment Scripts

#### Local Development Setup
```bash
#!/bin/bash
# scripts/setup-local.sh

echo "🚀 Setting up BHIV HR Platform for local development..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Set environment
export ENVIRONMENT=local

# Create local environment file if it doesn't exist
if [ ! -f "environments/local/.env" ]; then
    echo "📝 Creating local environment configuration..."
    cp environments/local/.env.template environments/local/.env
    echo "✅ Please edit environments/local/.env with your local settings"
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose -f docker-compose.yml --env-file environments/local/.env up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
curl -f http://localhost:8000/health && echo "✅ Gateway: Healthy"
curl -f http://localhost:9000/health && echo "✅ Agent: Healthy"

echo "🎉 Local development environment is ready!"
echo "📊 Access points:"
echo "   - API Gateway: http://localhost:8000/docs"
echo "   - AI Agent: http://localhost:9000/docs"
echo "   - HR Portal: http://localhost:8501"
echo "   - Client Portal: http://localhost:8502"
```

#### Production Deployment Validation
```bash
#!/bin/bash
# scripts/validate-production.sh

echo "🔍 Validating production deployment..."

# Check all production services
SERVICES=(
    "https://bhiv-hr-gateway-46pz.onrender.com/health"
    "https://bhiv-hr-agent-m1me.onrender.com/health"
    "https://bhiv-hr-portal-cead.onrender.com/"
    "https://bhiv-hr-client-portal-5g33.onrender.com/"
)

for service in "${SERVICES[@]}"; do
    if curl -f -s "$service" > /dev/null; then
        echo "✅ $service - Healthy"
    else
        echo "❌ $service - Unhealthy"
    fi
done

# Test API functionality
echo "🧪 Testing API functionality..."
API_KEY="prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
curl -H "Authorization: Bearer $API_KEY" \
     -f "https://bhiv-hr-gateway-46pz.onrender.com/v1/jobs" && \
     echo "✅ API Authentication: Working"

echo "🎉 Production validation complete!"
```

## Security Improvements

### 1. Secrets Management
```bash
# Remove secrets from repository
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch config/production.env' \
--prune-empty --tag-name-filter cat -- --all

# Add to .gitignore
echo "environments/*/.*env" >> .gitignore
echo "config/*.env" >> .gitignore
echo "**/*secret*" >> .gitignore
```

### 2. Environment Variable Validation
```python
# config/validator.py
import os
import re
from typing import List, Dict

class EnvironmentValidator:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_database_url(self, url: str) -> bool:
        """Validate database URL format"""
        pattern = r'^postgresql://[\w\-]+:[\w\-]+@[\w\-\.]+:\d+/[\w\-]+$'
        if not re.match(pattern, url):
            self.errors.append("Invalid DATABASE_URL format")
            return False
        return True
    
    def validate_api_key(self, key: str) -> bool:
        """Validate API key strength"""
        if len(key) < 32:
            self.errors.append("API_KEY_SECRET too short (minimum 32 characters)")
            return False
        if key.startswith('dev_') and os.getenv('ENVIRONMENT') == 'production':
            self.errors.append("Development API key used in production")
            return False
        return True
    
    def validate_jwt_secret(self, secret: str) -> bool:
        """Validate JWT secret strength"""
        if len(secret) < 32:
            self.errors.append("JWT_SECRET_KEY too short (minimum 32 characters)")
            return False
        return True
    
    def validate_all(self, config: Dict[str, str]) -> bool:
        """Validate all configuration"""
        self.errors.clear()
        self.warnings.clear()
        
        # Required validations
        if 'DATABASE_URL' in config:
            self.validate_database_url(config['DATABASE_URL'])
        
        if 'API_KEY_SECRET' in config:
            self.validate_api_key(config['API_KEY_SECRET'])
        
        if 'JWT_SECRET_KEY' in config:
            self.validate_jwt_secret(config['JWT_SECRET_KEY'])
        
        # Environment-specific validations
        environment = config.get('ENVIRONMENT', 'local')
        if environment == 'production':
            if config.get('DEBUG', 'false').lower() == 'true':
                self.warnings.append("DEBUG mode enabled in production")
        
        return len(self.errors) == 0
    
    def report(self) -> str:
        """Generate validation report"""
        report = []
        
        if self.errors:
            report.append("❌ ERRORS:")
            for error in self.errors:
                report.append(f"   - {error}")
        
        if self.warnings:
            report.append("⚠️  WARNINGS:")
            for warning in self.warnings:
                report.append(f"   - {warning}")
        
        if not self.errors and not self.warnings:
            report.append("✅ All validations passed!")
        
        return "\n".join(report)
```

## Migration Checklist

### Pre-Migration
- [ ] Backup current configuration files
- [ ] Document current Render environment variables
- [ ] Test local development environment
- [ ] Verify all service dependencies

### Migration Steps
- [ ] Create new environment directory structure
- [ ] Move configuration files to appropriate environments
- [ ] Update service configuration loading
- [ ] Configure Render environment variables
- [ ] Remove secrets from repository
- [ ] Update .gitignore file

### Post-Migration Validation
- [ ] Test local development setup
- [ ] Verify staging environment (if applicable)
- [ ] Validate production deployment
- [ ] Check all service health endpoints
- [ ] Verify API functionality
- [ ] Test client portal authentication

### Documentation Updates
- [ ] Update README.md with new environment setup
- [ ] Create environment setup guide
- [ ] Update deployment documentation
- [ ] Create troubleshooting guide

---

This optimization plan provides a comprehensive approach to securing and standardizing the BHIV HR Platform's environment management while maintaining the excellent architecture and deployment strategy already in place.