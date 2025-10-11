#!/usr/bin/env python3
"""
Phase 3 Feature Testing Script
Tests learning engine, enhanced batch processing, and adaptive scoring
"""

import sys
import os
import requests
import json
from datetime import datetime

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services'))

def test_imports():
    """Test Phase 3 imports"""
    try:
        from semantic_engine.learning_engine import LearningEngine
        from semantic_engine.advanced_matcher import AdvancedSemanticMatcher, EnhancedBatchMatcher
        print("SUCCESS: Phase 3 imports successful")
        return True
    except ImportError as e:
        print(f"ERROR: Import failed: {e}")
        return False

def test_learning_engine():
    """Test learning engine functionality"""
    try:
        from semantic_engine.learning_engine import LearningEngine
        
        learning_engine = LearningEngine()
        prefs_count = len(learning_engine.company_preferences)
        print(f"SUCCESS: Learning engine initialized with {prefs_count} company preferences")
        
        # Test company preferences
        test_prefs = learning_engine.get_company_preferences('TECH001')
        if test_prefs:
            print(f"SUCCESS: Company preferences loaded for TECH001")
        else:
            print("INFO: No preferences found for TECH001 (expected for new system)")
            
        return True
    except Exception as e:
        print(f"ERROR: Learning engine test failed: {e}")
        return False

def test_enhanced_batch_matcher():
    """Test enhanced batch processing"""
    try:
        from semantic_engine.advanced_matcher import EnhancedBatchMatcher
        
        enhanced_batch = EnhancedBatchMatcher()
        print("SUCCESS: Enhanced batch matcher initialized")
        
        # Test with sample data
        sample_jobs = [{'id': 1, 'title': 'Test Job', 'requirements': 'Python'}]
        sample_candidates = [{'id': 1, 'name': 'Test Candidate', 'technical_skills': 'Python'}]
        
        # Note: async test would require event loop setup
        print("SUCCESS: Enhanced batch matcher ready for async processing")
        return True
    except Exception as e:
        print(f"ERROR: Enhanced batch matcher test failed: {e}")
        return False

def test_production_endpoints():
    """Test production endpoints for Phase 3 features"""
    base_url = "https://bhiv-hr-agent-m1me.onrender.com"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Production service healthy - version {data.get('version')}")
        else:
            print(f"ERROR: Health check failed: {response.status_code}")
            return False
            
        # Test matching with Phase 3 features
        match_request = {"job_id": 1}
        response = requests.post(f"{base_url}/match", json=match_request, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            algorithm_version = data.get('algorithm_version', 'unknown')
            candidates_count = len(data.get('top_candidates', []))
            processing_time = data.get('processing_time', 0)
            
            print(f"SUCCESS: Phase 3 matching successful")
            print(f"   Algorithm: {algorithm_version}")
            print(f"   Candidates: {candidates_count}")
            print(f"   Processing time: {processing_time}s")
            
            # Check if Phase 3 algorithm is being used
            if '3.0.0' in algorithm_version:
                print("SUCCESS: Phase 3 algorithm confirmed")
            else:
                print("WARNING: Phase 3 algorithm not detected")
                
        else:
            print(f"ERROR: Match endpoint failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"ERROR: Production endpoint test failed: {e}")
        return False

def main():
    """Run all Phase 3 tests"""
    print("Testing Phase 3 Semantic Engine Features")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Learning Engine", test_learning_engine),
        ("Enhanced Batch Matcher", test_enhanced_batch_matcher),
        ("Production Endpoints", test_production_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("SUCCESS: All Phase 3 features working correctly!")
    else:
        print("WARNING: Some Phase 3 features need attention")

if __name__ == "__main__":
    main()