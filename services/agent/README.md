# AI Agent Service

**FastAPI 0.115.6 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-agent-m1me.onrender.com  
**Endpoints**: 6 total  
**Status**: ✅ Operational  

## Overview

AI-powered semantic candidate matching service with Phase 3 learning capabilities.

## Key Features

- **Phase 3 Semantic Engine**: Production-grade NLP processing
- **Batch Processing**: Multiple job matching optimization
- **Learning Algorithms**: Company preference tracking
- **Real-time Analysis**: <0.02 second response time

## Architecture

```
agent/
├── app.py                  # FastAPI AI service (600+ lines)
├── semantic_engine/        # Phase 3 AI engine
│   ├── __init__.py
│   └── phase3_engine.py
└── requirements.txt        # AI/ML dependencies
```

## Endpoints

- **Core** (2): GET /, GET /health
- **AI Processing** (3): POST /match, POST /batch-match, GET /analyze/{candidate_id}
- **Diagnostics** (1): GET /test-db

## AI Features

- **Semantic Matching**: Advanced sentence transformers
- **Adaptive Scoring**: Company-specific weight optimization
- **Cultural Fit Analysis**: Feedback-based alignment (10% bonus)
- **Multi-Factor Scoring**: Semantic (40%), Experience (30%), Skills (20%), Location (10%)

## Local Development

```bash
cd services/agent
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 9000 --reload
```