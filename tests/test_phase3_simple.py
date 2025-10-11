#!/usr/bin/env python3
"""
Phase 3 Production Test - Simple Version
Tests Phase 3 semantic engine without fallbacks
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_dependencies():
    """Test Phase 3 dependencies"""
    print("Testing Phase 3 dependencies...")
    
    try:
        import sentence_transformers
        print(f"[PASS] sentence-transformers: {sentence_transformers.__version__}")
    except ImportError as e:
        print(f"[FAIL] sentence-transformers: {e}")
        return False
    
    try:
        import sklearn
        print(f"[PASS] scikit-learn: {sklearn.__version__}")
    except ImportError as e:
        print(f"[FAIL] scikit-learn: {e}")
        return False
    
    try:
        import numpy as np
        print(f"[PASS] numpy: {np.__version__}")
    except ImportError as e:
        print(f"[FAIL] numpy: {e}")
        return False
    
    return True

def test_engine_import():
    """Test Phase 3 engine import"""
    print("\nTesting Phase 3 engine import...")
    
    try:
        from services.semantic_engine.phase3_engine import (
            Phase3SemanticEngine,
            AdvancedSemanticMatcher,
            BatchMatcher,
            LearningEngine
        )
        print("[PASS] Phase 3 engine imports successful")
        return True
    except ImportError as e:
        print(f"[FAIL] Phase 3 engine import: {e}")
        return False

def test_engine_init():
    """Test Phase 3 engine initialization"""
    print("\nTesting Phase 3 engine initialization...")
    
    try:
        from services.semantic_engine.phase3_engine import Phase3SemanticEngine
        engine = Phase3SemanticEngine()
        print("[PASS] Phase 3 engine initialized")
        
        if engine.model is not None:
            print("[PASS] Sentence transformer model loaded")
        else:
            print("[FAIL] Sentence transformer model not loaded")
            return False
        
        return True
    except Exception as e:
        print(f"[FAIL] Phase 3 engine initialization: {e}")
        return False

def test_semantic_matching():
    """Test Phase 3 semantic matching"""
    print("\nTesting Phase 3 semantic matching...")
    
    try:
        from services.semantic_engine.phase3_engine import Phase3SemanticEngine
        engine = Phase3SemanticEngine()
        
        job_data = {
            'id': 1,
            'title': 'Senior Python Developer',
            'description': 'Python developer with Django experience',
            'requirements': 'Python, Django, REST APIs',
            'location': 'Remote',
            'experience_level': 'Senior'
        }
        
        candidate_data = {
            'id': 1,
            'name': 'Test Candidate',
            'technical_skills': 'Python, Django, FastAPI',
            'experience_years': 5,
            'seniority_level': 'Senior',
            'location': 'Mumbai'
        }
        
        result = engine.calculate_adaptive_score(job_data, candidate_data)
        
        if 'total_score' in result and 'breakdown' in result:
            score = result['total_score']
            print(f"[PASS] Adaptive scoring: {score:.3f}")
            print(f"  Semantic: {result['breakdown']['semantic_similarity']:.3f}")
            print(f"  Experience: {result['breakdown']['experience_match']:.3f}")
            print(f"  Skills: {result['breakdown']['skills_match']:.3f}")
            return True
        else:
            print("[FAIL] Invalid scoring result")
            return False
            
    except Exception as e:
        print(f"[FAIL] Semantic matching: {e}")
        return False

def test_agent_import():
    """Test agent service can import Phase 3 engine"""
    print("\nTesting agent service import...")
    
    try:
        # Test the import that agent service uses
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "services"))
        
        from semantic_engine.phase3_engine import (
            Phase3SemanticEngine,
            AdvancedSemanticMatcher,
            BatchMatcher,
            LearningEngine,
            SemanticJobMatcher
        )
        
        # Test initialization like agent service does
        phase3_engine = Phase3SemanticEngine()
        advanced_matcher = AdvancedSemanticMatcher()
        batch_matcher = BatchMatcher()
        learning_engine = LearningEngine()
        
        print("[PASS] Agent service imports successful")
        print("[PASS] All Phase 3 components initialized")
        return True
        
    except Exception as e:
        print(f"[FAIL] Agent service import: {e}")
        return False

def run_tests():
    """Run all tests"""
    print("=" * 50)
    print("PHASE 3 PRODUCTION TEST")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Engine Import", test_engine_import),
        ("Engine Init", test_engine_init),
        ("Semantic Matching", test_semantic_matching),
        ("Agent Import", test_agent_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"[CRASH] {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: Phase 3 Production Ready!")
    else:
        print("FAILURE: Phase 3 needs fixes")
    
    print("=" * 50)
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)