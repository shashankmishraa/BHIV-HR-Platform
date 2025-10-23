# HR Portal Service

**Streamlit 1.41.1 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-portal-cead.onrender.com  
**Status**: ✅ Operational  

## Overview

Internal HR dashboard for candidate management, job posting, and AI-powered matching.

## Key Features

- **Dashboard**: Real-time metrics and analytics
- **Candidate Search**: Advanced filtering with AI matching
- **Job Management**: Create and manage job postings
- **Values Assessment**: 5-point BHIV values evaluation
- **Batch Upload**: Secure candidate data import

## Architecture

```
portal/
├── app.py              # Streamlit interface (1500+ lines)
├── batch_upload.py     # Batch processing
├── config.py           # Configuration
├── file_security.py    # File security
├── components/         # UI components
└── requirements.txt    # Streamlit 1.41.1 dependencies
```

## Features

- **Real-time Data**: Live updates from Gateway API
- **Security**: File validation and path traversal protection
- **2FA Integration**: QR code generation with function-level imports
- **Performance**: Optimized Streamlit components

## Local Development

```bash
cd services/portal
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```