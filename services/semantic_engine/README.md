# 🤖 Semantic Engine Module

**AI-Powered Candidate Matching System**

## 📁 Module Structure

```
semantic_engine/
├── __init__.py           # Package initialization
├── job_matcher.py        # Basic semantic matching
├── advanced_matcher.py   # Advanced AI algorithms
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

This module is imported by the **Agent Service** (`services/agent/app.py`) to provide AI-powered candidate matching capabilities. The agent service includes fallback mechanisms when semantic matching is unavailable.

## 📊 Performance

- **Response Time**: <0.02 seconds per match
- **Accuracy**: Baseline semantic similarity scoring
- **Scalability**: Handles concurrent matching requests
- **Fallback**: Graceful degradation when modules unavailable