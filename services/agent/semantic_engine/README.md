# 🤖 Semantic Engine Module v4.1.0

**AI-Powered Candidate Matching System**

**Updated**: January 18, 2025 | **Python**: 3.12.7 | **Status**: ✅ Production Ready

## 🌐 Live Integration
- **Agent Service**: https://bhiv-hr-agent-o6nx.onrender.com
- **Performance**: <0.02s per match
- **Accuracy**: Advanced semantic analysis
- **Fallback**: Graceful degradation available

## 📁 Module Structure

```
semantic_engine/
├── __init__.py           # Package initialization
├── job_matcher.py        # Basic semantic matching
├── advanced_matcher.py   # Advanced AI algorithms
├── model_manager.py      # ML model management
├── semantic_processor.py # Core processing engine
└── README.md            # This file
```

## 🔧 Components

### SemanticJobMatcher
- **Purpose**: Basic job-candidate semantic matching
- **Usage**: Fallback matching when advanced algorithms unavailable
- **Returns**: Similarity scores between job requirements and candidate skills

### AdvancedSemanticMatcher  
- **Purpose**: Advanced AI-powered matching with reasoning
- **Features**: Multi-factor analysis, bias mitigation, detailed scoring
- **Returns**: Comprehensive match analysis with explanations

### BatchMatcher
- **Purpose**: Process multiple candidates simultaneously
- **Optimization**: Efficient bulk matching operations
- **Use Case**: Large-scale candidate screening

## 🚀 Usage Example

```python
from services.semantic_engine.job_matcher import SemanticJobMatcher
from services.semantic_engine.advanced_matcher import AdvancedSemanticMatcher

# Basic matching
matcher = SemanticJobMatcher()
score = matcher.match(job_requirements, candidate_skills)

# Advanced matching
advanced = AdvancedSemanticMatcher()
result = advanced.advanced_match(job_data, candidate_data)
```

## 🔄 Integration

This module is imported by the **Agent Service** (`services/agent/app.py`) to provide AI-powered candidate matching capabilities. 

### **Current Status**
- **Live Service**: https://bhiv-hr-agent-o6nx.onrender.com/docs
- **Endpoints**: 15 AI matching endpoints
- **Fallback**: Robust fallback algorithms available
- **Monitoring**: Comprehensive health checks integrated

## 📊 Performance

- **Response Time**: <0.02 seconds per match
- **Accuracy**: Baseline semantic similarity scoring
- **Scalability**: Handles concurrent matching requests
- **Fallback**: Graceful degradation when modules unavailable