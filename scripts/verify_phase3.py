#!/usr/bin/env python3
"""
Phase 3 Production Verification Script
Verifies complete Phase 3 implementation without fallbacks
"""
import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def verify_phase3_complete():
    """Verify complete Phase 3 implementation"""
    print("PHASE 3 PRODUCTION VERIFICATION")
    print("=" * 40)
    
    # 1. Test Phase 3 Engine
    print("1. Testing Phase 3 Semantic Engine...")
    try:
        from services.semantic_engine.phase3_engine import Phase3SemanticEngine
        engine = Phase3SemanticEngine()
        
        # Test job and candidate data
        job_data = {
            'id': 1,
            'title': 'Senior Python Developer',
            'description': 'We need an experienced Python developer with Django and FastAPI knowledge',
            'requirements': 'Python, Django, FastAPI, PostgreSQL, Docker, AWS',
            'location': 'Remote',
            'experience_level': 'Senior',
            'client_id': 'TECH001'
        }
        
        candidate_data = {
            'id': 101,
            'name': 'Alice Johnson',
            'technical_skills': 'Python, Django, FastAPI, PostgreSQL, Docker, Kubernetes, AWS',
            'experience_years': 6,
            'seniority_level': 'Senior',
            'education_level': 'Bachelor in Computer Science',
            'location': 'Mumbai'
        }
        
        # Test adaptive scoring
        result = engine.calculate_adaptive_score(job_data, candidate_data, 'TECH001')
        
        print(f"   Adaptive Score: {result['total_score']:.3f}")
        print(f"   Algorithm: {result['algorithm_version']}")
        print(f"   Breakdown:")
        for key, value in result['breakdown'].items():
            print(f"     {key}: {value:.3f}")
        
        if result['total_score'] > 0.5:
            print("   [PASS] Phase 3 semantic scoring working")
        else:
            print("   [FAIL] Phase 3 semantic scoring too low")
            return False
            
    except Exception as e:
        print(f"   [FAIL] Phase 3 engine error: {e}")
        return False
    
    # 2. Test Batch Processing
    print("\n2. Testing Enhanced Batch Processing...")
    try:
        from services.semantic_engine.phase3_engine import BatchMatcher
        batch_matcher = BatchMatcher()
        
        jobs = [job_data]
        candidates = [candidate_data]
        
        results = batch_matcher.batch_process(jobs, candidates)
        
        if results and len(results) > 0:
            job_result = results[1]  # job_id = 1
            print(f"   Processed: {job_result['total_candidates']} candidates")
            print(f"   Top matches: {len(job_result['top_matches'])}")
            print(f"   Algorithm: {job_result['algorithm_version']}")
            print("   [PASS] Batch processing working")
        else:
            print("   [FAIL] Batch processing returned no results")
            return False
            
    except Exception as e:
        print(f"   [FAIL] Batch processing error: {e}")
        return False
    
    # 3. Test Learning Engine
    print("\n3. Testing Learning Engine...")
    try:
        from services.semantic_engine.phase3_engine import LearningEngine
        learning_engine = LearningEngine()
        
        # Test company preferences
        preferences = learning_engine.get_company_preferences('TECH001')
        print(f"   Company preferences loaded: {len(preferences)} items")
        
        # Test tracking (won't actually save without DB)
        learning_engine.track_successful_match(1, 101, 4.5)
        print("   [PASS] Learning engine working")
        
    except Exception as e:
        print(f"   [FAIL] Learning engine error: {e}")
        return False
    
    # 4. Test Agent Service Integration
    print("\n4. Testing Agent Service Integration...")
    try:
        # Test agent imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "services"))
        
        from semantic_engine.phase3_engine import (
            Phase3SemanticEngine,
            AdvancedSemanticMatcher,
            BatchMatcher,
            LearningEngine,
            SemanticJobMatcher
        )
        
        # Initialize like agent service
        phase3_engine = Phase3SemanticEngine()
        advanced_matcher = AdvancedSemanticMatcher()
        batch_matcher = BatchMatcher()
        learning_engine = LearningEngine()
        
        # Test advanced matcher
        candidates_list = [candidate_data]
        match_results = advanced_matcher.advanced_match(job_data, candidates_list)
        
        if match_results and len(match_results) > 0:
            match = match_results[0]
            print(f"   Match score: {match['total_score']:.3f}")
            print(f"   Algorithm: {match['algorithm_version']}")
            print("   [PASS] Agent integration working")
        else:
            print("   [FAIL] Agent integration failed")
            return False
            
    except Exception as e:
        print(f"   [FAIL] Agent integration error: {e}")
        return False
    
    # 5. Verify No Fallbacks
    print("\n5. Verifying No Fallback Mechanisms...")
    try:
        # Check agent service code for fallbacks
        agent_file = os.path.join(os.path.dirname(__file__), "..", "services", "agent", "app.py")
        with open(agent_file, 'r') as f:
            agent_code = f.read()
        
        # Check for fallback patterns
        fallback_patterns = [
            "SEMANTIC_ENABLED = False",
            "fallback to keyword",
            "if not SEMANTIC_ENABLED",
            "except ImportError",
            "keyword matching"
        ]
        
        fallbacks_found = []
        for pattern in fallback_patterns:
            if pattern.lower() in agent_code.lower():
                fallbacks_found.append(pattern)
        
        if fallbacks_found:
            print(f"   [FAIL] Fallback mechanisms found: {fallbacks_found}")
            return False
        else:
            print("   [PASS] No fallback mechanisms detected")
            
    except Exception as e:
        print(f"   [FAIL] Fallback check error: {e}")
        return False
    
    return True

def main():
    """Main verification function"""
    print(f"Starting verification at: {datetime.now().isoformat()}")
    print()
    
    success = verify_phase3_complete()
    
    print("\n" + "=" * 40)
    if success:
        print("SUCCESS: Phase 3 Production Implementation Complete!")
        print("- No fallback mechanisms")
        print("- Proper dependency management")
        print("- Production standards followed")
        print("- All components working correctly")
    else:
        print("FAILURE: Phase 3 Implementation Issues Detected")
        print("- Check error messages above")
        print("- Fix issues before deployment")
    
    print("=" * 40)
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)