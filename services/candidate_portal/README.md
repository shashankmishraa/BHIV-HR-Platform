# Candidate Portal Service

**Streamlit 1.41.1 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-candidate-portal.onrender.com  
**Status**: ✅ Operational  

## Overview

Job seeker interface for registration, job search, and application management.

## Key Features

- **Registration**: Secure account creation with validation
- **Profile Management**: Comprehensive candidate information
- **Job Search**: Browse and filter available positions
- **Application Tracking**: Submit applications and monitor status
- **Dashboard**: Personal overview of applications and activity

## Architecture

```
candidate_portal/
├── app.py              # Job seeker interface
├── config.py           # Configuration
└── requirements.txt    # Streamlit dependencies
```

## Features

- **Real-time Updates**: Live job postings and application status
- **Resume Upload**: Multi-format file support
- **Secure Authentication**: Password hashing with bcrypt
- **Application Management**: Track application history

## Local Development

```bash
cd services/candidate_portal
pip install -r requirements.txt
streamlit run app.py --server.port 8503
```