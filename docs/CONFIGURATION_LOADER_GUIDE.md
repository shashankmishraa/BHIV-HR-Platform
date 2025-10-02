# ⚙️ BHIV HR Platform - Configuration Loader Guide

**File**: `config/environment_loader.py`  
**Version**: 3.1.0  
**Last Updated**: January 2025  
**Status**: Production Configuration Management System

---

## 📊 Overview

The Configuration Loader is a centralized configuration management system that handles environment-specific settings, validation, and secure configuration loading across all BHIV HR Platform services.

### **Key Features**
- **Environment-Aware**: Automatic environment detection (local/staging/production)
- **Secure Loading**: Safe handling of sensitive configuration data
- **Validation**: Comprehensive configuration validation
- **Type Conversion**: Automatic type conversion for configuration values
- **Fallback Support**: Default values and graceful degradation

---

## 🏗️ Architecture Overview

### **Configuration Hierarchy**
```
Configuration Loading Order:
1. Base Configuration (shared/base.env)
2. Environment-Specific Config (environments/{env}/.env)
3. Environment Variables (OS-level overrides)
4. Validation & Type Conversion
```

### **File Structure**
```
config/
├── environment_loader.py      # Main configuration loader
├── .env.render               # Render platform config
└── production.env            # Production settings

environments/
├── local/
│   ├── .env.template         # Local development template
│   └── docker-compose.yml    # Local Docker setup
├── staging/
│   └── .env.template         # Staging template
├── production/
│   └── .env.template         # Production template
└── shared/
    └── base.env              # Base configuration
```

---

## 🔧 Configuration Loader Usage

### **Basic Usage**
```python
from config.environment_loader import get_config

# Get configuration instance
config = get_config()

# Access configuration values
database_url = config.get('DATABASE_URL')
api_key = config.get('API_KEY_SECRET')
debug_mode = config.get_bool('DEBUG', False)
port = config.get_int('PORT', 8000)
```

### **Environment-Specific Loading**
```python
# Load specific environment
config = get_config('production')
config = get_config('staging')
config = get_config('local')

# Auto-detect environment
config = get_config()  # Uses ENVIRONMENT variable
```

### **Type-Safe Access Methods**
```python
# String values (default)
database_url = config.get('DATABASE_URL', 'default_url')

# Integer values
port = config.get_int('PORT', 8000)
pool_size = config.get_int('DATABASE_POOL_SIZE', 10)

# Boolean values
debug = config.get_bool('DEBUG', False)
enable_2fa = config.get_bool('ENABLE_2FA', True)

# Float values
timeout = config.get_float('REQUEST_TIMEOUT', 30.0)

# List values
cors_origins = config.get_list('CORS_ORIGINS', separator=',')
```

---

## 📋 Configuration Categories

### **Database Configuration**
```python
# Get database configuration
db_config = config.get_database_config()

# Returns:
{
    'url': 'postgresql://...',
    'pool_size': 10,
    'pool_timeout': 30,
    'max_overflow': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'echo': False
}
```

### **Security Configuration**
```python
# Get security configuration
security_config = config.get_security_config()

# Returns:
{
    'api_key_secret': '<secure_key>',
    'jwt_secret_key': '<jwt_secret>',
    'jwt_algorithm': 'HS256',
    'jwt_expiration_hours': 24,
    'bcrypt_rounds': 12,
    'enable_2fa': True,
    'enable_rate_limiting': True
}
```

### **Service URLs Configuration**
```python
# Get service URLs
service_urls = config.get_service_urls()

# Returns:
{
    'gateway': 'https://bhiv-hr-gateway-46pz.onrender.com',
    'agent': 'https://bhiv-hr-agent-m1me.onrender.com',
    'portal': 'https://bhiv-hr-portal-cead.onrender.com',
    'client_portal': 'https://bhiv-hr-client-portal-5g33.onrender.com'
}
```

---

## 🔒 Security Features

### **Secure Configuration Handling**
```python
# Environment variable substitution
DATABASE_URL=${DATABASE_URL}
API_KEY=${API_KEY_SECRET}

# Quote handling
DEBUG="true"
LOG_LEVEL='INFO'

# Sensitive data protection
config.get('PASSWORD')  # Returns masked value in logs
```

### **Validation System**
```python
# Configuration validation
validation_result = config.validator.validate_all(config.config)

if validation_result.errors:
    # Handle validation errors
    for error in validation_result.errors:
        logger.error(f"Configuration error: {error}")

if validation_result.warnings:
    # Handle validation warnings
    for warning in validation_result.warnings:
        logger.warning(f"Configuration warning: {warning}")
```

---

## 🌍 Environment Management

### **Environment Detection**
```python
# Check current environment
if config.is_production():
    # Production-specific logic
    pass

if config.is_development():
    # Development-specific logic
    pass

if config.is_staging():
    # Staging-specific logic
    pass
```

### **Environment-Specific Behavior**
```python
# Production environment
if config.is_production():
    # Strict validation
    # No debug output
    # Secure defaults
    
# Development environment
if config.is_development():
    # Relaxed validation
    # Debug output enabled
    # Development defaults
```

---

## 📝 Configuration File Formats

### **Environment File Format (.env)**
```bash
# Database Configuration
DATABASE_URL=postgresql://user:pass@host:port/db
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30

# API Security
API_KEY_SECRET=<secure_api_key>
JWT_SECRET_KEY=<secure_jwt_secret>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Service Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false

# Feature Flags
ENABLE_2FA=true
ENABLE_RATE_LIMITING=true
ENABLE_MONITORING=true

# Service URLs
GATEWAY_SERVICE_URL=https://gateway.example.com
AGENT_SERVICE_URL=https://agent.example.com
```

