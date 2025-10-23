# Client Portal Service

**Streamlit 1.41.1 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-client-portal-5g33.onrender.com  
**Status**: ✅ Operational  

## Overview

External client interface for enterprise job posting and candidate review.

## Key Features

- **Enterprise Authentication**: JWT-based secure login
- **Job Posting**: Create and manage job listings
- **Candidate Review**: Access AI-matched candidates
- **Interview Coordination**: Schedule and manage interviews
- **Real-time Sync**: Instant updates with HR portal

## Architecture

```
client_portal/
├── app.py              # Client interface (800+ lines)
├── auth_service.py     # Enterprise authentication
├── config.py           # Configuration
└── requirements.txt    # Streamlit dependencies
```

## Authentication

- **Demo Credentials**: TECH001 / demo123
- **JWT Tokens**: Secure session management
- **Account Protection**: Lockout and session timeout

## Local Development

```bash
cd services/client_portal
pip install -r requirements.txt
streamlit run app.py --server.port 8502
```