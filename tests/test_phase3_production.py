#!/usr/bin/env python3
"""
Phase 3 Production Test Suite
Tests Phase 3 semantic engine without fallbacks
"""
import sys
import os
import requests
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_phase3_dependencies():
    """Test Phase 3 dependencies are properly installed"""
    print("Testing Phase 3 dependencies...")
    
    try:
        import sentence_transformers
        print(f"✓ sentence-transformers: {sentence_transformers.__version__}")
    except ImportError as e:
        print(f"✗ sentence-transformers not available: {e}")
        return False
    
    try:
        import sklearn
        print(f"✓ scikit-learn: {sklearn.__version__}")
    except ImportError as e:
        print(f"✗ scikit-learn not available: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✓ numpy: {np.__version__}")
    except ImportError as e:
        print(f"✗ numpy not available: {e}")
        return False
    
    return True

def test_phase3_engine_import():
    """Test Phase 3 engine can be imported"""
    print("\nTesting Phase 3 engine import...")
    
    try:
        from services.semantic_engine.phase3_engine import (
            Phase3SemanticEngine,
            AdvancedSemanticMatcher,
            BatchMatcher,
            LearningEngine
        )
        print("✓ Phase 3 engine imports successful")
        return True
    except ImportError as e:
        print(f"✗ Phase 3 engine import failed: {e}")
        return False

def test_phase3_engine_initialization():
    """Test Phase 3 engine initialization"""
    print("\nTesting Phase 3 engine initialization...")
    
    try:
        from services.semantic_engine.phase3_engine import Phase3SemanticEngine
        engine = Phase3SemanticEngine()
        print("✓ Phase 3 engine initialized successfully")
        
        # Test model is loaded
        if engine.model is not None:
            print("✓ Sentence transformer model loaded")
        else:
            print("✗ Sentence transformer model not loaded")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Phase 3 engine initialization failed: {e}")
        return False

def test_phase3_semantic_matching():
    """Test Phase 3 semantic matching functionality"""
    print("\nTesting Phase 3 semantic matching...")
    
    try:
        from services.semantic_engine.phase3_engine import Phase3SemanticEngine
        engine = Phase3SemanticEngine()
        
        # Test data
        job_data = {
            'id': 1,
            'title': 'Senior Python Developer',
            'description': 'We need a senior Python developer with Django experience',
            'requirements': 'Python, Django, REST APIs, PostgreSQL',
            'location': 'Remote',
            'experience_level': 'Senior'
        }
        
        candidate_data = {
            'id': 1,
            'name': 'Test Candidate',
            'technical_skills': 'Python, Django, FastAPI, PostgreSQL, Docker',
            'experience_years': 5,
            'seniority_level': 'Senior',
            'location': 'Mumbai'
        }
        
        # Test adaptive scoring
        result = engine.calculate_adaptive_score(job_data, candidate_data)
        
        if 'total_score' in result and 'breakdown' in result:
            print(f"✓ Adaptive scoring successful: {result['total_score']:.3f}")
            print(f"  - Semantic similarity: {result['breakdown']['semantic_similarity']:.3f}")
            print(f"  - Experience match: {result['breakdown']['experience_match']:.3f}")
            print(f"  - Skills match: {result['breakdown']['skills_match']:.3f}")
            print(f"  - Location match: {result['breakdown']['location_match']:.3f}")
            return True
        else:
            print("✗ Adaptive scoring returned invalid result")
            return False
            
    except Exception as e:
        print(f"✗ Phase 3 semantic matching failed: {e}")
        return False

def test_phase3_batch_processing():
    """Test Phase 3 batch processing"""
    print("\nTesting Phase 3 batch processing...")
    
    try:
        from services.semantic_engine.phase3_engine import BatchMatcher
        batch_matcher = BatchMatcher()
        
        # Test data
        jobs = [{
            'id': 1,
            'title': 'Python Developer',
            'description': 'Python development role',
            'requirements': 'Python, Django',
            'location': 'Remote',
            'experience_level': 'Mid'
        }]
        
        candidates = [{
            'id': 1,
            'name': 'Test Candidate',
            'technical_skills': 'Python, Django, FastAPI',
            'experience_years': 3,
            'seniority_level': 'Mid',
            'location': 'Mumbai'
        }]
        
        # Test batch processing
        results = batch_matcher.batch_process(jobs, candidates)
        
        if results and len(results) > 0:
            print(f"✓ Batch processing successful: {len(results)} job(s) processed")
            return True
        else:
            print("✗ Batch processing returned no results")
            return False
            
    except Exception as e:
        print(f"✗ Phase 3 batch processing failed: {e}")
        return False

def test_agent_service_endpoints():
    """Test agent service endpoints"""
    print("\nTesting agent service endpoints...")
    
    base_url = "http://localhost:9000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('version') == '3.0.0':
                print("✓ Health endpoint returns Phase 3 version")
            else:
                print(f"✗ Health endpoint version mismatch: {data.get('version')}")
                return False
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('version') == '3.0.0':
                print("✓ Root endpoint returns Phase 3 version")
            else:
                print(f"✗ Root endpoint version mismatch: {data.get('version')}")
                return False
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Agent service not accessible: {e}")
        return False

def test_production_gateway_endpoints():
    """Test production gateway endpoints"""
    print("\nTesting production gateway endpoints...")
    
    base_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✓ Production gateway health check successful")
        else:
            print(f"✗ Production gateway health failed: {response.status_code}")
            return False
        
        # Test jobs endpoint
        response = requests.get(f"{base_url}/v1/jobs", headers=headers, timeout=10)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✓ Production jobs endpoint: {len(jobs)} jobs available")
        else:
            print(f"✗ Production jobs endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Production gateway not accessible: {e}")
        return False

def run_all_tests():
    """Run all Phase 3 production tests"""
    print("=" * 60)
    print("PHASE 3 PRODUCTION TEST SUITE")
    print("=" * 60)
    print(f"Test started at: {datetime.now().isoformat()}")
    
    tests = [
        ("Dependencies", test_phase3_dependencies),
        ("Engine Import", test_phase3_engine_import),
        ("Engine Initialization", test_phase3_engine_initialization),
        ("Semantic Matching", test_phase3_semantic_matching),
        ("Batch Processing", test_phase3_batch_processing),
        ("Agent Service", test_agent_service_endpoints),
        ("Production Gateway", test_production_gateway_endpoints)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            print()
    
    print("=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Phase 3 Production Ready!")
    else:
        print("❌ SOME TESTS FAILED - Phase 3 needs fixes")
    
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)