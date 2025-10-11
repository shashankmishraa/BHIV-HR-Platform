# Semantic Engine Package - Phase 3 Production
# Production implementation with proper dependency management

__version__ = "3.0.0-phase3-production"

from .phase3_engine import (
    Phase3SemanticEngine,
    AdvancedSemanticMatcher, 
    BatchMatcher,
    LearningEngine,
    SemanticJobMatcher
)

__all__ = [
    "Phase3SemanticEngine",
    "AdvancedSemanticMatcher", 
    "BatchMatcher",
    "LearningEngine",
    "SemanticJobMatcher"
]