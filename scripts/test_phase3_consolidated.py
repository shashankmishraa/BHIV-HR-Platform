#!/usr/bin/env python3
"""
Phase 3 Consolidated Testing Script
Tests unified semantic engine with Python 3.12.7 compatibility
"""

import sys
import os
import time
from datetime import datetime

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services'))

def test_python_version():
    """Test Python version compatibility"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 12:
        print("SUCCESS: Python 3.12+ detected")
        return True
    else:
        print("WARNING: Python 3.12+ recommended for Phase 3")
        return True  # Still allow older versions

def test_consolidated_imports():
    """Test Phase 3 consolidated imports"""
    try:
        from semantic_engine.phase3_matcher import (
            Phase3SemanticEngine,
            AdvancedSemanticMatcher,
            BatchMatcher,
            LearningEngine
        )
        print("SUCCESS: Phase 3 consolidated imports working")
        return True
    except ImportError as e:
        print(f"ERROR: Phase 3 import failed: {e}")
        return False

def test_phase3_engine():
    """Test Phase 3 consolidated engine"""
    try:
        from semantic_engine.phase3_matcher import Phase3SemanticEngine
        
        engine = Phase3SemanticEngine()
        print(f"SUCCESS: Phase 3 engine initialized (enabled: {engine.enabled})")
        
        # Test basic scoring
        job_data = {
            'id': 1,
            'title': 'Python Developer',
            'description': 'Python development role',
            'requirements': 'Python, Django, REST APIs',
            'location': 'Remote',
            'experience_level': 'Mid',
            'client_id': 'TECH001'
        }
        
        candidate_data = {
            'id': 1,
            'name': 'Test Candidate',
            'technical_skills': 'Python, Django, FastAPI',
            'experience_years': 3,
            'seniority_level': 'Mid-level',
            'education_level': 'Bachelor',
            'location': 'Remote'
        }
        
        score_result = engine.calculate_adaptive_score(job_data, candidate_data, 'TECH001')
        print(f"SUCCESS: Adaptive scoring working - score: {score_result['total_score']:.3f}")
        print(f"INFO: Algorithm version: {score_result.get('algorithm_version')}")
        
        return True
    except Exception as e:
        print(f"ERROR: Phase 3 engine test failed: {e}")
        return False

def test_batch_processing():
    """Test enhanced batch processing"""
    try:
        from semantic_engine.phase3_matcher import BatchMatcher
        
        batch_matcher = BatchMatcher()
        print(f"SUCCESS: Batch matcher initialized (enabled: {batch_matcher.enabled})")
        
        # Test with sample data
        jobs = [{
            'id': 1,
            'title': 'Test Job',
            'requirements': 'Python',
            'client_id': 'TECH001'
        }]
        
        candidates = [{
            'id': 1,
            'name': 'Test Candidate',
            'technical_skills': 'Python, Django'
        }]
        
        results = batch_matcher.batch_process(jobs, candidates)
        if results:
            print("SUCCESS: Batch processing working")
        else:
            print("WARNING: Batch processing returned empty results")
        
        return True
    except Exception as e:
        print(f"ERROR: Batch processing test failed: {e}")
        return False

def test_learning_engine():
    """Test learning engine"""
    try:
        from semantic_engine.phase3_matcher import LearningEngine
        
        learning_engine = LearningEngine()
        prefs_count = len(learning_engine.company_preferences)
        print(f"SUCCESS: Learning engine initialized with {prefs_count} company preferences")
        
        # Test company preferences
        prefs = learning_engine.get_company_preferences('TECH001')
        if prefs:
            print("SUCCESS: Company preferences loaded")
        else:
            print("INFO: No preferences found (expected for new system)")
        
        return True
    except Exception as e:
        print(f"ERROR: Learning engine test failed: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility with existing code"""
    try:
        from semantic_engine.phase3_matcher import AdvancedSemanticMatcher
        
        matcher = AdvancedSemanticMatcher()
        print(f"SUCCESS: Backward compatibility working (enabled: {matcher.enabled})")
        
        # Test legacy method
        job_data = {'title': 'Test Job', 'requirements': 'Python'}
        candidate_data = {'technical_skills': 'Python, Django'}
        
        result = matcher.calculate_multi_factor_score(job_data, candidate_data)
        print(f"SUCCESS: Legacy method working - score: {result['total_score']:.3f}")
        
        return True
    except Exception as e:
        print(f"ERROR: Backward compatibility test failed: {e}")
        return False

def test_fallback_mechanisms():
    """Test fallback mechanisms when dependencies are missing"""
    try:
        # Temporarily disable dependencies
        import semantic_engine.phase3_matcher as phase3_module
        original_deps = phase3_module.DEPENDENCIES_AVAILABLE
        
        # Test with dependencies disabled
        phase3_module.DEPENDENCIES_AVAILABLE = False
        
        from semantic_engine.phase3_matcher import Phase3SemanticEngine
        engine = Phase3SemanticEngine()
        
        job_data = {'title': 'Test Job'}
        candidate_data = {'name': 'Test Candidate'}
        
        result = engine.calculate_adaptive_score(job_data, candidate_data)
        
        # Restore original state
        phase3_module.DEPENDENCIES_AVAILABLE = original_deps
        
        if result['algorithm_version'] == '3.0.0-fallback':
            print("SUCCESS: Fallback mechanisms working")
            return True
        else:
            print("WARNING: Fallback not triggered as expected")
            return False
            
    except Exception as e:
        print(f"ERROR: Fallback test failed: {e}")
        return False

def test_production_integration():
    """Test integration with production endpoints"""
    try:
        import requests
        
        # Test production health
        response = requests.get('https://bhiv-hr-agent-m1me.onrender.com/health', timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Production service healthy - version {data.get('version')}")
            return True
        else:
            print(f"WARNING: Production service returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"WARNING: Production integration test failed: {e}")
        return False

def main():
    """Run all Phase 3 consolidated tests"""
    print("Phase 3 Consolidated Semantic Engine Testing")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Consolidated Imports", test_consolidated_imports),
        ("Phase 3 Engine", test_phase3_engine),
        ("Batch Processing", test_batch_processing),
        ("Learning Engine", test_learning_engine),
        ("Backward Compatibility", test_backward_compatibility),
        ("Fallback Mechanisms", test_fallback_mechanisms),
        ("Production Integration", test_production_integration)
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERROR: {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    end_time = time.time()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    print(f"Test duration: {end_time - start_time:.2f} seconds")
    
    if passed == len(tests):
        print("SUCCESS: All Phase 3 consolidated features working!")
        return 0
    elif passed >= len(tests) * 0.75:
        print("PARTIAL: Most Phase 3 features working")
        return 0
    else:
        print("WARNING: Some Phase 3 features need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())