### **Docker Compose Integration**
```python
# Export configuration for Docker Compose
docker_config = config.export_for_docker()

# Use in docker-compose.yml
services:
  gateway:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY_SECRET=${API_KEY_SECRET}
```

---

## 🔧 Advanced Features

### **Configuration Reloading**
```python
# Reload configuration
config = reload_config('production')

# Force reload with new environment
config = reload_config()
```

### **Configuration Validation**
```python
class ConfigValidator:
    def validate_database_url(self, url):
        # Validate database URL format
        pass
    
    def validate_api_key(self, key):
        # Validate API key strength
        pass
    
    def validate_jwt_secret(self, secret):
        # Validate JWT secret strength
        pass
```

### **Custom Configuration Sources**
```python
# Load from custom file
config.load_from_file('/path/to/custom.env')

# Load from dictionary
config.load_from_dict({
    'DATABASE_URL': 'postgresql://...',
    'API_KEY_SECRET': 'secure_key'
})
```

---

## 🚀 Integration Examples

### **FastAPI Integration**
```python
from fastapi import FastAPI
from config.environment_loader import get_config

app = FastAPI()
config = get_config()

# Use configuration in FastAPI
@app.on_event("startup")
async def startup_event():
    database_url = config.get('DATABASE_URL')
    # Initialize database connection
```

### **Streamlit Integration**
```python
import streamlit as st
from config.environment_loader import get_config

config = get_config()

# Use configuration in Streamlit
st.title("BHIV HR Platform")
if config.is_development():
    st.sidebar.text("Development Mode")
```

### **Database Integration**
```python
from sqlalchemy import create_engine
from config.environment_loader import get_config

config = get_config()
db_config = config.get_database_config()

engine = create_engine(
    db_config['url'],
    pool_size=db_config['pool_size'],
    pool_timeout=db_config['pool_timeout'],
    max_overflow=db_config['max_overflow']
)
```

---

## 🔍 Troubleshooting

### **Common Issues**

#### **Configuration Not Found**
```python
# Issue: Configuration file not found
# Solution: Check file paths and environment
config = get_config('production')
if not config.get('DATABASE_URL'):
    logger.error("Database URL not configured")
```

#### **Type Conversion Errors**
```python
# Issue: Invalid type conversion
# Solution: Use type-safe methods with defaults
port = config.get_int('PORT', 8000)  # Safe with default
timeout = config.get_float('TIMEOUT', 30.0)  # Safe with default
```

#### **Environment Variable Override**
```python
# Issue: Environment variables not overriding
# Solution: Check environment variable names
import os
os.environ['DATABASE_URL'] = 'new_url'
config = reload_config()  # Reload to pick up changes
```

### **Debugging Configuration**
```python
# Debug configuration loading
config = get_config()
print(f"Environment: {config.environment}")
print(f"Config keys: {list(config.config.keys())}")
print(f"Database configured: {'DATABASE_URL' in config.config}")
```

---

## 📊 Performance Considerations

### **Configuration Caching**
- Configuration is loaded once and cached
- Use `reload_config()` only when necessary
- Environment detection is cached for performance

### **Memory Usage**
- Configuration values are stored in memory
- Large configuration files may impact startup time
- Consider lazy loading for large configurations

### **Startup Performance**
```python
# Optimize startup time
config = get_config()  # Load once at startup
database_url = config.get('DATABASE_URL')  # Fast access
```

---

## 🛡️ Security Best Practices

### **Sensitive Data Handling**
1. **Never commit secrets** to version control
2. **Use environment variables** for sensitive data
3. **Validate configuration** before use
4. **Log configuration** without sensitive values
5. **Use secure defaults** for production

### **Configuration Security**
```python
# Secure configuration access
api_key = config.get('API_KEY_SECRET')
if not api_key:
    raise ValueError("API key not configured")

# Validate configuration in production
if config.is_production():
    validation_result = config.validator.validate_all(config.config)
    if validation_result.errors:
        raise ValueError("Invalid production configuration")
```

---

## 📈 Monitoring & Logging

### **Configuration Monitoring**
```python
# Log configuration status
logger.info(f"Configuration loaded: {config.environment}")
logger.info(f"Database configured: {bool(config.get('DATABASE_URL'))}")
logger.info(f"Security features enabled: {config.get_bool('ENABLE_2FA')}")
```

### **Health Checks**
```python
def configuration_health_check():
    config = get_config()
    
    health = {
        'database_configured': bool(config.get('DATABASE_URL')),
        'api_key_configured': bool(config.get('API_KEY_SECRET')),
        'environment': config.environment,
        'validation_status': 'valid'
    }
    
    return health
```

---

## 🎯 Best Practices

### **Configuration Management**
1. **Use environment-specific files** for different deployments
2. **Validate configuration** at startup
3. **Provide sensible defaults** for optional settings
4. **Document all configuration options**
5. **Use type-safe access methods**

### **Development Workflow**
1. **Copy .env.template** to .env for local development
2. **Never commit .env files** with secrets
3. **Use environment variables** in production
4. **Test configuration changes** in staging first
5. **Document configuration requirements**

---

**Configuration Loader Guide Complete**  
**Status**: ✅ Production Ready  
**Security**: ✅ Secure Configuration Management  
**Integration**: ✅ All Services Supported