"""
BHIV HR Platform - Semantic Engine Package
Version: 3.0.0-phase3-advanced
Updated: October 13, 2025
Status: Production Ready (Local), Offline (Production)

Advanced AI-powered semantic matching for HR platform with:
- Phase 3 learning engine with company preference optimization
- Sentence transformer-based semantic similarity
- Cultural fit analysis with feedback integration
- Enhanced batch processing with smart caching
- Adaptive scoring algorithms

Production Status: Available locally, offline in production due to ML dependencies
"""

from .phase3_engine import (
    Phase3SemanticEngine,
    AdvancedSemanticMatcher,
    BatchMatcher,
    LearningEngine,
    SemanticJobMatcher
)

__version__ = "3.0.0-phase3-advanced"
__status__ = "Production Ready (Local)"
__updated__ = "2025-10-13"

__all__ = [
    'Phase3SemanticEngine',
    'AdvancedSemanticMatcher', 
    'BatchMatcher',
    'LearningEngine',
    'SemanticJobMatcher'
]