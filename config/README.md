# BHIV HR Platform - Configuration Management

## Security Overview

This directory contains configuration management tools and templates for secure environment setup.

## Files

### Templates (Safe to Commit)
- `environments.py` - Environment-specific configuration classes
- `env-management.py` - Environment validation and management tools
- `README.md` - This documentation

### Environment Files (NEVER COMMIT)
- `.env` - Local development environment (create from .env.example)
- `.env.production` - Production environment variables
- `.env.staging` - Staging environment variables

## Security Guidelines

### 1. Environment File Management
```bash
# Create local environment file
cp ../.env.example .env
# Edit with secure values - NEVER COMMIT THIS FILE
```

### 2. Required Environment Variables
```bash
# Database - Use strong passwords
DATABASE_URL=postgresql://username:SECURE_PASSWORD@host:5432/database
POSTGRES_USER=bhiv_user
POSTGRES_PASSWORD=GENERATE_32_CHAR_PASSWORD
POSTGRES_DB=bhiv_hr

# API Security - Generate cryptographically secure keys
API_KEY_SECRET=GENERATE_SECURE_32_CHAR_API_KEY
CLIENT_ACCESS_CODE=GENERATE_SECURE_CLIENT_CODE
```

### 3. Security Validation
```bash
# Validate current configuration
python env-management.py

# Run security audit
python ../tools/security_audit.py
```

## Deployment Environments

### Development
- Use `.env` file for local development
- Safe to use demo values for testing
- Never commit actual .env file

### Staging
- Use environment variables in deployment platform
- Test with production-like data
- Validate security configuration

### Production
- Use secure environment variable management
- Rotate secrets regularly
- Monitor for security issues

## Best Practices

### Secret Management
1. **Never commit actual secrets** to repository
2. **Use strong, unique passwords** for each environment
3. **Rotate secrets regularly** (quarterly minimum)
4. **Use environment-specific values** - no shared secrets

### Configuration Validation
1. **Run security audits** before deployment
2. **Validate environment** configuration
3. **Test with secure values** in staging
4. **Monitor for configuration drift**

### Access Control
1. **Limit access** to production environment variables
2. **Use principle of least privilege**
3. **Audit access logs** regularly
4. **Implement approval workflows** for changes

## Troubleshooting

### Common Issues
1. **Missing environment variables** - Check required variables list
2. **Insecure default values** - Generate secure replacements
3. **Configuration drift** - Use validation tools regularly

### Security Incidents
1. **Immediately rotate** any exposed secrets
2. **Update all environments** with new values
3. **Audit access logs** for unauthorized usage
4. **Document incident** and remediation steps

## Tools

### Environment Management
```bash
# Validate configuration
python env-management.py

# Generate secure template
python env-management.py --generate-template
```

### Security Audit
```bash
# Run comprehensive security audit
python ../tools/security_audit.py

# Check for committed secrets
git log --all --full-history -- .env config/*.env
```

## Support

For security-related issues:
1. **Do not** include actual secrets in issue reports
2. **Use secure channels** for sensitive information
3. **Follow incident response** procedures
4. **Document remediation** steps taken