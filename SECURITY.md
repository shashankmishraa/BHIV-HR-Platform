# Security Policy

## Supported Versions

The following versions of BHIV HR Platform are currently supported with security updates:

| Version | Supported          | Status        |
|---------|-------------------|--------------|
| 3.2.x   | :white_check_mark: | Current       |
| 3.1.x   | :white_check_mark: | LTS           |
| 3.0.x   | :x:                | End of Life   |
| < 3.0   | :x:                | Deprecated    |

## Security Features

BHIV HR Platform implements enterprise-grade security:

- **Authentication**: JWT tokens with Bearer authentication
- **API Security**: Rate limiting (60 req/min), CORS protection
- **Data Protection**: SQL injection prevention, XSS protection
- **2FA Support**: TOTP compatible (Google/Microsoft/Authy)
- **Monitoring**: Real-time security event tracking
- **Audit Logging**: Comprehensive security event logs
- **Session Management**: Advanced session tracking and cleanup
- **Threat Detection**: Automated security monitoring

## Reporting a Vulnerability

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. **Email**: Send reports to security@bhiv-hr-platform.com
3. **GitHub Security**: Use private security advisories

### Report Contents

Please include:
- Detailed description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Suggested fix (if applicable)
- Your contact information for follow-up

### Response Timeline

- **Acknowledgment**: Within 24 hours
- **Initial Assessment**: Within 72 hours
- **Status Update**: Weekly updates on progress
- **Resolution**: Target 30 days for critical issues

### Security Updates

- Critical vulnerabilities: Immediate patch release
- High severity: 7-day patch release
- Medium severity: Next scheduled release
- Low severity: Quarterly security review

### Disclosure Policy

- Coordinated disclosure after fix is available
- Credit will be given to security researchers
- CVE numbers assigned for qualifying vulnerabilities
- Security advisories published for transparency

## Security Contact

- **Primary**: security@bhiv-hr-platform.com
- **Backup**: shashankmishraa@github.com
- **GPG Key**: Available upon request

## Security Acknowledgments

We thank the security research community for helping keep BHIV HR Platform secure.

---

**Last Updated**: January 2025  
**Version**: 3.2.0  
**Classification**: Public
